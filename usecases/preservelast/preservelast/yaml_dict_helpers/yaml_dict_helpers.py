from typing import Dict, List, Any
from dasel.dasel_helpers import dasel_read
from yaml_gen_helpers.parse import parse_yaml_value

def get_dict_item_key_values(manifest_file: str, keys: List[str]) -> Dict[str, List[Dict[str, Any]]]:
    """
    For each key in keys (which correspond to dictionary items in the manifest file),
    constructs a selector to retrieve the dictionary, uses dasel_read to get its output,
    then splits that output into lines and parses each line into a dict with one key–value pair.
    
    Numeric values will be converted to integers if they were not originally quoted.
    
    Returns a dictionary mapping each key to a list of dictionaries (one per line).
    """
    result: Dict[str, List[Dict[str, Any]]] = {}
    for key in keys:
        # For dictionary items, the selector is just the key name.
        selector: str = key
        output: str = dasel_read(manifest_file, selector)
        line_dicts: List[Dict[str, Any]] = []
        for line in output.splitlines():
            if line.strip():  # skip blank lines
                if ":" in line:
                    parts = line.split(":", 1)
                    k = parts[0].strip()
                    v = parts[1].strip()
                    # Use the helper to preserve type info:
                    parsed_value = parse_yaml_value(v)
                    line_dicts.append({k: parsed_value})
        result[key] = line_dicts
    return result

def dict_item_to_yaml_str(dict_data: dict[str, List[Dict[str, Any]]]) -> str:
    """
    Merges the one-key dictionaries for each key in the input dictionary and returns a YAML-formatted string.
    Numeric values are output unquoted; others are enclosed in quotes.
    """
    lines = []
    for key, list_of_dicts in dict_data.items():
        # Write the top-level key
        lines.append(f"{key}:")
        # Merge all one-key dictionaries into a single dictionary
        merged = {}
        for d in list_of_dicts:
            merged.update(d)
        # Write each key-value pair with two spaces of indentation
        for subkey, value in merged.items():
            if isinstance(value, (int, float)):
                # Write numeric types without quotes.
                lines.append(f"  {subkey}: {value}")
            else:
                # Write non-numeric types with quotes.
                lines.append(f"  {subkey}: \"{value}\"")
    return "\n".join(lines)