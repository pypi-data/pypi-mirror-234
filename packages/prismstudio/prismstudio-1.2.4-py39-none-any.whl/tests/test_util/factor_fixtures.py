import pytest


@pytest.fixture
def commonly_used_dataitems(prism):
    mc = prism.market.market_cap(currency='trade')
    close = prism.market.close(adjustment='split', currency='trade').resample('D', 21)

    cash = (
        prism.financial.balance_sheet(dataitemid=100004, periodtype='Q', preliminary='keep', currency='trade')
            .fillna(method='ffill', n=4)
            .fillna(0)
            .resample('D', 365)
    )

    debt = (
        prism.financial.balance_sheet(dataitemid=100151, periodtype='Q', preliminary='keep', currency='trade')
            .fillna(method='ffill', n=4)
            .fillna(0)
            .resample('D', 365)
    )

    ev = prism.market.enterprise_value(currency='trade')
    return [mc, close, cash, debt, ev]


# -------------------------------------------------------------------------------------------------------------------- #
#                                                     Value Factors                                                    #
# -------------------------------------------------------------------------------------------------------------------- #

@pytest.fixture
def sales_related_factors(commonly_used_dataitems, prism):
    mc, _, _, _, ev = commonly_used_dataitems
    sales = (
        prism.financial.income_statement(dataitemid=100580, periodtype='LTM', preliminary='keep', currency='trade')
            .fillna(method='ffill', n=4)
            .resample('D', 365)
    )
    sales_fwd = (
        prism.estimate.consensus(dataitemid=200256, periodtype='NTM', periodout=0, currency='trade')
            .resample('D', 365)
    )

    #101. Sales to Price
    s2p = sales / mc

    #102. 5 year Average Sales to Price
    # s2p_5yr = s2p.n_periods_mean(5*365) #daily
    s2p_5yr = s2p.resample('M', 31).n_periods_mean(5*12) #monthly

    #103. Forward Sales to Price
    s2p_fwd = sales_fwd / mc

    #104. Sales to Enterprise Value(EV)
    s2ev = sales / ev

    #105. 5 year average Sales to Enterprise Value
    s2ev_5yr = (sales / ev).resample('BD', 10).n_periods_mean(5*260)
    #s2ev_5yr = s2ev.resample('M', 31).n_period_pct_mean(5*12) #monthly

    #106. Forward Sales to EV
    s2ev_fwd = sales_fwd / ev
    return {'s2p': s2p, 's2p_5yr': s2p_5yr, 's2p_fwd': s2p_fwd, 's2ev': s2ev, 's2ev_5yr': s2ev_5yr, 's2ev_fwd': s2ev_fwd}


@pytest.fixture
def book_related_factors(commonly_used_dataitems, prism):
    mc, _, _, _, _ = commonly_used_dataitems
    book = (
        prism.financial.balance_sheet(dataitemid=100075, periodtype='Q', preliminary='keep', currency='trade')
            .fillna(method='ffill', n=4)
            .resample('D', 365)
    )

    goodwill = (
        prism.financial.balance_sheet(dataitemid=100023, periodtype='Q', preliminary='keep', currency='trade')
            .fillna(method='ffill', n=4)
            .fillna(0)
            .resample('D', 365)
    )

    intangible = (
        prism.financial.balance_sheet(dataitemid=100024, periodtype='Q', preliminary='keep', currency='trade')
            .fillna(method='ffill', n=4)
            .fillna(0)
            .resample('D', 365)
    )

    book_tangible = book - goodwill - intangible

    #107. Book to Price
    b2p = book / mc

    #108. Tangible Book to Price
    b2p_tangible = book_tangible / mc

    #129. 12M Book to Price Z-Score
    b2p_z = b2p.n_periods_z_score(365)

    return {'b2p': b2p, 'b2p_tangible': b2p_tangible, 'b2p_z': b2p_z}


@pytest.fixture
def debt_related_factor(commonly_used_dataitems):
    _, _, cash, debt, ev = commonly_used_dataitems
    d2ev = (debt - cash) / ev
    return {'d2ev': d2ev}


