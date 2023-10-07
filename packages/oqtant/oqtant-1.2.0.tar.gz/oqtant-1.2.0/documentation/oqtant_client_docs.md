# Oqtant Client

## Capabilities

- Access all the functionality of the Oqtant Web App (https://oqtant.infleqtion.com)

  - BARRIER (Barrier Manipulator) jobs
  - BEC (Ultracold Matter) jobs

- Build parameterized (i.e. optimization) experiments using OqtantJobs

- Submit and retrieve OqtantJob results

## How Oqtant Works

- Construct a single or list of jobs using the OqtantJob class

  - 1D parameter sweeps are supported

- Run a single or list of jobs using run_jobs(). The jobs are submitted to run on hardware in FIFO queue.

  - job lists are run sequentially (uninterrupted) unless list exceeds 30 jobs

- As jobs run, OqtantJob objects are created automatically and stored in active_jobs.

  - View these jobs with see_active_jobs()
  - These jobs are available until the python session ends.

- To operate on jobs from a current or previous session, load them into active_jobs with

  - load_job_from_id(), load_job_from_id_list(), load_job_from_file(), load_job_from_file_list()

- To analyze job objects and use Oqtant's job analysis library, reference the OqtantJob class documentation.

## Considerations

- Oqtant cannot interact with jobs that have been deleted via the Oqtant Web App

- Job results and limits are restricted to the Oqtant account used to authenticate the Oqtant client

- All jobs that have been submitted will be processed even if the Oqtant client session is ended before they complete

## Oqtant API

The Oqtant API provides everything you need to get started working with OqtantJobs and the Oqtant REST API. For more information regarding the Oqtant REST API refer to our [Oqtant REST API Docs](oqtant_rest_api_docs.md)

### get_user_token

A utility method required for getting Oqtant authenticated with your Oqtant account. Starts up a server to handle the Auth0 authentication process and acquire a token. This helper method is located in `oqtant.util.auth`

```
Args:
    auth_server_port (int): optional port to run the authentication server on
Returns:
    str: Auth0 user token
```

### notebook_login

A utility method to display an authentication widget inside of a notebook. Required for getting Oqtant authenticated with your Oqtant account when using Jupyter.

```
Returns:
    Auth: ipywidget widget
```

### get_oqtant_client

A utility method to create a new OqtantClient instance. This helper method requires the token returned from `oqtant.util.auth.get_user_token` and is located in `oqtant.oqtant_client`

```
Args:
    token (str): the auth0 token required for interacting with the Oqtant REST API
Returns:
    OqtantClient: authenticated instance of OqtantClient
```

### get_job

Gets an OqtantJob from the Oqtant REST API. This will always be a targeted query for a specific run. If the run is omitted then this will always return the first run of the job. Will return results for any job regardless of it's status. This method is a member of `OqtantClient`

```
Args:
    job_id (str): this is the external_id of the job to fetch
    run (int): the run to target, this defaults to the first run if omitted
Returns:
    OqtantJob: an OqtantJob instance with the values of the job queried
```

### get_job_without_output

Gets an OqtantJob from the Oqtant REST API. This can return all runs within a job or a single run based on whether a run value is provided. The OqtantJobs returned will not have any output data, even if they are complete. This is useful for taking an existing job and creating a new one based on it's input data. This method is a member of `OqtantClient`

```
Args:
    job_id (str): this is the external_id of the job to fetch
    run (Union[int, None]): optional argument if caller wishes to only has a single run returned
    include_notes (bool): optional argument if caller wishes to include any notes associated with OqtantJob inputs. Defaults to False is not provided
Returns:
    OqtantJob: an OqtantJob instance of the job
```

### generate_oqtant_job

Generates an instance of OqtantJob from the provided dictionary that contains the job details and input. Will validate the values and raise an informative error if any violations are found. This method is a member of `OqtantClient`

```
Args:
    job (Dict): dictionary containing job details and input
Returns:
    OqtantJob: an OqtantJob instance containing the details and input from the provided dictionary
```

### create_job

Generate an instance of OqtantJob. When not providing a dictionary of job data this method will return an OqtantJob instance containing predefined input data based on the value of the job_type and runs. If a dictionary is provided an OqtantJob instance will be created using the data contained within it.

```
Args:
    name (str): the name ofd the job to be created
    job_type (job_schema.JobType): the type of job to be created
    runs (int): the number of runs to include in the job
Returns:
    OqtantJob: an OqtantJob instance of the provided dictionary or predefined input data
```

### submit_job

Submits a single OqtantJob to the Oqtant REST API. Upon successful submission this method will return a dictionary containing the external_id of the job and it's position in the queue. Will write the job data to file when the write argument is True. This method is a member of `OqtantClient`

```
Args:
    job (OqtantJob): the OqtantJob instance to submit for processing
    write (bool): flag to write job data to file
Returns:
    Dict: dictionary containing the external_id of the job and it's queue position
```

### run_jobs

Submits a list of OqtantJobs to the Oqtant REST API. This method provides some optional functionality to alter how it behaves. Providing it with an argument of track_status=True will make it wait and poll the Oqtant REST API until all jobs in the list have completed. Providing it with and argument of write=True will make it write the results of the jobs to file when they complete (only applies when the track_status argument is True). This method is a member of `OqtantClient`.

```
Args:
    job_list (List[OqtantJob]): the list of OqtantJob instances to submit for processing
    track_status (bool): optional argument to tell this method to either return immediately or wait and poll until all jobs have completed
    write (bool): optional argument to tell this method to write the results of each job to file when complete
Returns:
    List[str]: list of the external_id(s) returned for each submitted job in job_list
```

### search_jobs

Submits a query to the Oqtant REST API to search for jobs that match the provided criteria. The search results will be limited to jobs that meet your Oqtant account access. This method is a member of `OqtantClient`

```
Args:
    job_type (JobSchema.JobType): the type of the jobs to search for
    name (JobSchema.JobName): the name of the job to search for
    submit_start (str): the earliest submit date of the jobs to search for
    submit_start (str): the latest submit date of the jobs to search for
    notes (str): the notes of the jobs to search for
    limit (int): the limit for the number of jobs returned (max: 100)
Returns:
    List[Dict]: a list of jobs matching the provided search criteria
```

### track_jobs

Polls the Oqtant REST API with a list of OqtantJobs and waits until all of them have completed. Will output each job's status while it is polling and will output a message when all jobs have completed. When the write argument is True it will also write the jobs' data to file when they complete. This method is a member of `OqtantClient`

```
Args:
    pending_jobs (List[str]): list of job external_ids to track
    write (bool): optional argument to tell this method to write the results of each job to file when complete
    filename (Union[str, List[str]]): optional argument to be used in conjunction with the write argument. allows the caller to customize the name(s) of the files being created
```

### write_job_to_file

Utility method to write an OqtantJob instance to a file. This method is a member of `OqtantClient`

```
Args:
    job (OqtantJob): the OqtantJob instance to write to file
    file_name (str): optional argument to customize the name of the file (defaults to job name)
    file_path (str): optional argument to specify the full path of the file to write, including the name of the file
```

### load_job_from_file

Utility method to load an OqtantJob instance from a file. Will refresh the job data from the Oqtant REST API by default. This method is a member of `OqtantClient`

```
Args:
    file_path (str): the full path to the file to read
    refresh (bool): flag to refresh the job data from Oqtant
Returns:
    OqtantJob: an OqtantJob instance of the loaded job
```

### get_job_limits

Utility method to get job limits from the Oqtant REST API

```
Args:
    show_results (bool): flag to print out the results
Returns:
    dict: dictionary of job limits
```

### check_version

Compares the currently installed version of Oqtant with the latest version on PyPi and will raise a warning if it is older.

```
Returns:
    bool: True if current version is latest, False if it is older
```
