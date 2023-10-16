from ksxt.market.manager import MarketManager


def test_fetch_nyse_market(market_manager: MarketManager):
    result = market_manager.nyse.all()

    import pandas as pd
    df = pd.DataFrame(result)

    assert len(df) > 0

def test_fetch_nasdaq_market(market_manager: MarketManager):
    result = market_manager.nasdaq.all()

    import pandas as pd
    df = pd.DataFrame(result)

    assert len(df) > 0

def test_fetch_amex_market(market_manager: MarketManager):
    result = market_manager.amex.all()

    import pandas as pd
    df = pd.DataFrame(result)

    assert len(df) > 0

def test_fetch_nyse_security(market_manager: MarketManager, nyse_stock_symbol):
    result = market_manager.stock(nyse_stock_symbol)

    assert result is not None
    
    from ksxt.market.us.nyse import NyseItem
    assert type(result) == NyseItem

def test_fetch_nasdaq_security(market_manager: MarketManager, nasdaq_stock_symbol):
    result = market_manager.stock(nasdaq_stock_symbol)

    assert result is not None
    
    from ksxt.market.us.nasdaq import NasdaqItem
    assert type(result) == NasdaqItem

def test_fetch_amex_security(market_manager: MarketManager, amex_stock_symbol):
    result = market_manager.stock(amex_stock_symbol)

    assert result is not None
    
    from ksxt.market.us.amex import AmexItem
    assert type(result) == AmexItem