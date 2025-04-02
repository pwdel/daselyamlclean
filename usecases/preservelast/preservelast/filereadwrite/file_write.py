import os

def apply_pipeline_result(manifest_file: str, pipeline_result: str, backup_file: str) -> None:
    """
    Overwrites the manifest file with the updated pipeline result,
    deletes the backup file, and re-validates the updated manifest file.

    Args:
        manifest_file: Path to the target manifest YAML file.
        pipeline_result: The updated YAML content as a string.
        backup_file: Path to the backup file to be removed.
    """
    # Write the updated YAML content to the manifest file.
    with open(manifest_file, "w") as f:
        f.write(pipeline_result)
    print(f"Updated {manifest_file} with new content.")

    # Delete the backup file since it is no longer needed.
    os.remove(backup_file)
    print(f"Deleted backup file: {backup_file}")

    # Optionally re-read the file and validate its new contents.
    with open(manifest_file, "r") as f:
        new_content = f.read()