@pytest.fixture
def earnings_related_factors(commonly_used_dataitems, prism):
    mc, _, _, _, ev = commonly_used_dataitems
    earnings = (
        prism.financial.income_statement(dataitemid=100647, periodtype='LTM', preliminary='keep', currency='trade')
            .fillna(method='ffill', n=4)
            .resample('D', 365)
    )

    earnings_fwd = (
        prism.estimate.consensus(dataitemid=200219, periodtype='NTM', periodout=0, currency='trade')
            .resample('D', 365)
    )

    ebidta = (
        prism.financial.income_statement(dataitemid=100723, periodtype='LTM', preliminary='keep', currency='trade')
            .fillna(method='ffill', n=4)
            .resample('D', 365)
    )

    ebidta_fwd = (
        prism.estimate.consensus(dataitemid=200099, periodtype='NTM', periodout=0, currency='trade')
            .resample('D', 365)
    )

    gp = (
        prism.financial.income_statement(dataitemid=100595, periodtype='LTM', preliminary='keep', currency='trade')
            .fillna(method='ffill', n=4)
            .resample('D', 365)
    )

    #110. Earnings to Price
    e2p = earnings / mc

    #111. 5 year Average Earnings to Price
    e2p_5yr = e2p.n_periods_mean(5*365) #daily
    #e2p_5yr = e2p.resample('M', 31).n_periods_mean(5*12) #monthly

    #112. Forward Earnings to Price
    e2p_fwd = earnings_fwd / mc

    #113. EBITDA to EV
    ebidta2ev = ebidta / ev

    #114. Forward BITDA to EV
    ebitda2ev_fwd = ebidta_fwd / ev

    #115. Gross Profit to Price
    gp2p = gp / mc

    #130. 12M Earnings to Price Z-Score
    e2p_z = e2p.n_periods_z_score(365)

    #131. 4w Forward Earnings to Price Change
    e2pchg_fwd_4w = (earnings_fwd / mc).n_periods_pct_change(30)

    #132. 8w Forward Earnings to Price Change
    e2pchg_fwd_8w = (earnings_fwd / mc).n_periods_pct_change(60)

    return {
        'e2p': e2p,
        'e2p_5yr': e2p_5yr,
        'e2p_fwd': e2p_fwd,
        'ebidta2ev': ebidta2ev,
        'ebitda2ev_fwd': ebitda2ev_fwd,
        'gp2p': gp2p,
        'e2p_z': e2p_z,
        'e2pchg_fwd_4w': e2pchg_fwd_4w,
        'e2pchg_fwd_8w': e2pchg_fwd_8w
    }


@pytest.fixture
def cash_flow_related_factors(commonly_used_dataitems, prism):
    mc, _, _, _, ev = commonly_used_dataitems
    cash_op = (
        prism.financial.cash_flow(dataitemid=100412, periodtype='LTM', preliminary='keep', currency='trade')
            .fillna(method='ffill', n=4)
            .resample('D', 365)
    )

    cash_op_fwd = (
        prism.estimate.consensus(dataitemid=200063, periodtype='NTM', periodout=0, currency='trade')
            .resample('D', 365)
    )

    cash_free = (
        prism.financial.cash_flow(dataitemid=100513, periodtype='LTM', preliminary='keep', currency='trade')
            .fillna(method='ffill', n=4)
            .resample('D', 365)
    )

    cash_free_fwd = (
        prism.estimate.consensus(dataitemid=200153, periodtype='NTM', periodout=0, currency='trade')
            .resample('D', 365)
    )

    #117. Operating Cash Flow to Price
    ocf2p = cash_op / mc

    #118. Foward Operating Cash Flow to Price
    ocf2p_fwd = cash_op_fwd / mc

    #119. Free Cash Flow to Price
    fcf2p = cash_free / mc

    #120. Forward Free Cash Flow to Price
    fcf2p_fwd = cash_free_fwd / mc

    #121. Operating Cash Flow to EV
    ocf2ev = cash_op / ev

    #122. Forward Operating Cash Flow to EV
    ocf2ev_fwd = cash_op_fwd / ev

    #123. Operating Cash Flow to EV
    fcf2ev = cash_free / ev

    #124. Forward Operating Cash Flow to EV
    fcf2ev_fwd = cash_free_fwd / ev

    return {
        'ocf2p': ocf2p,
        'ocf2p_fwd': ocf2p_fwd,
        'fcf2p': fcf2p,
        'fcf2p_fwd':fcf2p_fwd,
        'ocf2ev': ocf2ev,
        'ocf2ev_fwd': ocf2ev_fwd,
        'fcf2ev': fcf2ev,
        'fcf2ev_fwd': fcf2ev_fwd
    }


