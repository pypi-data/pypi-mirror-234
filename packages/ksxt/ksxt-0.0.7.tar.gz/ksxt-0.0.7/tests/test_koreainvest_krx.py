import ksxt
from datetime import datetime

################################################################################################
# Public Feeder
################################################################################################
def test_fetch_market_kospi(koreainvest_exchange_dev: ksxt.KoreaInvest):
    result = koreainvest_exchange_dev.fetch_markets('kospi')

    assert result['response']['success'] == '0'
    assert len(result['symbol']) > 0

def test_fetch_market_kosdaq(koreainvest_exchange_dev: ksxt.KoreaInvest):
    result = koreainvest_exchange_dev.fetch_markets('kosdaq')

    assert result['response']['success'] == '0'
    assert len(result['symbol']) > 0

def test_fetch_security(koreainvest_exchange_dev: ksxt.KoreaInvest, krx_stock_symbol):
    result = koreainvest_exchange_dev.fetch_security(symbol=krx_stock_symbol)

    assert result['response']['success'] == '0'

def test_fetch_ticker(koreainvest_exchange_dev: ksxt.KoreaInvest, krx_stock_symbol):
    result = koreainvest_exchange_dev.fetch_ticker(symbol=krx_stock_symbol)
    
    assert result['response']['success'] == '0'
    assert float(result['price']) > 0

def test_fetch_historical_data_daily(koreainvest_exchange_dev: ksxt.KoreaInvest, krx_stock_symbol):
    time_frame = 'D'

    result = koreainvest_exchange_dev.fetch_historical_data(symbol=krx_stock_symbol,
                                                        time_frame=time_frame)
    
    assert result['response']['success'] == '0'
    assert len(result['history']) > 0

def test_fetch_historical_data_weekly(koreainvest_exchange_dev: ksxt.KoreaInvest, krx_stock_symbol):
    time_frame = 'W'

    result = koreainvest_exchange_dev.fetch_historical_data(symbol=krx_stock_symbol,
                                                        time_frame=time_frame)
    
    assert result['response']['success'] == '0'
    assert len(result['history']) > 0

def test_fetch_historical_data_monthly(koreainvest_exchange_dev: ksxt.KoreaInvest, krx_stock_symbol):
    time_frame = 'M'

    result = koreainvest_exchange_dev.fetch_historical_data(symbol=krx_stock_symbol,
                                                        time_frame=time_frame)
    
    assert result['response']['success'] == '0'
    assert len(result['history']) > 0

def test_fetch_historical_data_yearly(koreainvest_exchange_dev: ksxt.KoreaInvest, krx_stock_symbol):
    time_frame = 'Y'

    result = koreainvest_exchange_dev.fetch_historical_data(symbol=krx_stock_symbol,
                                                        time_frame=time_frame)
    
    assert result['response']['success'] == '0'
    assert len(result['history']) > 0

def test_fetch_is_holiday(koreainvest_exchange_dev: ksxt.KoreaInvest):
    holiday = datetime(2023, 8, 13)

    result = koreainvest_exchange_dev.fetch_is_holiday(holiday)
    if koreainvest_exchange_dev.is_dev:
        assert result['response']['success'] != '0'
    else:
        assert result == True

def test_fetch_is_not_holiday(koreainvest_exchange_dev: ksxt.KoreaInvest):
    holiday = datetime(2023, 8, 14)

    result = koreainvest_exchange_dev.fetch_is_holiday(holiday)

    if koreainvest_exchange_dev.is_dev:
        assert result['response']['success'] != '0'
    else:
        assert result == False


################################################################################################
# Private Feeder
################################################################################################
def test_fetch_balance(koreainvest_exchange_dev: ksxt.KoreaInvest, koreainvest_krx_accnum):
    result = koreainvest_exchange_dev.fetch_balance(acc_num=koreainvest_krx_accnum)

    assert result['response']['success'] == '0'

def test_fetch_cash(koreainvest_exchange_dev: ksxt.KoreaInvest, koreainvest_krx_accnum):
    result = koreainvest_exchange_dev.fetch_cash(acc_num=koreainvest_krx_accnum)

    assert result['response']['success'] == '0'

def test_fetch_screener_list(koreainvest_exchange_dev: ksxt.KoreaInvest, koreainvest_hts_user_id):
    result = koreainvest_exchange_dev.fetch_screener_list(user_id=koreainvest_hts_user_id)

    if koreainvest_exchange_dev.is_dev:
        assert result['response']['success'] == '-1'
    else:
        assert result['response']['success'] == '0'

