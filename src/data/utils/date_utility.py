from datetime import date, datetime, timedelta
from typing import Optional


def validate_date_format(s: str) -> Optional[date]:
    """
        Validate if date is in isoformat (YYYY-MM-DD).
    """
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD.")
    
def validate_date_range(from_date: date, to_date: date):
    """
        Check if from_date is before to_date.
    """
    if from_date > to_date:
        raise ValueError("Invalid date range. 'from_date' must be before or equal to 'to_date'.")
    
