# teamconnector

## Overview

`teamconnector` is a command-line tool for interacting with various cloud storage and remote server platforms. It provides a simple and unified interface for managing files and directories across different platforms, making it easier to work with data in a distributed environment.

## Installation

Before installing `teamconnector`, make sure you create a Conda environment for your project.
If you have our team Makefile, you can use the `make create-env` command to create a Conda environment.

To install `teamconnector`, you can use pip:

`pip install teamconnector`

## Set up ENV variables

For connector to work, the following environment variables must be set in your bash profile (`~/.bash_profile` on Mac; `~/.bashrc` in Unix):

```
# Team Connector
export REMOTE_USER=<nygcuser>
export REMOTE_HOST=login-singh.c.nygenome.org
export GOOGLE_ROOT='$HOME/Library/CloudStorage/GoogleDrive-<user>@nygenome.org'
export MY_DRIVE="$GOOGLE_ROOT/My Drive"
export SHARED_DRIVE="$GOOGLE_ROOT/Shared Drives"

#export REMOTE_HOST=nygc
#export ONE_DRIVE='$HOME/Library/CloudStorage/OneDrive-ColumbiaUniversityIrvingMedicalCenter'
```

In your conda environment, you need to set:

CLOUD_ROOT: the base name of your Google bucket (`gpc_array` if `gs://gpc_array`)
PROJECT_ROOT: absolute path of your local project folder ('/User/<user>/projects/gpc_array')

```
conda env config vars set CLOUD_ROOT=gpc_array PROJECT_ROOT=`pwd`
```

Additionally, for `datatracker` to work in complicated situations,

TRACKER_PATH: the absolute path to the `db.json` file

`conda env config vars set TRACKER_PATH=$PROJECT_ROOT/db.json`

## Usage

`tc config` 

This command lists all the environment variables that are currently described in your `~/.bashrc` or Conda environment.

Run `tc -h` to see which environment variables need to be set in bash profile for the connector to work.

## local to Google Drive

`tc drive -ls`
This command lists all the files and folders in your Google Drive Shared directory.

`# tc drive -ls -t personal`
This command lists all the files and folders in your Google Drive "Personal" directory.

`tc drive -o -p aouexplore`
This command opens the "aouexplore" shared drive in your Google Drive.

`tc drive -o -p aouexplore -s sample_qc`
This command opens the "sample_qc" folder in the "aouexplore" shared drive in your Google Drive.

`tc --debug drive --dir up --subdir sample_qc`
This command uploads the "sample_qc" folder to the parent directory of your Google Drive root directory.

`tc drive --dir up --subdir sample_qc`
This command uploads the "sample_qc" folder to the parent directory of your Google Drive root directory.

## local to Google Cloud

Need to set `CLOUD_ROOT` within your Makefile and Conda environment.

`tc gcp -ls`
This command lists all the files and folders in your Google Cloud Storage bucket described in `CLOUD_ROOT`.


`tc -n gcp --dir down --subdir phenotypes`
This command downloads the "phenotypes" folder from your Google Cloud Storage bucket to your local machine.

# remote

`tc remote -r /gpfs/commons/groups/singh_lab/projects/gpc_array/ --dir down --subdir preprocessing`

This command downloads the "preprocessing" folder from the remote server at "/gpfs/commons/groups/singh_lab/projects/gpc_array/" to your local machine.

## Cite

## Maintainer

[Tarjinder Singh @ ts3475@cumc.columbia.edu](ts3475@cumc.columbia.edu)

## Acknowledgements

## Release Notes