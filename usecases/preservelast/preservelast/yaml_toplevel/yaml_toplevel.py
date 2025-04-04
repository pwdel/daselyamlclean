from dasel.dasel_helpers import dasel_read
import re

def get_toplevel_inserts_keys(file_path):
    """
    Uses dasel_read on the provided file (with an empty selector)
    to extract the top-level keys from the YAML.
    For example, if the file contains:
      firstThing: null
      whateverThing: null
    then this function returns ["firstThing", "whateverThing"].
    """
    output = dasel_read(file_path, "")
    # Use regex to capture keys at the start of a line
    keys = re.findall(r'^(\S+):', output, re.MULTILINE)
    return keys

def determine_key_contents(manifest_file: str, keys: list[str]) -> tuple[list[str], list[str]]:
    """
    Determines which top-level keys in the given YAML file have list values and which have dict values.

    For each key in the provided list, this function uses dasel_read (with the key as the selector)
    to retrieve the content. It then inspects the content:
      - If the first non-whitespace character is '-', the key is assumed to contain a list.
      - Otherwise, it is assumed to contain a dict.

    Args:
        manifest_file: Path to the YAML manifest file.
        keys: A list of top-level keys to examine.

    Returns:
        A tuple (keys_with_list_as_values, keys_with_dict_as_values) where:
          - keys_with_list_as_values is a list of keys whose content starts with a dash (indicating a list).
          - keys_with_dict_as_values is a list of keys whose content does not start with a dash.
    """
    keys_with_list_as_values = []
    keys_with_dict_as_values = []

    for key in keys:
        # Retrieve the content for the key using dasel_read.
        content = dasel_read(manifest_file, key)
        # Check the first non-whitespace character.
        if content.lstrip().startswith('-'):
            keys_with_list_as_values.append(key)
        else:
            keys_with_dict_as_values.append(key)
    
    return keys_with_list_as_values, keys_with_dict_as_values