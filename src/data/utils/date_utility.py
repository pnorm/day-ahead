from datetime import date, datetime, timedelta
from typing import Optional, List, Union


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
    

def generate_date_list(from_date: date, to_date: date) -> List[str]:
    """
        Generate list of dates in a given range.
    """
    validate_date_range(from_date, to_date)

    date_list = []
    current_date = from_date
    while current_date <= to_date:
        date_list.append(current_date.strftime('%Y-%m-%d'))
        current_date += timedelta(days=1)

    return date_list


def generate_date_list_n_days_from_today(day_lag: int = 60) -> List[str]:
    """
        Generate list of dates, 60 dates back from today.
    """
    today = datetime.today()
    from_date = datetime.today() - timedelta(days=day_lag)

    date_list = generate_date_list(from_date=from_date, to_date=today)

    return date_list


def format_date(input_date: Union[date, str], date_format: str = "%Y-%m-%d") -> Union[str, date]:
    """
        Function which make switching between date and str objects easier.
    """
    if isinstance(input_date, date):
        return input_date.strftime(date_format)
    elif isinstance(input_date, str):
        return datetime.strptime(input_date, date_format).date()
    else:
        raise ValueError("Invalid input. Supported types are date and str.")