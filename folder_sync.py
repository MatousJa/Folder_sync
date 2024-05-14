import os
import shutil
import time
import hashlib
import argparse


def create_log_file(log_file):
    """Create the log file if it doesn't exist."""
    if not os.path.exists(log_file):
        with open(log_file, 'w') as log:
            log.write("Synchronization Log\n")


def synchronize_folders(source_folder, replica_folder, log_file, sync_interval):
    create_log_file(log_file)
    if not os.path.exists(replica_folder):
        os.makedirs(replica_folder)

    with open(log_file, 'a') as log:
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                source_file_path = os.path.join(root, file)
                replica_file_path = os.path.join(root.replace(source_folder, replica_folder), file)
                if not os.path.exists(replica_file_path):
                    shutil.copy2(source_file_path, replica_file_path)
                    log.write(f'Copied: {source_file_path} to {replica_file_path}\n')
                    print(f'Copied: {source_file_path} to {replica_file_path}')
                else:
                    source_hash = hashlib.md5(open(source_file_path, 'rb').read()).hexdigest()
                    replica_hash = hashlib.md5(open(replica_file_path, 'rb').read()).hexdigest()
                    if source_hash != replica_hash:
                        shutil.copy2(source_file_path, replica_file_path)
                        log.write(f'Updated: {source_file_path} to {replica_file_path}\n')
                        print(f'Updated: {source_file_path} to {replica_file_path}')

        for root, dirs, files in os.walk(replica_folder):
            for file in os.listdir(root):
                source_file_path = os.path.join(root.replace(replica_folder, source_folder), file)
                replica_file_path = os.path.join(root, file)
                if not os.path.exists(source_file_path):
                    os.remove(replica_file_path)
                    log.write(f'Removed: {replica_file_path}\n')
                    print(f'Removed: {replica_file_path}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to synchronize folders")
    parser.add_argument("source_folder", help="Path to the source folder")
    parser.add_argument("replica_folder", help="Path to the replica folder")
    parser.add_argument("log_file", help="Path to the log file")
    parser.add_argument("--interval", type=int, default=15, help="Synchronization interval in seconds (default: 15)")
    args = parser.parse_args()

    while True:
        synchronize_folders(args.source_folder, args.replica_folder, args.log_file, args.interval)
        time.sleep(args.interval)
