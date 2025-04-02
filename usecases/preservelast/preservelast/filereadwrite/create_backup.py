import shutil
import os

def create_backup(manifest_file):
    """
    Creates a backup of the manifest file by appending '.backup' to its name.
    If a backup already exists, it is removed first.
    Returns the backup file path.
    """
    backup_file = manifest_file + ".backup"
    if os.path.exists(backup_file):
        os.remove(backup_file)
        print(f"Deleted existing backup file: {backup_file}")
    shutil.copy2(manifest_file, backup_file)
    print(f"Created backup file: {backup_file}")
    return backup_file
