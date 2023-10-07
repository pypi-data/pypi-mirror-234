# Copyright 2023 Infleqtion
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
import json
import sys
import time
import warnings
from datetime import datetime
from importlib.metadata import version

import jwt
import requests
import semver
from bert_schemas import job as job_schema
from pydantic import ValidationError
from requests.exceptions import RequestException
from tabulate import tabulate

from oqtant.fixtures.jobs import barrier_manipulator_job, ultracold_matter_job
from oqtant.schemas.job import OqtantJob
from oqtant.schemas.optical import Barrier
from oqtant.schemas.quantum_matter import QuantumMatter
from oqtant.settings import Settings
from oqtant.util import exceptions as api_exceptions
from oqtant.util.auth import get_user_token

settings = Settings()


class OqtantClient:
    """Python class for interacting with Oqtant
    This class contains tools for:
        - Accessing all of the functionality of the Oqtant Web App (https://oqtant.infleqtion.com)
            - BARRIER (Barrier Manipulator) jobs
            - BEC (Ultracold Matter) jobs
        - Building parameterized (i.e. optimization) experiments using OqtantJobs
        - Submitting and retrieving OqtantJob results
    How Oqtant works:
        1.) Construct a single or list of OqtantJobs using 'create_job()'
        2.) Run the single or list of OqtantJobs on the Oqtant hardware using 'run_jobs()'
            - There is a limit of 30 OqtantJobs per use of 'run_jobs()'
            - There is an option to track the status of the submitted jobs which will cause the method
              to hold and wait until all jobs have finished before returning
        3.) Retrieve job results using 'get_job()'
        4.) Analyze OqtantJob objects using Oqtant's job analysis library
    Need help? Found a bug? Contact albert@infleqtion.com for support. Thank you!
    """

    def __init__(self, *, settings, token, debug: bool = False):
        self.base_url: str = settings.base_url
        self.token: str = token
        self.max_ind_var: int = settings.max_ind_var
        self.run_list_limit: int = settings.run_list_limit
        self.debug: bool = debug
        self.version = version("oqtant")
        self.verbosity: int = 1

        if not self.debug:
            sys.tracebacklimit = 0

    def __get_headers(self) -> dict:
        """Generate headers for use in calls to the REST API with requests
        Returns:
            dict: a dict of header information
        """
        return {
            "Authorization": f"Bearer {self.token}",
            "X-Client-Version": version("oqtant"),
        }

    def __print(self, message: str) -> None:
        """Internal method to control the verbosity of the print states
        Args:
            message (str): the message to print
        """
        if self.verbosity >= 1:
            print(message)

    def convert_matter_to_job(self, matter: QuantumMatter) -> OqtantJob:
        """
        Converts a QuantumMatter object to an OqtantJob object.

        Args:
            matter (QuantumMatter): The QuantumMatter object to be converted.

        Returns:
            OqtantJob: The resulting OqtantJob object.
        """
        return OqtantJob(
            **{
                "name": matter.name,
                "inputs": [{"values": matter.input.model_dump(), "notes": matter.note}],
            }
        )

    def submit(
        self,
        matter: QuantumMatter,
        track=False,
        write: bool = False,
        filename: str = "",
        target: str
        | None = None,  # TODO: implement as qpu or hardware/simulator backend
    ) -> str:
        """
        Submits a QuantumMatter object for execution, returns the resulting job id.

        Args:
            matter (QuantumMatter): The QuantumMatter object to submit for execution.
            track (bool, optional): Whether to track the status of the resulting job. Defaults to False.
            write (bool, optional): Whether to write the result to a file. Defaults to False.
            filename (str, optional): The name of the file to write the result to. Defaults to "".
            target (str, optional): The target backend to run the resulting job on. Defaults to None.

        Returns:
            str: The resulting Job ID of the resulting job.
        """
        job = self.convert_matter_to_job(matter)
        return self.run_jobs(job_list=[job], track_status=track)[0]

    def submit_list(
        self,
        matter_list: list[QuantumMatter],
        track=False,
        write: bool = False,
        filename: str = "",
        target: str
        | None = None,  # TODO: implement as qpu target or hardware/simulator backend
    ) -> list[str]:
        """
        Submits a list of QuantumMatter objects to be executed as OqtantJobs.

        Args:
            matters (list): The list of QuantumMatter objects to be submitted.
            track (bool, optional): Whether to track the status of the resulting jobs. Defaults to False.
            write (bool, optional): Whether to write the results to a file. Defaults to False.
            filename (str, optional): The name of the file to write the results to. Defaults to "".
            target (str, optional): The QPU target or hardware/simulator backend where the program should run. Defaults to None.

        Returns:
            list[str]: A list of job IDs for the submitted programs.
        """
        job_list = [self.convert_matter_to_job(matter) for matter in matter_list]
        return self.run_jobs(job_list=job_list, track_status=track)

    def submit_list_as_batch(
        self,
        matter_list: list[QuantumMatter],
        track: bool = False,
        write: bool = False,
        filename: str = "",
        name: str | None = None,  # optional global name for resulting job
        target: str
        | None = None,  # TODO: implement as qpu target or hardware/simulator backend
    ) -> str:
        """
        Submit a list of QuantumMatter objects as a batch job for execution.

        Args:
            matters (list): The list of QuantumMatter objects to submit as a single batch job.
            track (bool, optional): Whether to track the status of the job. Defaults to False.
            write (bool, optional): Whether to write the job to a file. Defaults to False.
            filename (str, optional): The name of the file to write the job to. Defaults to "".
            name (str | None, optional): The name of the batch job. If None, the name of the first program will be used. Defaults to None.
            target (str | None, optional): The target for the job. TODO: implement as qpu target or hardware/simulator backend where program should run. Defaults to None.

        Returns:
            str: The ID of the submitted job.
        """
        if name is None:
            name = matter_list[0].name
        inputs = []
        master_job_type = self.convert_matter_to_job(matter_list[0]).job_type
        for matter in matter_list:
            job_type = self.convert_matter_to_job(matter).job_type
            if job_type is not master_job_type:
                raise api_exceptions.OqtantError(
                    "All input objects must map to the same job type."
                )
            inputs.append({"values": matter.input.model_dump(), "notes": matter.note})
        job_data = {
            "name": name,
            "inputs": inputs,
        }
        job = OqtantJob(**job_data)
        ids = self.run_jobs(job_list=[job], track_status=track)
        return ids[0]

    def get_job(self, job_id: str, run: int = 1) -> OqtantJob:
        """Gets an OqtantJob from the Oqtant REST API. This will always be a targeted query
           for a specific run. If the run is omitted then this will always return the first
           run of the job. Will return results for any job regardless of it's status.
        Args:
            job_id (str): this is the external_id of the job to fetch
            run (int): the run to target, this defaults to the first run if omitted
        Returns:
            OqtantJob: an OqtantJob instance with the values of the job queried
        """
        request_url = f"{self.base_url}/{job_id}"
        params = {"run": run}
        response = requests.get(
            url=request_url,
            params=params,
            headers=self.__get_headers(),
            timeout=(5, 30),
        )
        if response.status_code in [401, 403]:
            raise api_exceptions.OqtantAuthorizationError
        try:
            response.raise_for_status()
        except RequestException as err:
            raise api_exceptions.OqtantRequestError(
                f"Failed to get job '{job_id}' from Oqtant"
            ) from err
        job_data = response.json()
        try:
            job = OqtantJob(**job_data)
        except ValidationError as err:
            raise api_exceptions.OqtantJobValidationError(
                f"Failed to validate job '{job_id}'"
            ) from err
        except (KeyError, Exception) as err:
            raise api_exceptions.OqtantJobParameterError(
                f"Failed to parse job '{job_id}'"
            ) from err
        return job

    def get_job_without_output(
        self, job_id: str, run: int | None = None, include_notes: bool = False
    ) -> OqtantJob:
        """Gets an OqtantJob from the Oqtant REST API. This can return all runs within a job
           or a single run based on whether a run value is provided. The OqtantJobs returned
           will not have any output data, even if they are complete. This is useful for
           taking an existing job and creating a new one based on it's input data.
        Args:
           job_id (str): this is the external_id of the job to fetch
           run (Union[int, None]): optional argument if caller wishes to only has a single run returned
           include_notes (bool): optional argument if caller wishes to include any notes associated
             with OqtantJob inputs. Defaults to False is not provided
        Returns:
           OqtantJob: an OqtantJob instance of the job
        """
        request_url = f"{self.base_url}/{job_id}"
        params = {"exclude_input_output": True}
        if run:
            params["run"] = run
        response = requests.get(
            url=request_url,
            params=params,
            headers=self.__get_headers(),
            timeout=(5, 30),
        )
        if response.status_code in [401, 403]:
            raise api_exceptions.OqtantAuthorizationError
        try:
            response.raise_for_status()
        except RequestException as err:
            raise api_exceptions.OqtantRequestError(
                f"Failed to get job '{job_id}' from Oqtant"
            ) from err
        job_data = response.json()
        try:
            job = OqtantJob(**job_data)
        except ValidationError as err:
            raise api_exceptions.OqtantJobValidationError(
                f"Failed to validate job '{job_id}'"
            ) from err
        except (KeyError, Exception) as err:
            raise api_exceptions.OqtantJobParameterError(
                f"Failed to parse job '{job_id}'"
            ) from err
        if not include_notes:
            job.inputs[0].notes = ""
        return job

    # necessary?
    def generate_oqtant_job(self, *, job: dict) -> OqtantJob:
        """Generates an instance of OqtantJob from the provided dictionary that contains the
           job details and input. Will validate the values and raise an informative error if
           any violations are found.
        Args:
           job (dict): dictionary containing job details and input
        Returns:
           OqtantJob: an OqtantJob instance containing the details and input from the provided
             dictionary
        """
        try:
            oqtant_job = OqtantJob(**job)
        except (KeyError, ValidationError) as err:
            raise api_exceptions.OqtantJobValidationError(
                "Failed to generate OqtantJob"
            ) from err
        return oqtant_job

    def create_job(
        self,
        name: str,
        job_type: job_schema.JobType,
        runs: int = 1,
        job: dict | None = None,
    ) -> OqtantJob:
        """Generates an instance of OqtantJob. When not providing a dictionary of job data this
           method will return an OqtantJob instance containing predefined input data based on
           the value of job_type and runs. If a dictionary is provided an OqtantJob instance will
           be created using the data contained within it.
        Args:
            name (str): the name of the job to be created
            job_type (job_schema.JobType): the type of job to be created
            runs (int): the number of runs to include in the job
        Returns:
            OqtantJob: an OqtantJob instance of the provided dictionary or predefined input data
        """
        if job:
            job["name"] = name
            job["job_type"] = job_type
            job = self.generate_oqtant_job(job=job)
            return job
        if job_type == job_schema.JobType.BARRIER:
            job = barrier_manipulator_job
        elif job_type == job_schema.JobType.BEC:
            job = ultracold_matter_job
        else:
            raise api_exceptions.OqtantJobUnsupportedTypeError(
                f"Job type '{job_type}' is either invalid or unsupported"
            )
        job = self.generate_oqtant_job(job=job)
        job.inputs = [copy.deepcopy(job.inputs[0].model_dump())] * runs
        job.name = name
        return job

    def submit_job(self, *, job: OqtantJob, write: bool = False) -> dict:
        """Submits a single OqtantJob to the Oqtant REST API. Upon successful submission this
           method will return a dictionary containing the external_id of the job and it's
           position in the queue. Will write the job data to file when the write argument is True
        Args:
           job (OqtantJob): the OqtantJob instance to submit for processing
           write (bool): flag to write job data to file
        Returns:
           dict: dictionary containing the external_id of the job and it's queue position
        """
        if not isinstance(job, OqtantJob):
            try:
                job = OqtantJob(**job)
            except (TypeError, AttributeError, ValidationError) as err:
                raise api_exceptions.OqtantJobValidationError(
                    "OqtantJob is invalid"
                ) from err
        data = {
            "name": job.name,
            "job_type": job.job_type,
            "input_count": len(job.inputs),
            "inputs": [input.model_dump() for input in job.inputs],
        }
        response = requests.post(
            url=self.base_url,
            json=data,
            headers=self.__get_headers(),
            timeout=(5, 30),
        )
        if response.status_code in [401, 403]:
            raise api_exceptions.OqtantAuthorizationError
        try:
            response.raise_for_status()
        except RequestException as err:
            raise api_exceptions.OqtantRequestError(
                "Failed to submit job to Oqtant"
            ) from err
        response_data = response.json()
        if write:
            job.status = job_schema.JobStatus.PENDING
            job.external_id = response_data["job_id"]
            self.write_job_to_file(job)
        return response_data

    def run_jobs(
        self, job_list: list[OqtantJob], track_status: bool = False, write: bool = False
    ) -> list[str]:
        """Submits a list of OqtantJobs to the Oqtant REST API. This method provides some
           optional functionality to alter how it behaves. Providing it with an argument of
           track_status=True will make it wait and poll the Oqtant REST API until all jobs
           in the list have completed. Providing it with and argument of write=True will make
           it write the results of the jobs to file when they complete (only applies when the
           track_status argument is True)
        Args:
           job_list (list[OqtantJob]): the list of OqtantJob instances to submit for processing
           track_status (bool): optional argument to tell this method to either return
             immediately or wait and poll until all jobs have completed
            write (bool): optional argument to tell this method to write job results to file
        Returns:
           list[str]: list of the external_id(s) returned for each submitted job in job_list
        """
        if len(job_list) > self.run_list_limit:
            raise api_exceptions.OqtantJobListLimitError(
                f"Maximum number of jobs submitted per run is {self.run_list_limit}."
            )
        pending_jobs = []
        submitted_jobs = []
        self.__print(f"Submitting {len(job_list)} job(s):")
        for job in job_list:
            response = self.submit_job(job=job, write=write)
            external_id = response["job_id"]
            queue_position = response["queue_position"]
            est_time = response["est_time"]
            job.external_id = external_id
            pending_jobs.append(job)
            submitted_jobs.append(job)
            self.__print(f"\n- Job: {job.name}")
            self.__print(f"  ID: {job.external_id}")
            self.__print(f"  Queue Position: {queue_position}")
            self.__print(f"  Estimated Time: {est_time} minutes")
        if track_status:
            self.track_jobs(pending_jobs=pending_jobs, write=write)
        return [str(job.external_id) for job in submitted_jobs]

    def search_jobs(
        self,
        *,
        job_type: job_schema.JobType | None = None,
        name: job_schema.JobName | None = None,
        submit_start: str | None = None,
        submit_end: str | None = None,
        notes: str | None = None,
        limit: int = 100,
        show_results: bool = False,
    ) -> list[dict]:
        """Submits a query to the Oqtant REST API to search for jobs that match the provided criteria.
           The search results will be limited to jobs that meet your Oqtant account access.
        Args:
           job_type (job_schema.JobType): the type of the jobs to search for
           name (job_schema.JobName): the name of the job to search for
           submit_start (str): the earliest submit date of the jobs to search for
           submit_start (str): the latest submit date of the jobs to search for
           notes (str): the notes of the jobs to search for
           limit (int): the limit for the number of jobs returned (max: 100)
        Returns:
           list[dict]: a list of jobs matching the provided search criteria
        """
        params = {"limit": limit}
        for param in ["job_type", "name", "submit_start", "submit_end", "notes"]:
            if locals()[param] is not None:
                params[param] = locals()[param]

        print(params)

        response = requests.get(
            url=self.base_url,
            params=params,
            headers=self.__get_headers(),
            timeout=(5, 30),
        )
        if response.status_code in [401, 403]:
            raise api_exceptions.OqtantAuthorizationError
        try:
            response.raise_for_status()
        except RequestException as err:
            raise api_exceptions.OqtantRequestError(
                "Failed to search jobs in Oqtant"
            ) from err
        job_data = response.json().get("items", [])
        if show_results and job_data:
            self.__print(f"Search returned {len(job_data)} job(s):\n")
            rows = [
                [
                    job.get("name")
                    if len(job.get("name", [])) < 40
                    else f"{job.get('name')[:37]}...",
                    job.get("job_type"),
                    job.get("status"),
                    job.get("external_id"),
                ]
                for job in job_data
            ]
            table = [
                ["Name", "Job Type", "Status", "ID"],
                *rows,
            ]
            self.__print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))
        return job_data

    def track_jobs(self, pending_jobs: list[OqtantJob], write: bool = False) -> None:
        """Polls the Oqtant REST API with a list of OqtantJobs and waits until all of them have
           completed. Will output each job's status while it is polling and will output a message when
           all jobs have completed. When the write argument is True it will also write the jobs' data
           to file when they complete.
        Args:
           pending_jobs (list[str]): list of job external_ids to track
           write (bool): optional argument to tell this method to write job results to file
        """
        self.__print(f"\nTracking {len(pending_jobs)} job(s):")
        pending_jobs = {str(job.external_id): job for job in pending_jobs}
        running_job = None
        while pending_jobs:
            if not running_job:
                for external_id, pending_job in pending_jobs.items():
                    job = self.get_job(job_id=external_id)
                    if job.status != pending_job.status:
                        pending_jobs[external_id].status = job.status
                        running_job = pending_jobs[external_id]
                        self.__print(f"\n- Job: {job.name}")
                        self.__print(f"  - {job.status}")
                        break
            else:
                job = self.get_job(job_id=running_job.external_id)
                if job.status != running_job.status:
                    if job.status in [
                        job_schema.JobStatus.INCOMPLETE,
                        job_schema.JobStatus.FAILED,
                        job_schema.JobStatus.COMPLETE,
                    ]:
                        pending_jobs.pop(str(running_job.external_id), None)
                        running_job = None
                    else:
                        running_job.status = job.status
                    self.__print(f"  - {job.status}")
                    if not running_job and write:
                        self.write_job_to_file(job)
            time.sleep(2)
        self.__print("\nAll job(s) complete")

    def write_job_to_file(
        self,
        job: OqtantJob,
        file_name: str | None = None,
        file_path: str | None = None,
    ) -> None:
        """Utility method to write an OqtantJob instance to a file.
        Args:
           job (OqtantJob): the OqtantJob instance to write to file
           file_name (str): optional argument to customize the name of the file (defaults to job name)
           file_path (str): optional argument to specify the full path to the file to write, including
             the name of the file
        """
        if file_path:
            target = file_path
        else:
            if job.input_count > 1:
                target = f"{file_name if file_name else str(job.external_id)}"
                target += (
                    "_run_"
                    + str(job.inputs[job.active_run - 1].run)
                    + "_of_"
                    + str(job.input_count)
                    + ".txt"
                )
            else:
                target = f"{file_name if file_name else str(job.external_id)}.txt"
        try:
            with open(target, "w+") as f:
                f.write(str(job.model_dump_json()))
                print(f'Wrote file: "{target}"')
        except Exception as err:
            raise api_exceptions.JobWriteError(
                f"Failed to write job to '{target}'"
            ) from err

    def load_job_from_file(self, file_path: str, refresh: bool = True) -> OqtantJob:
        """Utility method to load an OqtantJob instance from a file. Will refresh the job data from the
           Oqtant REST API by default
        Args:
           file_path (str): the full path to the file to read
           refresh (bool): flag to refresh the job data from Oqtant
        Returns:
            OqtantJob: an OqtantJob instance of the loaded job
        """
        try:
            with open(file_path) as json_file:
                data = json.load(json_file)
                job = OqtantJob(**data)
                if refresh:
                    job = self.get_job(job.external_id)
                    self.write_job_to_file(job, file_path=file_path)
                return job
        except FileNotFoundError as err:
            raise api_exceptions.JobReadError(
                f"Failed to load job from {file_path}"
            ) from err
        except (ValidationError, KeyError) as err:
            raise api_exceptions.JobReadError(
                f"Failed to parse job from {file_path}"
            ) from err
        except RequestException as err:
            raise api_exceptions.JobReadError(
                f"Failed to refresh job from {file_path}"
            ) from err

    def get_job_limits(self, show_results: bool = False) -> dict:
        """Utility method to get job limits from the Oqtant REST API
        Args:
            show_results (bool): flag to print out the results
        Returns:
            dict: dictionary of job limits
        """
        try:
            token_data = jwt.decode(
                self.token, key=None, options={"verify_signature": False}
            )
            external_user_id = token_data["sub"]
        except Exception as err:
            raise api_exceptions.OqtantTokenError(
                "Unable to decode JWT token. Please contact Infleqtion"
            ) from err

        url = f"{self.base_url.replace('jobs', 'users')}/{external_user_id}/job_limits"
        response = requests.get(
            url=url,
            headers=self.__get_headers(),
            timeout=(5, 30),
        )
        if response.status_code in [401, 403]:
            raise api_exceptions.OqtantAuthorizationError()
        try:
            response.raise_for_status()
        except RequestException as err:
            raise api_exceptions.OqtantRequestError(
                "Failed to get job limits from Oqtant"
            ) from err
        job_limits = response.json()
        if show_results:
            limit_table = [
                ["Daily Used", "Daily Remaining", "Daily Limit"],
                [
                    job_limits["daily_used"],
                    job_limits["daily_remaining"],
                    job_limits["daily_limit"],
                ],
            ]
            if job_limits["purchased_remaining"] > 0:
                limit_table[0].append("Purchased Remaining")
                limit_table[1].append(job_limits["purchased_remaining"])
            self.__print(
                "Job Limits:\n"
                + tabulate(limit_table, headers="firstrow", tablefmt="fancy_grid")
            )
        return job_limits

    def show_job_limits(self) -> None:
        self.get_job_limits(show_results=True)

    def get_queue_status(
        self,
        job_type: job_schema.JobType | None = None,
        name: job_schema.JobName | None = None,
        submit_start: str = datetime.now().isoformat(),
        submit_end: str = datetime.now().isoformat(),
        note: str | None = None,
        limit: int = 50,
        include_complete: bool = False,
        show_results: bool = False,
    ) -> list:
        search_results = list(
            filter(
                lambda job: True
                if include_complete
                else job.get("status") != job_schema.JobStatus.COMPLETE,
                self.search_jobs(
                    job_type=job_type,
                    name=name,
                    submit_start=submit_start,
                    submit_end=submit_end,
                    notes=note,
                    limit=limit,
                ),
            )
        )
        if show_results:
            self.__print(f"{len(search_results)} job(s) queued:\n")
            rows = [
                [
                    job.get("name")
                    if len(job.get("name", [])) < 40
                    else f"{job.get('name')[:37]}...",
                    job.get("status"),
                    OqtantJob.format_datetime_string(job.get("time_submit")),
                    job.get("external_id"),
                ]
                for job in search_results
            ]
            table = [
                ["Name", "Status", "Submit", "ID"],
                *rows,
            ]
            self.__print(tabulate(table, headers="firstrow", tablefmt="fancy_grid"))
        return search_results

    def show_queue_status(self, *args, **kwargs) -> None:
        self.get_queue_status(*args, **kwargs, show_results=True)

    def check_version(self) -> bool:
        """Compares the currently installed version of Oqtant with the latest version PyPi
        and will raise a warning if it is older
        Returns:
            bool: True if current version is latest, False if it is older
        """
        resp = requests.get("https://pypi.org/pypi/oqtant/json", timeout=5)
        current = True
        if resp.status_code == 200:
            current_version = resp.json()["info"]["version"]
            if semver.compare(self.version, current_version) < 0:
                current = False
                warnings.warn(
                    f"Please upgrade to Oqtant version {current_version}. "
                    f"You are currently using version {self.version}"
                )
        return current


def get_oqtant_client(token: str) -> OqtantClient:
    """A utility method to create a new OqtantClient instance.
    Args:
        token (str): the auth0 token required for interacting with the Oqtant REST API
    Returns:
        OqtantClient: authenticated instance of OqtantClient
    """

    client = OqtantClient(settings=settings, token=token)
    client.check_version()
    client.show_job_limits()
    return client


def get_client(port: int = 8080) -> OqtantClient:
    token = get_user_token(auth_server_port=port)
    client = OqtantClient(settings=settings, token=token)
    return client
