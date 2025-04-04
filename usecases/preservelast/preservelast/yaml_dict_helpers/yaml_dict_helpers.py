from typing import Dict, List
from dasel.dasel_helpers import dasel_read

def get_dict_item_key_values(manifest_file: str, keys: List[str]) -> Dict[str, List[Dict[str, str]]]:
    """
    For each key in keys (which correspond to dictionary items in the manifest file),
    constructs a selector to retrieve the dictionary, uses dasel_read to get its output
    (as a multi-line string), then splits that output into lines and parses each line into
    a dict with one key–value pair.
    
    Returns a dictionary mapping each key to a list of dictionaries (one per line).
    """
    result: Dict[str, List[Dict[str, str]]] = {}
    for key in keys:
        # For dictionary items, the selector is just the key name.
        selector: str = key
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

def dict_item_to_yaml_str(dict_data: dict[str, list[dict[str, str]]]) -> str:
    """
    Merges the one-key dictionaries for each key in the input dictionary and returns a YAML-formatted string.
    
    For example, given:
      {'pointStop': [{'markerPoint': '20250331'}]}
    this returns:
      pointStop:
        markerPoint: "20250331"
    
    Args:
        dict_data: A dictionary where each key maps to a list of one-key dictionaries.
    
    Returns:
        A string with YAML-formatted content.
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
            lines.append(f"  {subkey}: \"{value}\"")
    return "\n".join(lines)
