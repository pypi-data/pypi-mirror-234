import pytest

from tests.test_util.utils import query_test


# -------------------------------------------------------------------------------------------------------------------- #
#                                                     Value Factors                                                    #
# -------------------------------------------------------------------------------------------------------------------- #
def test_sales_related_factors(sales_related_factors, db_env):
    query_test(sales_related_factors, db_env)


def test_book_related_factors(book_related_factors, db_env):
    query_test(book_related_factors, db_env)


def test_debt_related_factor(debt_related_factor, db_env):
    query_test(debt_related_factor, db_env)


def test_earnings_related_factors(earnings_related_factors, db_env):
    query_test(earnings_related_factors, db_env)


def test_cash_flow_related_factors(cash_flow_related_factors, db_env):
    query_test(cash_flow_related_factors, db_env)


def test_yield_related_factors(yield_related_factors, db_env):
    query_test(yield_related_factors, db_env)


# # -------------------------------------------------------------------------------------------------------------------- #
# #                                                     Growth Factors                                                    #
# # -------------------------------------------------------------------------------------------------------------------- #
def test_growth_sales_related_factor(growth_sales_related_factor, db_env):
    query_test(growth_sales_related_factor, db_env)


def test_growth_debt_related_factor(growth_debt_related_factor, db_env):
    query_test(growth_debt_related_factor, db_env)


def test_growth_earnings_related_factor(growth_earnings_related_factor, db_env):
    query_test(growth_earnings_related_factor, db_env)


def test_growth_cash_flow_related_factors(growth_cash_flow_related_factors, db_env):
    query_test(growth_cash_flow_related_factors, db_env)


def test_growth_yield_related_factors(growth_yield_related_factors, db_env):
    query_test(growth_yield_related_factors, db_env)