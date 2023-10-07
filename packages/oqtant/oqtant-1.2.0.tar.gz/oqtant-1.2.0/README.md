# Oqtant

[![License: Apache](https://img.shields.io/badge/License-Apache-yellow.svg)](https://opensource.org/licenses/Apache-2.0)
[![pypi](https://img.shields.io/pypi/v/oqtant.svg)](https://pypi.python.org/pypi/oqtant)
[![versions](https://img.shields.io/pypi/pyversions/bert-schemas.svg)](https://pypi.python.org/pypi/bert-schemas)
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/Infleqtion.svg?style=social&label=Follow%20%40Infleqtion)](https://twitter.com/Infleqtion)

## 🚀 Quick Install

```python
pip install oqtant
```

## 🧭 Introduction

This API contains tools to:

- Access all the functionality of the Oqtant Web App (https://oqtant.infleqtion.com)

  - BARRIER (Barrier Manipulator) jobs
  - BEC (Ultracold Matter) jobs

- Build parameterized (i.e. optimization) experiments using OqtantJobs

- Submit and retrieve OqtantJob results

## 🤖 How Oqtant Works

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

Need help? Found a bug? Contact <albert@infleqtion.com> for support. Thank you!

## 📓 Documentation

- [Getting started](https://gitlab.com/infleqtion/albert/oqtant/-/blob/main/documentation/INSTALL.md) (installation, setting up the environment, how to run the walkthrough notebooks)
- [Walkthroughs](https://gitlab.com/infleqtion/albert/oqtant/-/blob/main/documentation/walkthroughs/walkthroughs.md) (demos for creating and submitting jobs)
- [Oqtant REST API docs](https://gitlab.com/infleqtion/albert/oqtant/-/blob/main/documentation/oqtant_rest_api_docs.md)
- [Job Analysis docs](https://gitlab.com/infleqtion/albert/oqtant/-/blob/main/documentation/job_analysis_docs.md)
