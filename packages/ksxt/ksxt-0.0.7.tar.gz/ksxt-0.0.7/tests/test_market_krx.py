from ksxt.market.manager import MarketManager


def test_fetch_kospi_market(market_manager: MarketManager):
    result = market_manager.kospi.all()

    import pandas as pd
    df = pd.DataFrame(result)
    
    assert len(df) > 0

def test_fetch_kosdaq_market(market_manager: MarketManager):
    result = market_manager.kosdaq.all()

    import pandas as pd
    df = pd.DataFrame(result)

    assert len(df) > 0

def test_fetch_kospi_security(market_manager: MarketManager, kospi_stock_symbol):
    result = market_manager.stock(kospi_stock_symbol)

    assert result is not None
    
    from ksxt.market.krx.kospi import KospiItem
    assert type(result) == KospiItem

def test_fetch_kosdaq_security(market_manager: MarketManager, kosdaq_stock_symbol):
    result = market_manager.stock(kosdaq_stock_symbol)

    assert result is not None
    
    from ksxt.market.krx.kosdaq import KosdaqItem
    assert type(result) == KosdaqItem