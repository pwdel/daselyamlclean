def find_yaml_block_indices_for_combined(
    file_path: str, 
    combined_updated_data: dict[str, dict[str, list[dict[str, str]]]]
) -> tuple[list[str], list[tuple[str, int, int]]]:
    """
    Reads the YAML file once and finds the start and end indices of the blocks corresponding to
    each target key present in the combined_updated_data. The combined_updated_data is expected to be a 
    nested dict with two keys: "inserts" and "updates". Keys under "inserts" use the standard logic,
    and keys under "updates" are assumed to correspond to a single line block that should be replaced.

    For each target key (the union of keys in combined_updated_data["inserts"] and combined_updated_data["updates"]):
      - Locate the key’s definition in the file.
      - The block starts immediately after the key definition (i.e. key_index + 1).
      - If the key is in the "updates" section, assume the block is exactly one line (end_index = start_index + 1).
      - If the key is in the "inserts" section, scan until the next top-level key is encountered 
        (a non-empty line that does not start with a space or a dash) or until end-of-file.

    Args:
        file_path: Path to the YAML file.
        combined_updated_data: A dictionary with two keys: "inserts" and "updates". Each maps a target key 
                               (str) to a list of one-key dictionaries.
    
    Returns:
        A tuple containing:
          - A list of the file’s lines (the snapshot).
          - A list of tuples in the form (target_key, start_index, end_index) for that key.
    
    Raises:
        ValueError: If any target key is not found in the file.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    blocks = []
    # Get the union of keys from both "inserts" and "updates"
    insert_keys = combined_updated_data.get("inserts", {}).keys()
    update_keys = combined_updated_data.get("updates", {}).keys()
    all_keys = set(insert_keys) | set(update_keys)
    
    for key in all_keys:
        # Locate the target key’s definition.
        key_index = None
        for i, line in enumerate(lines):
            # Look for a top-level key definition (line with no indentation that starts with "key:")
            if line.lstrip() == line and line.startswith(key + ":"):
                key_index = i
                break
        if key_index is None:
            raise ValueError(f"Key '{key}' not found in file.")
        
        # The block starts immediately after the key definition.
        start_index = key_index + 1
        
        # If the key is in the "updates" section, assume the block is a single line to be replaced.
        if key in update_keys:
            end_index = start_index + 1
        else:
            # For "inserts", determine the block end by scanning for the next top-level key.
            end_index = None
            for j in range(start_index, len(lines)):
                # A new key is assumed to start at column 0 (no leading whitespace) and is not a list item (not starting with '-')
                if lines[j].strip() and lines[j][0] != ' ' and not lines[j].lstrip().startswith('-'):
                    end_index = j
                    break
            if end_index is None:
                end_index = len(lines)
        
        blocks.append((key, start_index, end_index))
    
    return lines, blocks
