import pytest
import json
from sqlalchemy import update

from tests.test_util.dq_table import dataqueries


def update_dataquery(
    sales_related_factors,
    book_related_factors,
    debt_related_factor,
    earnings_related_factors,
    cash_flow_related_factors,
    yield_related_factors,
    growth_sales_related_factor,
    growth_debt_related_factor,
    growth_earnings_related_factor,
    growth_cash_flow_related_factors,
    growth_yield_related_factors,
    db_env
):
    engine = db_env

    with engine.connect() as con:
        for dq_name, dq in sales_related_factors.items():
            con.execute(update(dataqueries).where(dataqueries.c.dataqueryname == dq_name).values(dataquerybody = json.dumps(dq._query)))

        for dq_name, dq in book_related_factors.items():
            con.execute(update(dataqueries).where(dataqueries.c.dataqueryname == dq_name).values(dataquerybody = json.dumps(dq._query)))

        for dq_name, dq in debt_related_factor.items():
            con.execute(update(dataqueries).where(dataqueries.c.dataqueryname == dq_name).values(dataquerybody = json.dumps(dq._query)))

        for dq_name, dq in earnings_related_factors.items():
            con.execute(update(dataqueries).where(dataqueries.c.dataqueryname == dq_name).values(dataquerybody = json.dumps(dq._query)))

        for dq_name, dq in cash_flow_related_factors.items():
            con.execute(update(dataqueries).where(dataqueries.c.dataqueryname == dq_name).values(dataquerybody = json.dumps(dq._query)))

        for dq_name, dq in yield_related_factors.items():
            con.execute(update(dataqueries).where(dataqueries.c.dataqueryname == dq_name).values(dataquerybody = json.dumps(dq._query)))

        for dq_name, dq in growth_sales_related_factor.items():
            con.execute(update(dataqueries).where(dataqueries.c.dataqueryname == dq_name).values(dataquerybody = json.dumps(dq._query)))

        for dq_name, dq in growth_debt_related_factor.items():
            con.execute(update(dataqueries).where(dataqueries.c.dataqueryname == dq_name).values(dataquerybody = json.dumps(dq._query)))

        for dq_name, dq in growth_earnings_related_factor.items():
            con.execute(update(dataqueries).where(dataqueries.c.dataqueryname == dq_name).values(dataquerybody = json.dumps(dq._query)))

        for dq_name, dq in growth_cash_flow_related_factors.items():
            con.execute(update(dataqueries).where(dataqueries.c.dataqueryname == dq_name).values(dataquerybody = json.dumps(dq._query)))

        for dq_name, dq in growth_yield_related_factors.items():
            con.execute(update(dataqueries).where(dataqueries.c.dataqueryname == dq_name).values(dataquerybody = json.dumps(dq._query)))


def update_modelquery(
    tcmodel_quries,
    riskmodel_queires,
    db_env
):
    engine = db_env

    with engine.connect() as con:
        for mq_name, mq in tcmodel_quries.items():
            con.execute(update(dataqueries).where(dataqueries.c.dataqueryname == mq_name).values(dataquerybody = json.dumps(mq._query)))

        for rm_name, mq in riskmodel_queires.items():
            con.execute(update(dataqueries).where(dataqueries.c.dataqueryname == rm_name).values(dataquerybody = json.dumps(mq._query)))

