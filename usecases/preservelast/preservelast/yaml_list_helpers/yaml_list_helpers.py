from typing import Dict, List
from dasel.dasel_helpers import dasel_read, dasel_last_index_for_key

def get_last_list_index_for_key(manifest_file, keys):
    """
    For each key in the provided list, provide a dict showing the last index
    in the list under a given key.
    """
    counts = {}
    for key in keys:
        try:
            count_output = dasel_last_index_for_key(manifest_file, key)
            counts[key] = int(count_output) - 1
        except Exception as e:
            print(f"Error retrieving count for key '{key}': {e}")
            counts[key] = None
    return counts

def get_list_item_key_values(manifest_file: str, counts_dict: Dict[str, int]) -> Dict[str, List[Dict[str, str]]]:
    """
    For each key in counts_dict (which maps top-level keys to their last index),
    constructs a selector to get the last list item, uses dasel_read to retrieve
    its output (as a multi-line string), then splits that output into lines and
    parses each line into a dict with one key–value pair.
    
    Returns a dictionary mapping each key to a list of dictionaries (one per line).
    """
    result: Dict[str, List[Dict[str, str]]] = {}
    for key, last_index in counts_dict.items():
        selector: str = f"{key}.[{last_index}]"
        output: str = dasel_read(manifest_file, selector)
        line_dicts: List[Dict[str, str]] = []
        for line in output.splitlines():
            if line.strip():  # skip blank lines
                if ":" in line:
                    parts = line.split(":", 1)
                    k = parts[0].strip()
                    v = parts[1].strip()
                    # Remove surrounding quotes if present
                    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                        v = v[1:-1]
                    line_dicts.append({k: v})
        result[key] = line_dicts
    return result

def list_item_to_yaml_str(list_item: list[dict[str, any]]) -> str:
    """
    Converts a list of one-key dictionaries into a YAML formatted string while preserving order.
    If an entry’s value is an empty string, it is interpreted as a signal that this key is a container
    for subsequent key/value pairs. These following entries are then output as nested under that key.
    
    For example, given input:
      [
        {'timestampA': '20250402'},
        {'fizz': 'buzz'},
        {'another': ''},
        {'SET_VARIABLE': '100'},
        {'ANOTHER_VARIABLE': '2000'}
      ]
    
    This returns:
      - timestampA: "20250402"
        fizz: "buzz"
        another:
          SET_VARIABLE: "100"
          ANOTHER_VARIABLE: "2000"
    
    In contrast, a flat list (without an empty value marker) is output as individual key/value pairs.
    """
    lines = []
    i = 0
    first_line = True
    while i < len(list_item):
        # Each dictionary is assumed to have a single key-value pair.
        key, value = next(iter(list_item[i].items()))
        prefix = "- " if first_line else "  "
        first_line = False

        if value == "":
            # The empty string signals that this key is meant to be a container.
            lines.append(f"{prefix}{key}:")
            i += 1
            # Process subsequent items as nested entries until we hit another group marker (empty value)
            # or run out of items.
            while i < len(list_item):
                next_key, next_value = next(iter(list_item[i].items()))
                # If the next item also has an empty value, assume it's a new top-level group.
                if next_value == "":
                    break
                # Otherwise, output as nested (4-space indent)
                lines.append(f"    {next_key}: \"{next_value}\"")
                i += 1
            continue  # Continue outer loop without extra i increment.
        else:
            # Simple flat key/value pair.
            lines.append(f"{prefix}{key}: \"{value}\"")
        i += 1

    return "\n".join(lines)