@pytest.fixture
def yield_related_factors(commonly_used_dataitems, prism):
    mc, close, _, _, _ = commonly_used_dataitems
    dps = (
        prism.financial.dps(dataitemid=100549, periodtype='LTM', preliminary='keep', currency='trade')
            .fillna(method='ffill', n=2)
            .fillna(0)
            .resample('D', 365)
    )

    dps_fwd = (
        prism.estimate.consensus(dataitemid=200069, periodtype='NTM', periodout=0, currency='trade')
            .fillna(0)
            .resample('D', 365)
    )

    buyback_comm = (
        prism.financial.cash_flow(dataitemid=100431, periodtype='LTM', preliminary='keep', currency='trade')
            .fillna(method='ffill', n=2).fillna(0) * -1
    )

    buyback_pref = (
        prism.financial.cash_flow(dataitemid=100433, periodtype='LTM', preliminary='keep', currency='trade')
            .fillna(method='ffill', n=2).fillna(0) * -1
    )

    div = (
        prism.financial.cash_flow(dataitemid=100438, periodtype='LTM', preliminary='keep', currency='trade')
            .fillna(method='ffill', n=2).fillna(0) * -1
    )


    #125. Dividend Yield
    dy = dps / close

    #126. Forward Dividend Yield
    dy_fwd = dps_fwd / close

    #127. Buyback Yield
    bby = (buyback_comm + buyback_pref ).resample('D', 365) / mc

    #127. Total Yield
    ty = (buyback_comm + buyback_pref + div).resample('D', 365) / mc

    return {
        'dy': dy,
        'dy_fwd': dy_fwd,
        'bby': bby,
        'ty': ty
    }



# -------------------------------------------------------------------------------------------------------------------- #
#                                                     Growth Factors                                                    #
# -------------------------------------------------------------------------------------------------------------------- #

@pytest.fixture
def growth_sales_related_factor(prism):
    sales = prism.financial.income_statement(dataitemid=100580, periodtype='LTM', preliminary='keep', currency='trade')
    sales_fwd = prism.estimate.consensus(dataitemid=200256, periodtype='NTM', periodout=0, currency='trade').resample('D', 365)
    sales_act = prism.estimate.actual(dataitemid=200032, periodtype='A', currency='trade').resample('D', 365)

    #201. 1 Year Sales Growth
    sg_1yr = sales.n_fiscal_quarters_pct_change(4, positive_denominator=True).fillna(method='ffill', n=4).resample('D', 365)

    #202. 3 Year Sales Growth
    sg_3yr = sales.n_fiscal_quarters_pct_change(12, positive_denominator=True).fillna(method='ffill', n=4).resample('D', 365)

    #204. Forward Sales Growth
    sg_fwd =  (sales_fwd / sales_act) - 1
    return {
        'sg_1yr': sg_1yr,
        'sg_3yr': sg_3yr,
        'sg_fwd': sg_fwd
    }


@pytest.fixture
def growth_debt_related_factor(prism):
    capex = prism.financial.cash_flow(dataitemid=100413, periodtype='LTM', preliminary='keep', currency='trade')

    #205. 1 Year Capital Expenditure Growth
    capex_1yr = capex.n_fiscal_quarters_pct_change(4).fillna(method='ffill', n=4).resample('D', 365)
    return {'capex_1yr': capex_1yr}


@pytest.fixture
def growth_earnings_related_factor(prism):
    earnings = prism.financial.income_statement(dataitemid=100647, periodtype='LTM', preliminary='keep', currency='trade')

    #206. 1 Year Earnings Growth
    eg_1yr = earnings.n_fiscal_quarters_pct_change(4, positive_denominator=True).fillna(method='ffill', n=4).resample('D', 365)

    #207. 3 Year Earnings Growth
    eg_3yr = earnings.n_fiscal_quarters_pct_change(12, positive_denominator=True).fillna(method='ffill', n=4).resample('D', 365)

    #208. 5 Year Earnings Growth
    eg_5yr = earnings.n_fiscal_quarters_pct_change(20, positive_denominator=True).fillna(method='ffill', n=4).resample('D', 365)

    return {'eg_1yr': eg_1yr, 'eg_3yr': eg_3yr, 'eg_5yr': eg_5yr}


