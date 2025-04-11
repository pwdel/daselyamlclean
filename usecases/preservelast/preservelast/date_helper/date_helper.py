from datetime import datetime
import re

def update_if_valid_date_or_suffix(date_str) -> str:
    """
    Checks if the given input is a valid date in YYYYMMDD format or a valid date with a suffix (YYYYMMDD-N).
    If valid, updates the string as follows:
      - If the base date equals today's date:
           - If no suffix exists, append "-2".
           - If a suffix exists, increment the counter (e.g., -2 becomes -3).
      - If the base date is not today's date:
           - Replace the entire value with today's date (without any suffix).
    If the input is not a string or is not a valid date (or date with suffix), returns it unchanged.
    """
    # If the input is not a string, return it unchanged.
    if not isinstance(date_str, str):
        return date_str

    import re
    from datetime import datetime

    pattern = re.compile(r"^(\d{8})(?:-(\d+))?$")
    match = pattern.match(date_str)
    if not match:
        return date_str

    base_date = match.group(1)
    suffix = match.group(2)

    try:
        datetime.strptime(base_date, "%Y%m%d")
    except ValueError:
        return date_str

    today_str = datetime.today().strftime("%Y%m%d")

    if base_date == today_str:
        if suffix is None:
            return f"{today_str}-2"
        else:
            try:
                counter = int(suffix)
            except ValueError:
                return date_str
            return f"{today_str}-{counter + 1}"
    else:
        return today_str

    
def update_dates_in_data(data: dict[str, list[dict[str, str]]]) -> dict[str, list[dict[str, str]]]:
    """
    Iterates over each key and nested dictionary in 'data' and updates any valid date or date-with-suffix
    field using update_if_valid_date_or_suffix. Returns the updated data structure.
    """
    updated_data = {}
    for outer_key, list_of_dicts in data.items():
        updated_list = []
        for inner_dict in list_of_dicts:
            updated_inner = {}
            for sub_key, value in inner_dict.items():
                updated_inner[sub_key] = update_if_valid_date_or_suffix(value)
            updated_list.append(updated_inner)
        updated_data[outer_key] = updated_list
    return updated_data