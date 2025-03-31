from yaml_list_helpers.yaml_list_helpers import list_item_to_yaml_str
from yaml_dict_helpers.yaml_dict_helpers import dict_item_to_yaml_str

def insert_updated_blocks(lines_snapshot: list[str],
                          block_indicies: list[tuple[str, int, int]],
                          updated_data: dict[str, list[dict[str, str]]]) -> str:
    """
    Inserts updated YAML blocks for each target key into the provided snapshot of file lines.

    For each tuple in block_indicies (of the form (target_key, start_index, end_index)):
      - Retrieves the updated block from updated_data[target_key].
      - Converts it into a YAML-formatted string using list_item_to_yaml_str.
      - Ensures it ends with a newline and appends an extra line with a single space.
      - Inserts it at the end_index of the block.

    Blocks are inserted in descending order of end_index so that subsequent insertions do not shift earlier indices.

    Args:
        lines_snapshot: A list of strings representing the file content.
        block_indicies: A list of tuples, each tuple is (target_key, start_index, end_index)
                        for a target block.
        updated_data: A dictionary mapping each target key to a list of dictionaries (the updated block).

    Returns:
        A string representing the modified file content with all new blocks inserted.
    """
    # Sort the block indices in descending order by end_index.
    sorted_blocks = sorted(block_indicies, key=lambda x: x[2], reverse=True)
    
    for block_info in sorted_blocks:
        target_key, start_index, end_index = block_info
        
        # Retrieve the updated list for the target key.
        if target_key not in updated_data:
            raise ValueError(f"Key '{target_key}' not found in updated_data.")
        input_list = updated_data[target_key]
        
        # Convert the input list into a YAML-formatted string.
        yaml_str = list_item_to_yaml_str(input_list)
        
        # Ensure the YAML string ends with a newline.
        if not yaml_str.endswith("\n"):
            yaml_str += "\n"
        
        # Append an extra line with a single space.
        yaml_str += " \n"
        
        # Optionally remove a blank line at the insertion point.
        if end_index < len(lines_snapshot) and lines_snapshot[end_index].strip() == "":
            del lines_snapshot[end_index]
        
        # Insert the YAML block at the end_index.
        lines_snapshot = lines_snapshot[:end_index-1] + [yaml_str] + lines_snapshot[end_index:]
    
    return "".join(lines_snapshot)

def insert_combined_updated_blocks(
    lines_snapshot: list[str],
    block_indicies: list[tuple[str, int, int]],
    updated_data: dict[str, list[dict[str, str]]],
    keys_with_list_as_values: list[str],
    keys_with_dict_as_values: list[str],
) -> str:
    """
    Inserts updated YAML blocks for each target key into the provided snapshot of file lines.
    
    For each tuple in block_indicies (of the form (target_key, start_index, end_index)):
      - Retrieves the updated block from updated_data[target_key].
      - Determines whether to format it as a list or dict based on the provided key lists.
      - Converts the block into a YAML-formatted string using:
            - list_item_to_yaml_str for keys in keys_with_list_as_values.
            - dict_item_to_yaml_str for keys in keys_with_dict_as_values (by passing {target_key: block_data}).
      - Ensures the YAML string ends with a newline and appends an extra line with a single space.
      - Inserts it at the end_index of the block.
      
    Blocks are inserted in descending order of end_index so that subsequent insertions do not shift earlier indices.
    
    Args:
        lines_snapshot: A list of strings representing the file content.
        block_indicies: A list of tuples, each tuple is (target_key, start_index, end_index) for a target block.
        updated_data: A dictionary mapping each target key to a list of dictionaries (the updated block).
        keys_with_list_as_values: A list of keys that should be formatted using list_item_to_yaml_str.
        keys_with_dict_as_values: A list of keys that should be formatted using dict_item_to_yaml_str.
    
    Returns:
        A string representing the modified file content with all new blocks inserted.
    """
    # Sort block indices in descending order by end_index.
    sorted_blocks = sorted(block_indicies, key=lambda x: x[2], reverse=True)
    
    for target_key, start_index, end_index in sorted_blocks:
        if target_key not in updated_data:
            raise ValueError(f"Key '{target_key}' not found in updated_data.")
        
        block_data = updated_data[target_key]
        
        # Choose the appropriate YAML conversion function based on the key.
        if target_key in keys_with_list_as_values:
            yaml_str = list_item_to_yaml_str(block_data)
        elif target_key in keys_with_dict_as_values:
            # Pass a dictionary with the top-level key if it's a dict block.
            yaml_str = dict_item_to_yaml_str({target_key: block_data})
        else:
            raise ValueError(
                f"Key '{target_key}' is not listed in keys_with_list_as_values or keys_with_dict_as_values."
            )
        
        # Ensure the YAML string ends with a newline.
        if not yaml_str.endswith("\n"):
            yaml_str += "\n"
        # Append an extra line with a single space.
        yaml_str += " \n"
        
        # Optionally remove a blank line at the insertion point.
        if end_index < len(lines_snapshot) and lines_snapshot[end_index].strip() == "":
            del lines_snapshot[end_index]
        
        # Insert the YAML block at the given end_index.
        lines_snapshot = lines_snapshot[:end_index-1] + [yaml_str] + lines_snapshot[end_index:]
    
    return "".join(lines_snapshot)
