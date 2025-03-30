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