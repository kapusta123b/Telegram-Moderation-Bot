from datetime import datetime, timedelta

from loguru import logger

def parse_time(time_str: str) -> datetime | str | None:
    """
    Parses a time string (for example, '1m') and returns a datetime object or "permanent".
    Uses a dictionary to map suffixes (m, h, d, w) to timedelta arguments.
    """
    if time_str == "permanent":
        return "permanent"

    unit = time_str[
        -1
    ]  # Extract the last character as the time unit (e.g., 'm' from '10m')
    
    units = {
        "m": "minutes",
        "h": "hours",
        "d": "days",
        "w": "weeks",
    }  # Dictionary mapping suffixes to timedelta keywords

    if unit not in units:  # Return None if the unit is not supported
        return None

    try:
        value = int(
            time_str[:-1]
        )  # Extract the numeric value (everything except the last character) and convert to int
        # Return a future datetime based on the calculated interval
        return datetime.now() + timedelta(**{units[unit]: value})

    except ValueError:
        logger.warning(f"Failed to parse time string: {time_str}")

        return None