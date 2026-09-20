# Code for syncing files between OneDrive and local disk, with a whitelist for specific subdirectories.
import argparse
import json
import os
import shutil

import logging as l

def load_config(path):
    """Load configuration from a JSON file."""
    with open(path, 'r') as f:
        return json.load(f)

def load(config, destination):
    """Send files from local path to destination path."""
    for subdir in config['whitelist_subdirs']:
        root = config['disk_root']
        local_path = os.path.join(root, subdir)
        dest_path = os.path.join(root, destination, subdir)
        l.msg(f"Sending {local_path} to {dest_path}")
        sync_dirs(local_path, dest_path)

def download(config, source):
    """Retrieve files from source path to local path."""
    for subdir in config['whitelist_subdirs']:
        root = config['disk_root']
        src_path = os.path.join(root, source, subdir)
        local_path = os.path.join(root, subdir)
        l.msg(f"Retrieving {src_path} to {local_path}")
        sync_dirs(src_path, local_path)

def sync_dirs(src, dest):
    for root, dirs, files in os.walk(src):

        rpath = os.path.relpath(root, src)
        droot = os.path.join(dest, rpath)

        os.makedirs(droot, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(droot, file)
            if not os.path.exists(dest_file):
                shutil.copy2(src_file, dest_file)
                l.msg(f"[COPIED] {src_file} to {dest_file}")
            elif compare_times(src_file, dest_file):
                shutil.copy2(src_file, dest_file)
                l.msg(f"[UPDATED] {src_file} to {dest_file}")
            else:
                l.msg(f"[SKIPPED] {src_file} is up to date.")

def compare_times(file1, file2):
    src_time = os.path.getmtime(file1)
    dest_time = os.path.getmtime(file2)
    return src_time > dest_time

def run(config, mode):
    """Run the sync operation based on the selected mode."""
    if mode == 'load':
        l.msg(f"Sending files from {config['disk_root']} to {config['onedrive_destiny']}... ")
        load(config, config['onedrive_destiny'])
    elif mode == 'download':
        l.msg(f"Retrieving files from {config['onedrive_destiny']} to {config['disk_root']}... ")
        download(config, config['onedrive_destiny'])
    else:
        l.error("Invalid mode selected. Choose 'load' or 'download'.")

if __name__ == "__main__":
    info = load_config('config.json')
    parser = argparse.ArgumentParser(description='Sync files between OneDrive and local disk.')
    parser.add_argument('--mode', type=str, choices=['load', 'download'], help='Select a mode: "load" to send files to OneDrive, "download" to retrieve files from OneDrive.')
    args = parser.parse_args()
    run(info, args.mode)