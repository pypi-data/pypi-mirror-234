# Module oqtant.oqtant_client

## Functions

`get_oqtant_client(token: str) ‑> oqtant.oqtant_client.OqtantClient`
: A utility function to create a new OqtantClient instance.
Args:
token (str): the auth0 token required for interacting with the Oqtant REST API
Returns:
OqtantClient: authenticated instance of OqtantClient

`version_check(client_version: str) ‑> None`
: Compares the given current Oqtant version with the version currently on pypi,
and raises a warning if it is older.
Args:
client_version (str): the client semver version number

## Classes

`OqtantClient(*, settings, token, debug: bool = False)`
: Python class for interacting with Oqtant
This class contains tools for: - Accessing all of the functionality of the Oqtant Web App (https://oqtant.infleqtion.com) - BARRIER (Barrier Manipulator) jobs - BEC (Ultracold Matter) jobs - Building parameterized (i.e. optimization) experiments using OqtantJobs - Submitting and retrieving OqtantJob results
How Oqtant works:
1.) Construct a single or list of OqtantJobs using 'generate_oqtant_job()'
2.) Run the single or list of OqtantJobs on the Oqtant hardware using 'run_jobs()' - There is a limit of 30 OqtantJobs per use of 'run_jobs()'
3.) As OqtantJobs are running, the results are automatically stored in 'active_jobs' - The OqtantJobs stored in 'active_jobs' are available until the python session ends
4.) If you choose to not track the status of OqtantJobs with 'run_jobs()' you can see the status
of your session's active OqtantJobs with 'see_active_jobs()'
5.) To operate on jobs submitted in a previous session you can load them into your 'active_jobs'
by using either 'load_job_from_id()' or 'load_job_from_file()'
6.) To analyze OqtantJob objects and use Oqtant's job analysis library reference the OqtantJob
class documentation located in 'oqtant/job.py'
Need help? Found a bug? Contact albert@infleqtion.com for support. Thank you!

    ### Methods

    `generate_oqtant_job(self, *, job: dict) ‑> oqtant.schemas.job.OqtantJob`
    :   Generates an instance of OqtantJob from the provided dictionary that contains the
           job details and input. Will validate the values and raise an informative error if
           any violations are found.
        Args:
           job (dict): dictionary containing job details and input
        Returns:
           OqtantJob: an OqtantJob instance containing the details and input from the provided
              dictionary

    `get_job(self, job_id: str, run: int = 1) ‑> oqtant.schemas.job.OqtantJob`
    :   Gets an OqtantJob from the Oqtant REST API. This will always be a targeted query
           for a specific run. If the run is omitted then this will always return the first
           run of the job. Will return results for any job regardless of it's status.
        Args:
            job_id (str): this is the external_id of the job to fetch
            run (int): the run to target, this defaults to the first run if omitted
        Returns:
            OqtantJob: an OqtantJob instance with the values of the job queried

    `get_job_inputs_without_output(self, job_id: str, run: int | None = None, include_notes: bool = False) ‑> dict`
    :   Gets an OqtantJob from the Oqtant REST API. This can return all runs within a job
           or a single run based on whether a run value is provided. The OqtantJobs returned
           will be converted to dictionaries and will not have any output data, even if
           they are complete. This is useful for taking an existing job and creating a new one
           based on it's input data.
        Args:
           job_id (str): this is the external_id of the job to fetch
           run (Union[int, None]): optional argument if caller wishes to only has a single run returned
           include_notes (bool): optional argument if caller wishes to include any notes associated
              with OqtantJob inputs. Defaults to False is not provided
        Returns:
           dict: a dict representation of an OqtantJob instance

    `get_job_limits(self) ‑> dict`
    :   Utility method to get job limits from the Oqtant REST API
        Returns:
            dict: dictionary of job limits

    `load_job_from_file(self, file: str) ‑> None`
    :   Loads an OqtantJob from the Oqtant REST API into the current active_jobs list using a file
           containing OqtantJob info. The results of the jobs loaded by this function are limited to
           their first run.
        Args:
           file_list (list[str]): list of filenames containing OqtantJob information

    `load_job_from_file_list(self, file_list: list) ‑> None`
    :   Loads OqtantJobs from the Oqtant REST API into the current active_jobs list using a list
           of filenames containing OqtantJob info. The results of the jobs loaded by this function are
           limited to their first run.
        Args:
           file_list (list[str]): list of filenames containing OqtantJob information

    `load_job_from_id(self, job_id: str, run: int = 1) ‑> None`
    :   Loads an OqtantJob from the Oqtant REST API into the current active_jobs list using a job
           external_id. The results of the jobs loaded by this function can be targeted to a specific
           run if there are multiple.
        Args:
           job_id (str): the external_id of the job to load
           run (int): optional argument to target a specific job run

    `load_job_from_id_list(self, job_id_list: list) ‑> None`
    :   Loads OqtantJobs from the Oqtant REST API into the current active_jobs list using a list
           of job external_ids. The results of the jobs loaded by this function are limited to their
           first run.
        Args:
           job_id_list (list[str]): list of job external_ids to load

    `run_jobs(self, job_list: list, track_status: bool = False, write: bool = False, filename: str | list[str] = '') ‑> list`
    :   Submits a list of OqtantJobs to the Oqtant REST API. This function provides some
           optional functionality to alter how it behaves. Providing it with an argument of
           track_status=True will make it wait and poll the Oqtant REST API until all jobs
           in the list have completed. The track_status functionality outputs each jobs
           current status as it is polling and opens up the ability to use the other optional
           arguments write and filename. The write and filename arguments enable the ability
           to have the results of each completed job written to a file. The value of filename
           is optional and if not provided will cause the files to be created using the
           external_id of each job. If running more than one job and using the filename
           argument it is required that the number of jobs in job_list match the number of
           values in filename.
        Args:
           job_list (list[OqtantJob]): the list of OqtantJob instances to submit for processing
           track_status (bool): optional argument to tell this function to either return
             immediately or wait and poll until all jobs have completed
           write (bool): optional argument to tell this function to write the results of each
             job to file when complete
           filename (Union[str, list[str]]): optional argument to be used in conjunction with the
             write argument. allows the caller to customize the name(s) of the files being created
        Returns:
           list[str]: list of the external_id(s) returned for each submitted job in job_list

    `search_jobs(self, *, job_type: bert_schemas.job.JobType | None = None, name: bert_schemas.job.JobName | None = None, submit_start: str | None = None, submit_end: str | None = None, notes: str | None = None) ‑> list`
    :   Submits a query to the Oqtant REST API to search for jobs that match the provided criteria.
           The search results will be limited to jobs that meet your Oqtant account access.
        Args:
           job_type (job_schema.JobType): the type of the jobs to search for
           name (job_schema.JobName): the name of the job to search for
           submit_start (str): the earliest submit date of the jobs to search for
           submit_start (str): the latest submit date of the jobs to search for
           notes (str): the notes of the jobs to search for
        Returns:
           list[dict]: a list of jobs matching the provided search criteria

    `see_active_jobs(self, refresh: bool = True) ‑> None`
    :   Utility function to print out the current contents of the active_jobs list. The optional
           argument of refresh tells the function whether it should refresh the data of pending or
           running jobs stored in active_jobs before printing out the results. Refreshing also
           updates the data in active_jobs so if jobs were submitted but not tracked this is a way
           to check on their status.
        Args:
           refresh (bool): optional argument to refresh the data of jobs in active_jobs

    `submit_job(self, *, job: oqtant.schemas.job.OqtantJob) ‑> dict`
    :   Submits a single OqtantJob to the Oqtant REST API. Upon successful submission this
           function will return a dictionary containing the external_id of the job and it's
           position in the queue.
        Args:
           job (OqtantJob): the OqtantJob instance to submit for processing
        Returns:
           dict: dictionary containing the external_id of the job and it's queue position

    `track_jobs(self, *, pending_jobs: list, filename: str | list = '', write: bool = False) ‑> None`
    :   Polls the Oqtant REST API with a list of job external_ids and waits until all of them have
           completed. Will output each job's status while it is polling and will output a message when
           all jobs have completed. This function provides some optional functionality to alter how it
           behaves. Providing it with an argument of write will have it write the results of each
           completed job to a file. There is an additional argument that can be used with write called
           filename. The value of filename is optional and if not provided will cause the files to be
           created using the external_id of each job. If tracking more than one job and using the
           filename argument it is required that the number of jobs in job_list match the number of
           values in filename.
        Args:
           pending_jobs (list[str]): list of job external_ids to track
           write (bool): optional argument to tell this function to write the results of each job to
             file when complete
           filename (Union[str, list[str]]): optional argument to be used in conjunction with the write
             argument. allows the caller to customize the name(s) of the files being created
