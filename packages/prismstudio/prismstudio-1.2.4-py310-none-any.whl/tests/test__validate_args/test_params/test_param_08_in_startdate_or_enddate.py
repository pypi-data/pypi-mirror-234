import pytest

from prism._utils.validate_utils import _validate_args
from prism._utils.exceptions import PrismTypeError, PrismValueError


@_validate_args
def get_portfolio_of_startdate(portfolio,
                               startdate: str = None):
    return startdate


def test_startdate_param():
    # Valid Date
    assert get_portfolio_of_startdate(
        'S&P 500', startdate='2023-04-05') == '2023-04-05'
    assert get_portfolio_of_startdate(
        'S&P 500', startdate='2023-4-5') == '2023-4-5'
    assert get_portfolio_of_startdate(
        'S&P 500', startdate='2023-4') == '2023-4'
    assert get_portfolio_of_startdate(
        'S&P 500', startdate='2023') == '2023'
    assert get_portfolio_of_startdate('S&P 500', '2023.01.11') == '2023.01.11'

    # check type
    assert isinstance(get_portfolio_of_startdate('S&P 500', startdate='2023-04-05'), str)

    # BEGIN DATE
    assert get_portfolio_of_startdate('S&P 500', '1700-01-01') == '1700-01-01'

    # ACTIVE DATE
    assert get_portfolio_of_startdate('S&P 500', '2199-12-31') == '2199-12-31'

    # Looks wrong but valid case. (ex) '23-12-99' is 2099-12-23
    assert get_portfolio_of_startdate('S&P 500', '23-12-99') == '23-12-99'
    assert get_portfolio_of_startdate('S&P 500', '23.12.99') == '23.12.99'
    assert get_portfolio_of_startdate('S&P 500', '23 12 99') == '23 12 99'
    assert get_portfolio_of_startdate('S&P 500', '23/12/99') == '23/12/99'


def test_wrong_startdate_param():
    # out of valid date
    with pytest.raises(AssertionError):
        assert get_portfolio_of_startdate(
            'S&P 500', '2200-01-01') == '2200-01-01'

    with pytest.raises(AssertionError):
        assert get_portfolio_of_startdate(
            'S&P 500', '1699-12-31') == '1699-12-31'

    # pandas - out of bound
    with pytest.raises(PrismValueError):
        assert get_portfolio_of_startdate('S&P 500', '1600-12-01')

    with pytest.raises(PrismValueError):
        assert get_portfolio_of_startdate('S&P 500', '2300-01-01')

    # parsing error
    with pytest.raises(PrismValueError):
        assert get_portfolio_of_startdate(
            'S&P 500', '2023-12-32') == '2023-12-32'

    with pytest.raises(PrismValueError):
        assert get_portfolio_of_startdate(
            'S&P 500', '2023년 12월 20일') == '2023년 12월 20일'

    with pytest.raises(PrismValueError):
        assert get_portfolio_of_startdate(
            'S&P 500', '1699-12-31typo') == '1699-12-31typo'

    # wrong type
    with pytest.raises(PrismTypeError):
        assert get_portfolio_of_startdate('S&P 500', startdate=20220101)


@_validate_args
def get_portfolio_of_enddate(portfolio,
                             enddate: str = None):
    return enddate


def test_enddate_param():
    # Valid Date
    assert get_portfolio_of_enddate(
        'S&P 500', enddate='2023-04-05') == '2023-04-05'
    assert get_portfolio_of_enddate(
        'S&P 500', enddate='2023-4-5') == '2023-4-5'
    assert get_portfolio_of_enddate(
        'S&P 500', enddate='2023-4') == '2023-4'
    assert get_portfolio_of_enddate(
        'S&P 500', enddate='2023') == '2023'
    assert get_portfolio_of_enddate('S&P 500', '2023.01.11') == '2023.01.11'

    # check type
    assert isinstance(get_portfolio_of_enddate('S&P 500', enddate='2023-04-05'), str)

    # BEGIN DATE
    assert get_portfolio_of_enddate('S&P 500', '1700-01-01') == '1700-01-01'

    # ACTIVE DATE
    assert get_portfolio_of_enddate('S&P 500', '2199-12-31') == '2199-12-31'

    # Looks wrong but valid case. (ex) '23-12-99' is 2099-12-23
    assert get_portfolio_of_enddate('S&P 500', '23-12-99') == '23-12-99'
    assert get_portfolio_of_enddate('S&P 500', '23.12.99') == '23.12.99'
    assert get_portfolio_of_enddate('S&P 500', '23 12 99') == '23 12 99'
    assert get_portfolio_of_enddate('S&P 500', '23/12/99') == '23/12/99'


def test_wrong_enddate_param():
    # out of valid date
    with pytest.raises(AssertionError):
        assert get_portfolio_of_enddate(
            'S&P 500', '2200-01-01') == '2200-01-01'

    with pytest.raises(AssertionError):
        assert get_portfolio_of_enddate(
            'S&P 500', '1699-12-31') == '1699-12-31'

    # pandas - out of bound
    with pytest.raises(PrismValueError):
        assert get_portfolio_of_enddate('S&P 500', '1600-12-01')

    with pytest.raises(PrismValueError):
        assert get_portfolio_of_enddate('S&P 500', '2300-01-01')

    # parsing error
    with pytest.raises(PrismValueError):
        assert get_portfolio_of_enddate(
            'S&P 500', '2023-12-32') == '2023-12-32'

    with pytest.raises(PrismValueError):
        assert get_portfolio_of_enddate(
            'S&P 500', '2023년 12월 20일') == '2023년 12월 20일'

    with pytest.raises(PrismValueError):
        assert get_portfolio_of_enddate(
            'S&P 500', '1699-12-31typo') == '1699-12-31typo'

    # wrong type
    with pytest.raises(PrismTypeError):
        assert get_portfolio_of_enddate('S&P 500', enddate=20220101)


@_validate_args
def get_portfolio(portfolio,
                  startdate: str = None,
                  enddate: str = None):
    return startdate, enddate


def test_get_portfolio():
    assert get_portfolio(
        'S&P 500', startdate='2022-04-05', enddate='2023-04-05') == ('2022-04-05', '2023-04-05')

    assert get_portfolio('S&P 500', '1700-01-01',
                         '2199-12-31') == ('1700-01-01', '2199-12-31')


def test_get_portfolio_with_wrong_param():
    # out of valid date
    with pytest.raises(AssertionError):
        assert get_portfolio(
            'S&P 500', startdate='2023-01-01', enddate='2200-01-01') == ('2200-01-01', '2023-01-01')

    with pytest.raises(AssertionError):
        assert get_portfolio(
            'S&P 500', startdate='1699-12-31', enddate='2030-02-02') == ('1699-12-31', '2030-02-02')

    # pandas - out of bound
    with pytest.raises(PrismValueError):
        assert get_portfolio('S&P 500', startdate='1600-12-01',
                             enddate='2023-04-05') == ('1600-12-01', '2023-04-05')

    with pytest.raises(PrismValueError):
        assert get_portfolio('S&P 500', startdate='2023-04-05',
                             enddate='9999-01-01') == ('2023-04-05', '9999-01-01')

    with pytest.raises(PrismValueError):
        assert get_portfolio('S&P 500', startdate='1600-12-01',
                             enddate='9999-01-01') == ('1600-12-01', '9999-01-01')
