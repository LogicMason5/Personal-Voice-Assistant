from datetime import datetime


def get_date() -> str:
    """Return current date as string (e.g. 'Jan 26 2026')."""
    return datetime.now().strftime("%b %d %Y")


def get_time() -> str:
    """Return current time as string (e.g. '14:32:10')."""
    return datetime.now().strftime("%H:%M:%S")
