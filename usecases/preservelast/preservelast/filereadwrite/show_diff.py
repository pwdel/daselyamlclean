import os
import subprocess
import tempfile

def show_diff(backup_file, updated_manifest_content):
    """
    Writes updated manifest content to a temporary file,
    compares it to the backup file, and prints the differences.
    
    Parameters:
        backup_file (str): Path to the backup file.
        updated_manifest_content (str): The updated manifest content as a string.
    """
    print("Showing diff and creating temporary file for updated manifest.")
    # Write the updated manifest content to a temporary file
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as tmp:
        tmp.write(updated_manifest_content)
        tmp_manifest_file = tmp.name

    # Run diff between the backup file and the temporary file
    diff_cmd = ["diff", backup_file, tmp_manifest_file]
    diff_result = subprocess.run(diff_cmd, capture_output=True, text=True)
    
    print("Diff between backup and updated manifest:")
    if diff_result.stdout:
        print(diff_result.stdout)
    else:
        print("No differences found.")

    # Optionally, delete the temporary file
    os.remove(tmp_manifest_file)
    print(f"Deleted temporary file: {tmp_manifest_file}")