@pytest.fixture
def growth_cash_flow_related_factors(prism):
    cash_op = prism.financial.cash_flow(dataitemid=100412, periodtype='LTM', preliminary='keep', currency='trade')
    cash_op_fwd = prism.estimate.consensus(dataitemid=200063, periodtype='NTM', periodout=0, currency='trade').resample('D', 365)
    cash_op_act = prism.estimate.actual(dataitemid=200005, periodtype='A', currency='trade').resample('D', 365)
    cash_free = prism.financial.cash_flow(dataitemid=100513, periodtype='LTM', preliminary='keep', currency='trade')
    cash_free_fwd = prism.estimate.consensus(dataitemid=200153, periodtype='NTM', periodout=0, currency='trade').resample('D', 365)
    cash_free_act = prism.estimate.actual(dataitemid=200005, periodtype='A', currency='trade').resample('D', 365)


    #217. 1 Year Operating Cash Flow Growth
    ocfg_1yr = cash_op.n_fiscal_quarters_pct_change(4, positive_denominator=True).fillna(method='ffill', n=4).resample('D', 365)

    #218. 3 Year Operating Cash Flow Growth
    ocfg_3yr = cash_op.n_fiscal_quarters_pct_change(12, positive_denominator=True).fillna(method='ffill', n=4).resample('D', 365)

    #219. 5 Year Operating Cash Flow Growth
    ocfg_5yr = cash_op.n_fiscal_quarters_pct_change(20, positive_denominator=True).fillna(method='ffill', n=4).resample('D', 365)

    #220. Operating Cash Flow Forward Growth
    ocfg_fwd = (cash_op_fwd / cash_op_act) - 1

    #221. 1 Year Free Cash Flow Growth
    fcfg_1yr = cash_free.n_fiscal_quarters_pct_change(4, positive_denominator=True).fillna(method='ffill', n=4).resample('D', 365)

    #222. 3 Year Free Cash Flow Growth
    fcfg_3yr = cash_free.n_fiscal_quarters_pct_change(12, positive_denominator=True).fillna(method='ffill', n=4).resample('D', 365)

    #223. 5 Year Free Cash Flow Growth
    fcfg_5yr = cash_free.n_fiscal_quarters_pct_change(20, positive_denominator=True).fillna(method='ffill', n=4).resample('D', 365)

    #224. Free Cash Flow Forward Growth
    fcfg_fwd = (cash_free_fwd / cash_free_act) - 1

    return {
        'ocfg_1yr': ocfg_1yr,
        'ocfg_3yr': ocfg_3yr,
        'ocfg_5yr': ocfg_5yr,
        'ocfg_fwd': ocfg_fwd,
        'fcfg_1yr': fcfg_1yr,
        'fcfg_3yr': fcfg_3yr,
        'fcfg_5yr': fcfg_5yr,
        'fcfg_fwd': fcfg_fwd
    }


@pytest.fixture
def growth_yield_related_factors(prism):
    dps = prism.financial.dps(dataitemid=100549, periodtype='LTM', preliminary='keep', currency='trade')
    dps_fwd = prism.estimate.consensus(dataitemid=200069, periodtype='NTM', periodout=0, currency='trade').fillna(0).resample('D', 365)
    dps_act = prism.estimate.actual(dataitemid=200006, periodtype='A', currency='trade').fillna(0).resample('D', 365)

    buyback_comm = prism.financial.cash_flow(dataitemid=100431, periodtype='LTM', preliminary='keep', currency='trade').fillna(0) * -1
    buyback_pref = prism.financial.cash_flow(dataitemid=100433, periodtype='LTM', preliminary='keep', currency='trade').fillna(0) * -1
    div = prism.financial.cash_flow(dataitemid=100438, periodtype='LTM', preliminary='keep', currency='trade').fillna(0) * -1

    #210. 1 Year Dividend Growth
    dg_1yr = dps.n_fiscal_quarters_pct_change(4, positive_denominator=True).fillna(method='ffill', n=2).resample('D', 365)

    #211. 3 Year Dividend Growth
    dg_3yr = dps.n_fiscal_quarters_pct_change(12, positive_denominator=True).fillna(method='ffill', n=2).resample('D', 365)

    #211. 5 Year Dividend Growth
    dg_5yr = dps.n_fiscal_quarters_pct_change(20, positive_denominator=True).fillna(method='ffill', n=2).resample('D', 365)

    #213. Dividend Forward Growth
    dg_fwd = (dps_fwd / dps_act) - 1

    #214. 1 Year Total Yield Growth
    yg_1yr = (buyback_comm + buyback_pref + div).n_fiscal_quarters_pct_change(4, positive_denominator=True).fillna(method='ffill', n=2).resample('D', 365)

    #215. 3 Year Total Yield Growth
    yg_3yr = (buyback_comm + buyback_pref + div).n_fiscal_quarters_pct_change(12, positive_denominator=True).fillna(method='ffill', n=2).resample('D', 365)

    #216. 5 Year Total Yield Growth
    yg_5yr = (buyback_comm + buyback_pref + div).n_fiscal_quarters_pct_change(20, positive_denominator=True).fillna(method='ffill', n=2).resample('D', 365)

    return {
        'dg_1yr': dg_1yr,
        'dg_3yr': dg_3yr,
        'dg_5yr': dg_5yr,
        'dg_fwd': dg_fwd,
        'yg_1yr': yg_1yr,
        'yg_3yr': yg_3yr,
        'yg_5yr': yg_5yr
    }

