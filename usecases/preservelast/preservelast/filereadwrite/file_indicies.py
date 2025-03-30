def find_yaml_block_indices_for_all(
        file_path: str, 
        updated_data: dict[str, list[dict[str, str]]]
        ) -> tuple[list[str], list[tuple[str, int, int]]]:
    """
    Reads the file once and finds the start and end indices of the blocks corresponding to each target key 
    present in updated_data.
    
    For each key in updated_data (which should correspond to top-level YAML keys), the block is defined as 
    the lines following the key's definition (i.e. the line after "key:") until the next top-level key is 
    encountered (a non-empty line at column 0 that does not start with a dash ('-')) or until end-of-file.
    
    Args:
        file_path: Path to the YAML file.
        updated_data: A dictionary whose keys are the target keys to be located in the YAML file.
    
    Returns:
        A tuple containing:
          - A snapshot of the file as a list of strings.
          - A list of tuples, each tuple being (target_key, start_index, end_index) for that key.
    
    Raises:
        ValueError: If any target key from updated_data is not found in the file.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    blocks = []
    for key in updated_data.keys():
        # Locate the target key's definition.
        key_index = None
        for i, line in enumerate(lines):
            if line.lstrip() == line and line.startswith(key + ":"):
                key_index = i
                break
        if key_index is None:
            raise ValueError(f"Key '{key}' not found in file.")
        
        # The block starts immediately after the key definition.
        start_index = key_index + 1
        
        # Find the first line after the block that is a new top-level key.
        end_index = None
        for j in range(start_index, len(lines)):
            stripped = lines[j].lstrip()
            if lines[j].strip() and lines[j][0] != ' ' and not stripped.startswith('-'):
                end_index = j
                break
        if end_index is None:
            end_index = len(lines)
        
        blocks.append((key, start_index, end_index))
    
    return lines, blocks