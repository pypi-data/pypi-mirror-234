import os
import subprocess

def sync_remote(args):
    """Sync a local directory to a remote cluster filesystem using rsync."""
    try:
        remote_dir = f"{os.environ['REMOTE_DIR']}" if args.remote_dir is None else args.remote_dir
    except KeyError:
        print('REMOTE_DIR environment variable is not defined. Error...')
        exit()
        
    try:
        user = f"{os.environ['REMOTE_USER']}" if args.user is None else args.user
        host = f"{os.environ['REMOTE_HOST']}" if args.host is None else args.host
    except:
        print('REMOTE_USER or REMOTE_HOST environment variable is not defined. Error...')
        exit()
        
    if args.list:
        ssh_cmd = ["ssh", f"{user}@{host}", f"ls -l {remote_dir}"]
        subprocess.run(ssh_cmd, check=True)
        return
    
    local_dir = f"{args.folder}/{args.subdir}/"
    remote_dir = f"{user}@{host}:{remote_dir}/{args.folder}/{args.subdir}/"
    
    cmd = ["rsync", "-avhW"]
    includes = ["--include=*.tsv", "--include=*.csv",
                "--include=*.txt", "--include=*.xlsx", "--include=*/"]
    excludes = ["--exclude=*"]
    
    max_size = f"--max-size={args.max_size_mb}mb"
    if args.debug:
        cmd.append("--dry-run")
    cmd = cmd + includes + excludes + [max_size]
    if args.dir == 'up':
        cmd.extend([local_dir, remote_dir])
    else:
        cmd.extend([remote_dir, local_dir])
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)
