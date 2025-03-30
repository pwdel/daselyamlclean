from datetime import datetime
import re

def update_if_valid_date_or_suffix(date_str: str) -> str:
    """
    Checks if the given string is a valid date in YYYYMMDD format or a valid date with a suffix (YYYYMMDD-N).
    If valid, update the string as follows:
      - If the base date equals today's date:
           - If no suffix exists, append "-2".
           - If a suffix exists, increment the counter (e.g., -2 becomes -3).
      - If the base date is not today's date:
           - Replace the entire value with today's date (without any suffix).
    If the string is not a valid date (or date with suffix), return it unchanged.
    """
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