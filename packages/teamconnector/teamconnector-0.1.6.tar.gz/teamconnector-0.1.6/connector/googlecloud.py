import os
import subprocess

def sync_bucket(args):
    """Sync a local directory to a Google Cloud Storage bucket using gsutil."""
    try:
        drive_dir = f"{os.environ['CLOUD_ROOT']}"
    except KeyError:
        print('CLOUD_ROOT environment variable is not defined. Error...')
        exit()
    local_dir = f"{args.folder}/{args.subdir}/"
    drive_dir = f"{drive_dir}/{args.folder}/{args.subdir}/"
    if args.open:
        subprocess.call(
            ['open', 'https://console.cloud.google.com/storage/browser/' + drive_dir])
        return
    if args.list:
        cmd = ["gsutil", "ls", f"gs://{drive_dir}"]
        subprocess.run(cmd, check=True)
        return
    cmd = ["gsutil", "-m", "rsync", "-x", ".*\.ht|.*\.mt|.*\.vcf|.*\.log", "-r"]
    if args.debug:
        cmd.append("-n")
    if args.dir =='up':
        cmd.extend([local_dir, f"gs://{drive_dir}"])
    else:
        cmd.extend([f"gs://{drive_dir}", local_dir])
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)
