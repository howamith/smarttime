import datetime
from typing import Tuple


def get_current_working_week() -> Tuple[datetime.datetime, datetime.datetime]:
    """Get the current working week."""
    now = datetime.datetime.utcnow()

    # If it's a weekend then skip to the following Monday, otherwise go back
    # to the previous monday.
    day_of_week = now.weekday()
    if day_of_week > 5:
        start = now + datetime.timedelta(days=7 - day_of_week)
    else:
        start = now - datetime.timedelta(days=day_of_week)

    return (
        start.replace(hour=0, minute=0),
        start.replace(day=start.day + 4, hour=23, minute=59, second=59),
    )


def get_weekday(date_time: datetime.datetime) -> str:
    """Convert a datetime into the day of the week."""
    return ["Mon", "Tues", "Wed", "Thur", "Fri"][date_time.weekday()]


def get_date_from_datetime(date_time: datetime.datetime) -> str:
    """Convert a datetime into a date stamp as `dd/mm/yyyy`."""
    return (
        f"{__padd(date_time.day)}/{__padd(date_time.month)}/{date_time.year}"
    )


def get_time_from_datetime(date_time: datetime.datetime) -> str:
    """Convert a datetime into a time stamp as `hh:mm`."""
    return f"{__padd(date_time.hour)}:{__padd(date_time.minute)}"


def format_timedelta(td: datetime.timedelta) -> str:
    """Build a nicely formatted string from a timedelta."""
    seconds = td.seconds
    if seconds < 60:
        return f"{seconds} seconds"

    minutes = int(seconds / 60)
    if minutes < 60:
        return f"{minutes} minutes"

    hours = int(minutes / 60)
    ret = f"{hours} hours"

    # Account for remaining minutes.
    if rem := minutes % 60:
        ret = f"{ret} and {int(rem)} minutes"

    return ret


def __padd(x: int) -> str:
    return str(x).rjust(2, "0")