def test_fetch_screener(koreainvest_exchange_dev: ksxt.KoreaInvest, koreainvest_hts_user_id):
    screen_id = '0'
    result = koreainvest_exchange_dev.fetch_screener(user_id=koreainvest_hts_user_id, screen_id=screen_id)

    if koreainvest_exchange_dev.is_dev:
        assert result['response']['success'] == '-1'
    else:
        assert result['response']['success'] == '0'

################################################################################################
# Broker
################################################################################################
def test_create_limit_buy_order(koreainvest_exchange_dev: ksxt.KoreaInvest, koreainvest_krx_accnum, krx_stock_symbol):
    ticket_type = 'entry_long'
    price = 35000
    qty = 2
    otype = 'limit'

    result = koreainvest_exchange_dev.create_order(acc_num=koreainvest_krx_accnum,
                                               symbol=krx_stock_symbol,
                                               ticket_type=ticket_type,
                                               price=price,
                                               qty=qty,
                                               otype=otype)
    
    assert result['response']['success'] == '0'

def test_create_market_buy_order(koreainvest_exchange_dev: ksxt.KoreaInvest, koreainvest_krx_accnum, krx_stock_symbol):
    ticket_type = 'entry_long'
    price = 35000
    qty = 2
    otype = 'market'

    result = koreainvest_exchange_dev.create_order(acc_num=koreainvest_krx_accnum,
                                               symbol=krx_stock_symbol,
                                               ticket_type=ticket_type,
                                               price=price,
                                               qty=qty,
                                               otype=otype)
    
    assert result['response']['success'] == '0'

def test_create_limit_sell_order(koreainvest_exchange_dev: ksxt.KoreaInvest, koreainvest_krx_accnum, krx_stock_symbol):
    ticket_type = 'exit_long'
    price = 35000
    qty = 2
    otype = 'limit'

    result = koreainvest_exchange_dev.create_order(acc_num=koreainvest_krx_accnum,
                                               symbol=krx_stock_symbol,
                                               ticket_type=ticket_type,
                                               price=price,
                                               qty=qty,
                                               otype=otype)
    
    assert result['response']['success'] == '0'

def test_create_market_sell_order(koreainvest_exchange_dev: ksxt.KoreaInvest, koreainvest_krx_accnum, krx_stock_symbol):
    ticket_type = 'exit_long'
    price = 35000
    qty = 2
    otype = 'market'

    result = koreainvest_exchange_dev.create_order(acc_num=koreainvest_krx_accnum,
                                               symbol=krx_stock_symbol,
                                               ticket_type=ticket_type,
                                               price=price,
                                               qty=qty,
                                               otype=otype)
    
    assert result['response']['success'] == '0'

def test_cancel_order(koreainvest_exchange_dev: ksxt.KoreaInvest, koreainvest_krx_accnum, krx_stock_symbol):
    ticket_type = 'entry_long'
    price = 30000
    qty = 2
    otype = 'limit'

    result = koreainvest_exchange_dev.create_order(acc_num=koreainvest_krx_accnum,
                                               symbol=krx_stock_symbol,
                                               ticket_type=ticket_type,
                                               price=price,
                                               qty=qty,
                                               otype=otype)
    
    order_id = result['order_id']

    result = koreainvest_exchange_dev.cancel_order(acc_num=koreainvest_krx_accnum,
                                               order_id=order_id)
    
    assert result['response']['success'] == '0'


def test_modify_order(koreainvest_exchange_dev: ksxt.KoreaInvest, koreainvest_krx_accnum, krx_stock_symbol):
    ticket_type = 'entry_long'
    price = 30000
    qty = 2
    otype = 'limit'

    result = koreainvest_exchange_dev.create_order(acc_num=koreainvest_krx_accnum,
                                               symbol=krx_stock_symbol,
                                               ticket_type=ticket_type,
                                               price=price,
                                               qty=qty,
                                               otype=otype)
    
    order_id = result['order_id']

    result = koreainvest_exchange_dev.modify_order(acc_num=koreainvest_krx_accnum,
                                               order_id=order_id,
                                               price=30500,
                                               qty=qty)
    
    assert result['response']['success'] == '0'

def test_fetch_open_order(koreainvest_exchange_dev: ksxt.KoreaInvest, koreainvest_krx_accnum):
    result = koreainvest_exchange_dev.fetch_open_order(acc_num=koreainvest_krx_accnum)

    assert result['response']['success'] == '0'

def test_fetch_closed_order(koreainvest_exchange_dev: ksxt.KoreaInvest, koreainvest_krx_accnum):
    result = koreainvest_exchange_dev.fetch_closed_order(acc_num=koreainvest_krx_accnum)

    assert result['response']['success'] == '0'