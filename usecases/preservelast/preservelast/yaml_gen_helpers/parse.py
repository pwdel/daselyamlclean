from typing import Any

def parse_yaml_value(raw_value: str) -> Any:
    """
    Parses a raw YAML value string and returns it as the proper type.
    
    If the value is enclosed in quotes (single or double), the quotes are removed
    and the result is returned as a string regardless of its content.
    
    If the value is not quoted and consists solely of digits, it is converted to an integer.
    Otherwise, it is returned as the stripped string.
    
    Args:
        raw_value: The raw value string extracted from the YAML (e.g. '"19700101"' or '19700101').
        
    Returns:
        The parsed value, either a string or an int.
    """
    value = raw_value.strip()
    # If value is enclosed in quotes, remove them and return as string.
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        return value[1:-1]
    # If not quoted and composed only of digits, return an int.
    elif value.isdigit():
        return int(value)
    else:
        return value
