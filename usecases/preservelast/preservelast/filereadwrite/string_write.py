import re
from yaml_list_helpers.yaml_list_helpers import list_item_to_yaml_str
from yaml_dict_helpers.yaml_dict_helpers import dict_item_to_yaml_str

def replace_combined_updated_blocks(
    lines_snapshot: list[str],
    block_indicies: list[tuple[str, int, int]],
    combined_updated_data: dict[str, dict[str, list[dict[str, str]]]],
    keys_with_list_as_values_inserts: list[str],
    keys_with_dict_as_values_inserts: list[str],
    keys_with_dict_as_values_updates: list[str],
) -> str:
    """
    Processes both insert and update operations on a YAML file snapshot.
    
    For each target key in block_indicies:
      - If the key is in the "inserts" section, it inserts a new YAML block below the current block.
      - If the key is in the "updates" section, it replaces the block content (the line immediately following
        the key definition) with the updated YAML. For updates, the conversion function output (via dict_item_to_yaml_str)
        is assumed to include the key on its first line; that line is removed since the key is already present in the file.
    
    Args:
        lines_snapshot: List of file lines.
        block_indicies: List of tuples (target_key, start_index, end_index) for each target block.
        combined_updated_data: Nested dict with two keys:
            - "inserts": mapping target keys to new block data (list of dicts).
            - "updates": mapping target keys to new block data (list of dicts).
        keys_with_list_as_values_inserts: List of keys (for insert operations) to be formatted with list_item_to_yaml_str.
        keys_with_dict_as_values_inserts: List of keys (for insert operations) to be formatted with dict_item_to_yaml_str.
        keys_with_dict_as_values_updates: List of keys (for update operations) to be formatted with dict_item_to_yaml_str.
    
    Returns:
        A string representing the modified file content.
    """
    inserts_data = combined_updated_data.get("inserts", {})
    updates_data = combined_updated_data.get("updates", {})
    
    # Process blocks in descending order of end_index so that modifications don't affect earlier indices.
    sorted_blocks = sorted(block_indicies, key=lambda x: x[2], reverse=True)
    
    for target_key, start_index, end_index in sorted_blocks:
        # Handle insert operations.
        if target_key in inserts_data:
            block_data = inserts_data[target_key]
            if target_key in keys_with_list_as_values_inserts:
                yaml_str = list_item_to_yaml_str(block_data)
            elif target_key in keys_with_dict_as_values_inserts:
                yaml_str = dict_item_to_yaml_str({target_key: block_data})
            else:
                raise ValueError(
                    f"Key '{target_key}' not listed in keys_with_list_as_values_inserts or keys_with_dict_as_values_inserts."
                )
            if not yaml_str.endswith("\n"):
                yaml_str += "\n"
            yaml_str += " \n"
            # If there's an extra blank line at end_index, remove it.
            if end_index < len(lines_snapshot) and lines_snapshot[end_index].strip() == "":
                del lines_snapshot[end_index]
            # INSERT: add the new block below the existing block.
            lines_snapshot = lines_snapshot[:end_index-1] + [yaml_str] + lines_snapshot[end_index:]
        
        # Handle update operations.
        elif target_key in updates_data:
            block_data = updates_data[target_key]
            if target_key not in keys_with_dict_as_values_updates:
                raise ValueError(f"Key '{target_key}' not listed in keys_with_dict_as_values_updates.")
            # Generate the YAML block; this normally includes the key line.
            full_yaml_str = dict_item_to_yaml_str({target_key: block_data})
            # Split into lines and remove the first line (which duplicates the key already present in the file).
            yaml_lines = full_yaml_str.splitlines()
            if len(yaml_lines) < 2:
                raise ValueError(f"Not enough lines in YAML block for update for key '{target_key}'.")
            # Reassemble the YAML block without the key line.
            updated_yaml_str = "\n".join(yaml_lines[1:]) + "\n" + " \n"
            # For updates, we replace the line immediately following the key declaration.
            # Our block indices for updates should be (target_key, start_index, start_index+1),
            # so we update lines_snapshot[start_index].
            if start_index < len(lines_snapshot):
                lines_snapshot[start_index] = updated_yaml_str
            else:
                raise ValueError(f"Cannot update: target line index {start_index} out of range for key '{target_key}'.")
        else:
            raise ValueError(f"Key '{target_key}' not found in either inserts or updates data.")
    
    return "".join(lines_snapshot)

def replace_nulls_with_tilde_in_string(yaml_str: str) -> str:
    """
    Replaces YAML null values (i.e. "null", "Null", or "NULL") with the YAML null literal ~.
    This function removes any surrounding quotes so that the result is an unquoted tilde,
    per the YAML specification.
    
    Args:
        yaml_str: The YAML content as a string.
    
    Returns:
        The YAML string with all null-like values replaced with an unquoted ~.
    """
    # Replace quoted null values (handles both single and double quotes)
    yaml_str = re.sub(r'(:\s*)["\'](null|Null|NULL)["\']', r'\1~', yaml_str)
    # Replace unquoted null values (if they occur as standalone values)
    yaml_str = re.sub(r'(:\s*)(null|Null|NULL)\b', r'\1~', yaml_str)
    return yaml_str