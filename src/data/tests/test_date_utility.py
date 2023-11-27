from datetime import date, timedelta
import pytest

from ..utils.date_utility import (
    validate_date_format,
    validate_date_range,
    generate_date_list,
    generate_date_list_n_days_from_today
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


def test_generate_date_list_valid_range():
    from_date_str = date(2023, 1, 1)
    to_date_str = date(2023, 1, 5)
    result = generate_date_list(from_date_str, to_date_str)
    expected_result = ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05']
    assert result == expected_result


def test_generate_date_list_single_day():
    from_date_str = date(2023, 2, 10)
    to_date_str = date(2023, 2, 10)
    result = generate_date_list(from_date_str, to_date_str)
    expected_result = ['2023-02-10']
    assert result == expected_result


def test_generate_date_list_invalid_range():
    from_date_str = date(2023, 3, 1)
    to_date_str = date(2023, 2, 28)
    with pytest.raises(ValueError):
        generate_date_list(from_date_str, to_date_str)