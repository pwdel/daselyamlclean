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

def list_item_to_yaml_str(list_item: list[dict[str, str]]) -> str:
    """
    Merges a list of one-key dictionaries into one mapping and returns a YAML-formatted string.
    For example, given:
      [{'timestampX': '20250329'}, {'timestampY': '20250329'}, {'anotherBlah': 'heyNowString'}, {'countyThing': '1'}, {'numberThing': '1000'}]
    this returns:
      - timestampX: "20250329"
        timestampY: "20250329"
        anotherBlah: "heyNowString"
        countyThing: "1"
        numberThing: "1000"
    """
    merged = {}
    for d in list_item:
        merged.update(d)
    
    lines = []
    first = True
    for key, value in merged.items():
        if first:
            lines.append(f"- {key}: \"{value}\"")
            first = False
        else:
            lines.append(f"  {key}: \"{value}\"")
    return "\n".join(lines)