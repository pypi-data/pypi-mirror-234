# Oqtant Quickstart Guide

This Quickstart Guide assumes the user has some familiarity with Python

To get started with Oqtant you will need to have the following installed:

- Python >=3.10 and <3.12

# User Account

You will need to have a registered Explorer account, available at https://oqtant.infleqtion.com.

# Installation

Oqtant is compatible with Windows, Mac and Linux. Below are the steps needed to get Oqtant installed with instructions for each operating system

## Python + Pip

If you do not already have a compatible version of python and pip installed on your system follow the instructions below:

**Note: Depending on how python is installed on your system you may need to adjust which version of python to use in the following steps (ex: python3 or python3.11). This also applies to pip (ex: pip or pip3)**

### Terminal

In order to complete the installation of and use Oqtant you will need to open a terminal of your choice based on your operating system. The following have been confirmed to work with Oqtant:

- Windows Command Prompt
- Windows PowerShell
- Windows Terminal
- Linux Bash/Zsh Shell
- Mac Terminal

### Windows

1. Download the latest stable version of python here: https://www.python.org/downloads/windows/
2. Open the executable to start the installation wizard
3. Before proceeding with the wizard make sure to select the "Add Python to PATH" option
4. Once finished, open your preferred terminal and verify python is installed using `python --version`
5. Ensure that pip is installed alongside python by running `py -m ensurepip --upgrade`
6. Run `pip --version` to confirm installation

### Mac

1. Download the latest stable version of python here: https://www.python.org/downloads/macos/
2. Open the executable to start the installation wizard
3. Once finished, open your preferred terminal and verify python is installed using `python --version`
   - If after running `python --version` you encounter an error similar to: `xcode-select: note: no developer tools were found at '/Applications/Xcode.app', requesting install. Choose an option in the dialog to download the command line developer tools`, you will need to select the install option in the pop-up window that appears. Once the installation is complete you should now be able to run `python --version`
4. Ensure that pip is installed alongside python by running `python -m ensurepip --upgrade`
5. Run `pip --version` to confirm installation

### Linux

Many distributions of linux already come with a version of python installed. To check run `python --version` and verify if it is installed and within >=3.10 and <3.12. If python is not installed or you need to install a newer version you can run the following:

1. Download the latest stable version of python here: https://www.python.org/downloads/source/
2. Extract the tarball using `tar -xf`
3. Navigate to the now extracted file and execute `./configure`
4. If your system does not have an existing version of python installed run `sudo make install`, otherwise run `sudo make altinstall`
5. Once finished, open your preferred terminal and verify python is installed using `python --version`
6. Ensure that pip is installed alongside python by running `python -m ensurepip --upgrade`
7. Run `pip --version` to confirm installation

## Oqtant

As dependencies of the Oqtant package the following are downloaded automatically and do not need to be installed separately:

- Jupyter Notebook
- Matplotlib
- Numpy
- Scipy
- Scikit-learn

Below are the steps for installing Oqtant by operating system:

If you are using Anaconda/Miniconda you can follow these [steps](#using-conda)

### Windows

**Note: You can use either Command Prompt or PowerShell with Oqtant. The steps for each only differ slightly**

1. Create a python virtual environment to install Oqtant into:

   ```
   python -m venv .venv
   ```

   **Note: You can name your virtual environment whatever makes sense to you. In the above example we use `.venv`**

2. Activate your virtual environment:

   ### Command Prompt

   ```
   <path to virtual environment location>\.venv\Scripts\activate.bat
   ```

   Replace `<path to virtual environment location>` with where the virtual environment was created. The path should include the name of the virtual environment, in this case we used `.venv`

   ### PowerShell

   If this is your first time using PowerShell you will need to run the following command and answer the prompt with `A`:

   ```
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
   ```

   Going forward you will not need to repeat the above command. Now you can activate your virtual environment with the following command:

   ```
   .\<path to virtual environment location>\.venv\Scripts\Activate.ps1
   ```

   Replace `<path to virtual environment location>` with where the virtual environment was created. The path should include the name of the virtual environment, in this case we used `.venv`

3. Inside of the activated virtual environment run the following command to install Oqtant and it's dependencies:

   ```
   pip install oqtant
   ```

### Linux/Mac

1. Create a python virtual environment to install Oqtant into:

   ```
   python -m venv .venv
   ```

   **Note: You can name your virtual environment whatever makes sense to you. In the above example we use `.venv`**

2. Activate your virtual environment:

   ```
   source <path to virtual environment location>/.venv/bin/activate
   ```

   Replace `<path to virtual environment location>` with where the virtual environment was created. The path should include the name of the virtual environment, in this case we used `.venv`

3. Once activated run the following command to install Oqtant and it's dependencies:

   ```
   pip install oqtant
   ```

### Using Conda

If you are using Anaconda/Miniconda to manage python environments you can follow the steps below:

1. Create a conda environment to install Oqtant into:

   ```
   conda create --name oqtant PYTHON=3.10
   ```

2. Activate your virtual environment:

   ```
   conda activate oqtant
   ```

3. Once activated run the following command to install Oqtant and it's dependencies:

   ```
   pip install oqtant
   ```

   If your conda environment is missing pip you can install it and run the above again:

   ```
   conda install pip
   ```

# Walkthrough Notebooks

Getting started with Oqtant is easy using the walkthrough notebooks. These walkthroughs will walk you through the basic functions of using Oqtant to interact with the Oqtant hardware. Feel free to use these as a starting point for your own code: edit, rename, share… they are yours.

## Downloading Walkthrough Notebooks

You can download a copy of our walkthrough notebooks from our GitLab project located here: https://gitlab.com/infleqtion/albert/oqtant/-/tree/main/documentation

## Running Walkthrough Notebooks

To start up Jupyter and begin using the walkthrough notebooks run the following command in the same directory as the notebook files you have downloaded:

```
jupyter notebook
```

- This will open a tab in your default web browser with a file explorer type interface.
- Using this interface navigate to the location of the provided notebooks and select one to open.
- This will open another tab with the contents of the selected notebook.
- Each notebook has pre-populated examples you can then execute with instructions for each step
- For a more detailed explanation of the Oqtant REST API refer to our [API Docs](oqtant_rest_api_docs.md)

If you run into `ModuleNotFound` errors when running cells within the notebooks it can be a sign that the notebooks are not using the correct version of python. To fix this close the notebook server, run the following, then restart the notebooks:

```
python -m ipykernel install --user
```

**Note: You may notice that each walkthrough notebook has two files with different extensions (.ipynb and .md). The files you want to be using with Jupyter are the .ipynb files as these are what runs the underlying Oqtant python code. The .md files are static markdown representations of the walkthrough notebooks that can be used as reference if needed. The .md files are safe to delete**

## Authentication

At the top of each walkthrough notebook you will see a step called `Authenticate with Oqtant`. This step is required for all notebook and client operations to ensure only authorized parties are accessing Oqtant.

This step will require that you already have an account created for Oqtant. If you have not done so yet visit https://oqtant.infleqtion.com and follow the registration steps to get set up.
