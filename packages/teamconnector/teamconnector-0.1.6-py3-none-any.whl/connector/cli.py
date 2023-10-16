#!/usr/bin/env python3
"""
connector-cli (06 October 2023)
The Team Connector provides a short command-line interface (CLI) to connect
to the team's data and compute resources. Simple commands will sync and connect
files and results from your local computer to the team's cloud storage and 
the NYGC's compute cluster. 

For connector to work, the following environment variables must be set in your bash profile:
    export REMOTE_USER=tsingh
    #export REMOTE_HOST=login-singh.c.nygenome.org
    export REMOTE_HOST=nygc
    export GOOGLE_ROOT='$HOME/Library/CloudStorage/GoogleDrive-tsingh@nygenome.org'
    export MY_DRIVE="$GOOGLE_ROOT/My Drive"
    export SHARED_DRIVE="$GOOGLE_ROOT/Shared Drives"
    export ONE_DRIVE='$HOME/Library/CloudStorage/OneDrive-ColumbiaUniversityIrvingMedicalCenter'

example:
    $ tc config
    $ tc drive -ls
    $ tc drive -o -p aouexplore -s sample_qc
    $ tc -d gcp --dir down --subdir phenotypes

(C) 2023, TJ Singh lab (singhlab@nygenome.org)
Source: www.github.com/tjsinghlab/connector
License: GNU General Public License v3
"""

__author__ = "Tarjinder Singh"
__version__ = "0.1.5"
__license__ = "MIT"

import os
import argparse
from loguru import logger

from . import googledrive as gd
from . import googlecloud as gc
from . import remote as sl

def describe_env_variables(args):
    if 'REMOTE_USER' in os.environ:
        print(f"REMOTE_USER:   {os.environ['REMOTE_USER']}")
    if 'REMOTE_HOST' in os.environ:
        print(f"REMOTE_HOST:   {os.environ['REMOTE_HOST']}")
    if 'MY_DRIVE' in os.environ:
        print(f"MY_DRIVE:   {os.environ['MY_DRIVE']}")
    if 'SHARED_DRIVE' in os.environ:
        print(f"SHARED_DRIVE:    {os.environ['SHARED_DRIVE']}")
    if 'ONE_DRIVE' in os.environ:
        print(f"ONE_DRIVE:      {os.environ['ONE_DRIVE']}")
    if 'GOOGLE_ROOT' in os.environ:
        print(f"GOOGLE_ROOT:    {os.environ['GOOGLE_ROOT']}")
    if 'CLOUD_ROOT' in os.environ:
        print(f"CLOUD_ROOT:   {os.environ['CLOUD_ROOT']}")
    if 'PROJECT_ROOT' in os.environ:
        print(f"PROJECT_ROOT:   {os.environ['PROJECT_ROOT']}")

def main():
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug mode')
    subparsers = parser.add_subparsers(title='Commands', dest='command')
    parser.add_argument("--version", action="version",
                        version="%(prog)s (version {version})".format(version=__version__))

    #----
    sync_drive_parser = subparsers.add_parser(
        'config', help='Show relevant environment variables.')

    #----
    # Subparser for the sync_drive command to connect to Google Drive
    sync_drive_parser = subparsers.add_parser(
        'drive', help='Connect local directory to a Google Drive directory.')
    sync_drive_parser.add_argument(
        '-d', '--dir', choices=['up', 'down'], help='Choose direction to sync files, with up being local to remote (default: up)', default='up')
    sync_drive_parser.add_argument(
        '-p', '--project-name', type=str, help='The basename of the Google Drive project directory to sync to. Defaults to CLOUD_ROOT, then to the name of the current working directory.')
    sync_drive_parser.add_argument(
        '-f', '--folder', choices=['src', 'data'], help='Choose folder to sync (default: data)', default='data')
    sync_drive_parser.add_argument(
        '-s', '--subdir', type=str, help='The subdirectory within the local src/ or data/ directory to sync.', default='')
    sync_drive_parser.add_argument(
        '-t', '--target', choices=['personal', 'shared'], help='Choose which folder to share (default: shared)', default='shared')
    sync_drive_parser.add_argument('--max-size-mb', type=int, default=10,
                                   help='The maximum size of files to sync, in megabytes. Defaults to 10.')
    sync_drive_parser.add_argument('-o', '--open', action='store_true', help='Open remote drive.')
    sync_drive_parser.add_argument('-ls', '--list', action='store_true', help='List  drive files.')

    #----
    # Subparser for the sync_bucket command to connect to Google Cloud Storage
    sync_drive_parser = subparsers.add_parser(
        'gcp', help='Connect local directory to a Google Cloud Storage bucket.')
    sync_drive_parser.add_argument(
        '-d', '--dir', choices=['up', 'down'], help='Choose direction to sync files, with up being local to remote (default: down)', default='down')
    sync_drive_parser.add_argument(
        '-f', '--folder', choices=['src', 'data'], help='Choose folder to sync (default: data)', default='data')
    sync_drive_parser.add_argument(
        '-s', '--subdir', type=str, help='The subdirectory within the local src/ or data/ directory to sync.', default='')
    sync_drive_parser.add_argument('--max-size-mb', type=int, default=10,
                                help='The maximum size of files to sync, in megabytes. Defaults to 10.')
    sync_drive_parser.add_argument('-o', '--open', action='store_true', help='Open remote bucket.')
    sync_drive_parser.add_argument('-ls', '--list', action='store_true', help='List bucket files.')

    #----
    # Subparser for the sync_remote command to connect to a remote filesystem
    sync_remote_parser = subparsers.add_parser(
        'remote', help='Connect local directory to a remote cluster filesystem.')
    sync_remote_parser.add_argument(
        '-u', '--user', type=str, help='The username for the remote cluster.')
    sync_remote_parser.add_argument(
        '-H', '--host', type=str, help='The hostname for the remote cluster.')
    sync_remote_parser.add_argument(
        '-r', '--remote-dir', type=str, help='The remote directory to sync to.')
    sync_remote_parser.add_argument(
        '-d', '--dir', choices=['up', 'down'], help='Choose direction to sync files, with up being local to remote (default: up)', default='up')
    sync_remote_parser.add_argument(
        '-s', '--subdir', type=str, help='The subdirectory within the local src/ or data/ directory to sync.', default='')
    sync_remote_parser.add_argument(
        '-f', '--folder', choices=['src', 'data'], help='Choose folder to sync (default: data)', default='data')
    sync_remote_parser.add_argument('--max-size-mb', type=int, default=10,
                                help='The maximum size of files to sync, in megabytes. Defaults to 10.')
    sync_remote_parser.add_argument('-ls', '--list', action='store_true', help='List remote cluster files.')

    args = parser.parse_args()
    
    if args.command == 'config':
        describe_env_variables(args)
    elif args.command == 'drive':
        gd.sync_drive(args)
    elif args.command == 'gcp':
        gc.sync_bucket(args)
    elif args.command == 'remote':
        sl.sync_remote(args)
    else:
        parser.print_help()

    return(0)

