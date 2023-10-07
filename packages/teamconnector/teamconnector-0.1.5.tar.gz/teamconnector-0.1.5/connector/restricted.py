#!/usr/bin/env python3
"""
from teamconnector.restricted import *
split_gz_file(tar_gz(folder_path, outdir='~/Downloads/'), n_chunks=10)

from teamconnector.restricted import *
untar_gz(merge_tar_files(split_file_pattern), '~/Downloads/')

sync_downloads(source_path, destination_path, debug=False)
"""

import os
import subprocess

def tar_gz(folder_path, archive_path=None, outdir=None):
    """Create a compressed archive of a folder using tar and gzip."""
    if archive_path is None:
        folder_name = os.path.basename(folder_path)
        archive_path = f"{folder_name}.tar.gz"
    if outdir is not None:
        archive_path = os.path.join(outdir, archive_path)
    cmd = ["tar", "-czvf", archive_path, folder_path]
    subprocess.run(cmd, check=True)
    return archive_path

def split_gz_file(tar_file_path, n_chunks):
    """Split a tarred file into n chunks using the split command."""
    subprocess.run(["split", "-n", str(n_chunks), "-d", tar_file_path, f"{tar_file_path}.part-"], check=True)
    return tar_file_path
    
def merge_tar_files(split_file_pattern, tar_file_path=None):
    """Merge split tar files back into a single tar file."""
    if tar_file_path is None:
        tar_file_path = os.path.splitext(split_file_pattern)[0]
    subprocess.run(["cat", f"{split_file_pattern}*",
                    ">", tar_file_path], check=True)
    return tar_file_path
    
def untar_gz(archive_path, extract_path="."):
    """Extract the contents of a compressed archive using tar."""
    cmd = ["tar", "-xzvf", archive_path, "-C", extract_path]
    subprocess.run(cmd, check=True)

def sync_download(source_path, destination_path, debug=False):
    """Copy the contents of a folder to another folder using rsync."""
    cmd = ["rsync", "-avhW"]
    if debug:
        cmd.append("--dry-run")
    cmd.extend([source_path, destination_path])
    subprocess.run(cmd, check=True)
