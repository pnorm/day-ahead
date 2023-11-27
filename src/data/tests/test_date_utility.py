from datetime import date
import pytest

from ..utils.date_utility import (
    validate_date_format,
    validate_date_range
)


def test_validate_date_format_valid():
    valid_date_str = "2023-11-25"
    result = validate_date_format(valid_date_str)
    assert result == date(2023, 11, 25)


def test_validate_date_format_invalid():
    invalid_date_str = "2023/11/25"
    with pytest.raises(ValueError):
        validate_date_format(invalid_date_str)


def test_validate_date_range_valid():
    from_date = "2023-11-25"
    to_date = "2023-11-30"
    validate_date_range(from_date, to_date)


def test_validate_date_range_invalid():
    from_date = "2023-12-01"
    to_date = "2023-11-30"
    with pytest.raises(ValueError):
        validate_date_range(from_date, to_date)