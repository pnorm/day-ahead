from datetime import date
from pytest import raises

from ..utils.data_query import PSEDataQuery, TGEDataQuery


def test_valid_pse_data_query():
    valid_date = date(2022, 1, 1)
    valid_feature = 'PL_GEN_WIATR'

    # Test valid PSEDataQuery instance
    pse_query = PSEDataQuery(current_date=valid_date, feature=valid_feature)
    assert pse_query.generate_url() == "https://www.pse.pl/getcsv/-/export/csv/PL_GEN_WIATR/data/20220101/unit/all"


def test_invalid_pse_data_query_date():
    invalid_date = date(2050, 1, 1)
    valid_feature = 'PL_GEN_WIATR'

    # Test invalid date
    with raises(ValueError, match=f"Date must be between 2013-01-01 and {date.today().isoformat()}"):
        PSEDataQuery(current_date=invalid_date, feature=valid_feature)


def test_invalid_pse_data_query_feature():
    valid_date = date(2022, 1, 1)
    invalid_feature = 'INVALID_FEATURE'

    # Test invalid feature
    with raises(ValueError, match="Invalid feature. Valid features are:"):
        PSEDataQuery(current_date=valid_date, feature=invalid_feature)


def test_valid_tge_data_query():
    valid_date = date(2022, 1, 1)

    # Test valid TGEDataQuery instance
    tge_query = TGEDataQuery(current_date=valid_date)
    assert tge_query.generate_url() == "https://tge.pl/energia-elektryczna-rdn?dateShow=01-01-2022"


def test_invalid_tge_data_query_date():
    invalid_date = date(2050, 1, 1)

    # Test invalid date
    with raises(ValueError, match="Date must not be greater than today. Given date: 2050-01-01"):
        TGEDataQuery(current_date=invalid_date)
