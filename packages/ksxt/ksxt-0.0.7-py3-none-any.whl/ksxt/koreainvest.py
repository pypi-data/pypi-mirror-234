import json
from datetime import datetime, timedelta
import os
import pandas as pd
from typing import Any, Dict, Optional, Union

from ksxt.base.rest_exchange import RestExchange
from ksxt.base.types import Entry

from ksxt.market.manager import MarketManager


class ImplicitAPI:
    ################################################################################################
    # KRX API
    ################################################################################################
    fetchTicker = Entry('fetch_ticker_price', 'stock', 'feeder', 'public', 'GET', {})
    fetchOHLCV = Entry('fetch_ohlcv_stock', 'stock', 'feeder', 'public', 'GET', {})
    fetchIsHoliday = Entry('fetch_calendar_holiday', 'stock', 'feeder', 'public', 'GET', {})
    fetchScreenerList = Entry('fetch_screener_list', 'stock', 'feeder', 'private', 'GET', {})
    fetchScreener = Entry('fetch_screener', 'stock', 'feeder', 'private', 'GET', {})

    fetchBalance = Entry('fetch_balance', 'stock', 'broker', 'private', 'GET', {})
    fetchCash = Entry('fetch_cash', 'stock', 'broker', 'private', 'GET', {})
    sendOrderEntry = Entry('send_order_entry', 'stock', 'broker', 'private', 'POST', {})
    sendOrderExit = Entry('send_order_entry', 'stock', 'broker', 'private', 'POST', {})
    sendModifyOrder = Entry('send_modify_order', 'stock', 'broker', 'private', 'POST', {})
    sendCancelOrder = Entry('send_cancel_order', 'stock', 'broker', 'private', 'POST', {})

    fetchOpenedOrder = Entry('fetch_opened_order', 'stock', 'broker', 'private', 'GET', {})
    fetchClosedOrder = Entry('fetch_closed_order_short', 'stock', 'broker', 'private', 'GET', {})

    ################################################################################################
    # US API
    ################################################################################################
    fetchTickerForUS = Entry('fetch_ticker_price', 'oversea_stock', 'feeder', 'public', 'GET', {})
    fetchOHLCVforUS = Entry('fetch_ohlcv_stock', 'oversea_stock', 'feeder', 'public', 'GET', {})
    fetchScreenerListForUS = Entry('fetch_screener_list', 'oversea_stock', 'feeder', 'private', 'GET', {})
    fetchScreenerForUS = Entry('fetch_screener', 'oversea_stock', 'feeder', 'private', 'GET', {})

    fetchBalanceForUS = Entry('fetch_balance', 'oversea_stock', 'broker', 'private', 'GET', {})
    fetchCashForUS = Entry('fetch_cash', 'oversea_stock', 'broker', 'private', 'GET', {})
    
    sendOrderEntryForUS = Entry('send_order_entry', 'oversea_stock', 'broker', 'private', 'POST', {})
    sendOrderExitForUS = Entry('send_order_exit', 'oversea_stock', 'broker', 'private', 'POST', {})
    sendModifyOrderForUS = Entry('send_modify_order', 'oversea_stock', 'broker', 'private', 'POST', {})
    sendCancelOrderForUS = Entry('send_cancel_order', 'oversea_stock', 'broker', 'private', 'POST', {})

    fetchOpenedOrderForUS = Entry('fetch_opened_order', 'oversea_stock', 'broker', 'private', 'GET', {})
    fetchClosedOrderForUS = Entry('fetch_closed_order', 'oversea_stock', 'broker', 'private', 'GET', {})

class KoreaInvest(RestExchange, ImplicitAPI):
    def __init__(self, config: Dict=None) -> None:
        super().__init__(config=config)

    def describe(self) -> Dict:
        result = self.deep_extend(super(KoreaInvest, self).describe(), {
            'id': 'KIS',
            'name': 'KoreaInvestment',
            'countries': ['KR', 'US'],
            'version': 'v1',
            'rateLimit': 1000,
            'urls': {
                'logo': '',
                'api': {
                    'token': 'https://{hostname}/oauth2/tokenP',
                    'public': 'https://{hostname}',
                    'private': 'https://{hostname}',
                },
                'www': 'https://securities.koreainvestment.com',
                'doc': 'https://apiportal.koreainvestment.com/apiservice/oauth2#L_5c87ba63-740a-4166-93ac-803510bb9c02',
                'fees': '',
            },
        })

        return result
    
    # region _____
    def set_token(self):
        url = self.implode_hostname(self.urls['api']['token'], self.apis['rest']['hostname'])
        request_headers = self.prepare_request_headers()

        body = {
            "grant_type":"client_credentials",
            "appkey":self.open_key, 
            "appsecret":self.secret_key
        }

        body = json.dumps(body, separators=(',', ':'))

        res = self.fetch(url=url, method='POST', headers=request_headers, body=body)
        self.token = res['access_token']
        self.token_expired = res['access_token_token_expired']   

        import logging
        logging.info('set token')
        logging.info(self.token)
        logging.info(self.token_expired)

    def sign(self, path, market, module, api: Any = 'public', method='GET', headers: Optional[Any] = None, body: Optional[Any] = None, params: Optional[Dict] = {}, config={}):
        host_url = self.implode_hostname(self.urls['api'][api], self.apis[self.type]['hostname'])
        folder = self.apis[self.type][market][module]['foldername']
        destination = self.apis[self.type][market][module][path]['url']
        url = host_url + '/' + folder + '/' + self.version + '/' + destination

        tr_id = self.apis['rest'][market][module][path]['tr']
        if headers is None:
            headers = {}
            headers.update(
                {
                    "content-type":"application/json",
                    "authorization": f"Bearer {self.token}",
                    "appKey": self.open_key,
                    "appSecret": self.secret_key,
                    "tr_id": tr_id
                }
            )

        if method.upper() == 'POST':
            body = json.dumps(params)
            params = {}

        return {'url': url, 'method': method, 'headers': headers, 'body': body, 'params': params}
    # endregion ____

    # region public feeder
    @RestExchange.check_token
    def fetch_markets(self, market_name: str):
        db_path = os.path.join(os.getcwd(), f".ksxt-cache_market.{datetime.now().strftime('%Y%m%d')}.db")
        manager = MarketManager(db_path=db_path)
        manager._init()
        if market_name.lower() == 'kospi':
            result = manager.kospi.all()
            base_market = 'KRW'
        elif market_name.lower() == 'kosdaq':
            result = manager.kosdaq.all()
            base_market = 'KRW'
        elif market_name.lower() == 'nyse':
            result = manager.nyse.all()
            base_market = 'USD'
        elif market_name.lower() == 'nasdaq':
            result = manager.nasdaq.all()
            base_market = 'USD'
        elif market_name.lower() == 'amex':
            result = manager.amex.all()
            base_market = 'USD'
        else:
            return self.get_error_response(error_code='market_error', error_message=f'{market_name} market is not yet supported.')
        
        df = pd.DataFrame(result)
        
        return self.parse_market(response=df, base_market=base_market)
    
    def parse_market(self, response: pd.DataFrame, base_market: str= 'KRW'):
        result = self.get_common_successful_response(response=response)

        if base_market == 'KRW':
            result.update({
                # 종목 코드
                'symbol': response['mksc_shrn_iscd'],
                # 종목 이름
                'name': response['hts_kor_isnm'],
                # 거래소 정보 (KOSPI, KOSDAQ)
                'exchange': response['excd'],
                # 거래 통화
                'currency': response['curr'],
            })
        elif base_market == 'USD':
            result.update({
                # 종목 코드
                'symbol': response['symb'],
                # 종목 이름
                'name': response['enam'],
                # 거래소 정보 (NYSE, NASDAQ, AMEX)
                'exchange': response['excd'],
                # 거래 통화
                'currency': response['curr'],
            })
        else:
            return self.get_error_response(error_code='market_error', error_message=f'{base_market} market is not yet supported.')

        return result
    
    @RestExchange.check_token
    def fetch_security(self, symbol: str, base_market: str = 'KRW'):
        db_path = os.path.join(os.getcwd(), f".ksxt-cache_market.{datetime.now().strftime('%Y%m%d')}.db")
        manager = MarketManager(db_path=db_path)
        manager._init()

        response = manager.stock(symbol)

        return self.parse_security(response=response, base_market=base_market)
    
    def parse_security(self, response, base_market: str = 'KRW'):
        result = self.get_common_successful_response(response=response)

        if base_market == 'KRW':
            result.update({
                # 종목 코드
                'symbol': response.mksc_shrn_iscd,
                # 종목 이름
                'name': response.hts_kor_isnm,
                # 거래소 정보 (KOSPI, KOSDAQ)
                'exchange': response.excd,
                # 거래 통화
                'currency': response.curr,
            })
        elif base_market == 'USD':
            result.update({
                # 종목 코드
                'symbol': response.symb,
                # 종목 이름
                'name': response.enam,
                # 거래소 정보 (NYSE, NASDAQ, AMEX)
                'exchange': response.excd,
                # 거래 통화
                'currency': response.curr,
            })
        else:
            return self.get_error_response(error_code='market_error', error_message=f'{base_market} market is not yet supported.')
        
        return result
        

    @RestExchange.check_token
    def fetch_ticker(self, symbol: str, base_market: str= 'KRW'):
        if base_market == 'KRW':
            params = {
                "FID_COND_MRKT_DIV_CODE":"J",
                "FID_INPUT_ISCD": symbol
            }
            response = self.fetchTicker(self.extend(params))
        elif base_market == 'USD':
            market_code = self.get_market_code_in_feeder(symbol=symbol, base_market=base_market)
            params = {
                "AUTH": "",
                "EXCD": market_code,
                "SYMB": symbol
            }
            response = self.fetchTickerForUS(self.extend(params))
        else:
            return self.get_error_response(error_code='market_error', error_message=f'{base_market} market is not yet supported.')
        
        return self.parse_ticker(response=response, base_market=base_market)
    
    def parse_ticker(self, response: dict, base_market: str= 'KRW'):
        data = self.safe_value(response, 'output')
        if data is None:
            return response

        result = self.get_common_successful_response(response=response)

        if base_market == 'KRW':
            result.update({
                # 종목 코드
                'symbol': self.safe_value(data, 'stck_shrn_iscd'),
                # 현재가
                'price': self.safe_value(data, 'stck_prpr'),
            })
        elif base_market == 'USD':
            symbol = self.safe_value(data, 'rsym')
            symbol = symbol[4:]
            result.update({
                # 중목 코드
                'symbol': symbol,
                # 현재가
                'price': self.safe_value(data, 'last')
            })
        else:
            return self.get_error_response(error_code='market_error', error_message=f'{base_market} market is not yet supported.')
        
        return result
    
    @RestExchange.check_token
    def fetch_historical_data(self, symbol: str, time_frame: str, start: Optional[str] = None, end: Optional[str] = None, base_market: str= 'KRW'):
        limit = 100

        if end is None:
            end = KoreaInvest.now(base_market=base_market)

        if start is None:

            if time_frame == 'D':
                start = end - timedelta(days=limit)
            elif time_frame == 'W':
                start = end - timedelta(weeks=limit)
            elif time_frame == "M":
                start = end - timedelta(days=limit * 30)
            elif time_frame == 'Y':
                start = end - timedelta(days=limit * 365)
            else:
                start = end

        if base_market == 'KRW':
            params = {
                "FID_COND_MRKT_DIV_CODE": "J",
                "FID_INPUT_ISCD": symbol,
                "FID_INPUT_DATE_1": start.strftime('%Y%m%d'),
                "FID_INPUT_DATE_2": end.strftime('%Y%m%d'),
                "FID_PERIOD_DIV_CODE": time_frame,
                "FID_ORG_ADJ_PRC":"1",
            }

            response = self.fetchOHLCV(self.extend(params))
        elif base_market == 'USD':
            if time_frame == 'D':
                gubn = '0'
            elif time_frame == 'W':
                gubn = '1'
            elif time_frame == 'M':
                gubn = '2'
            else:
                return self.get_error_response(error_code='time frame error', error_message=f'{time_frame} time-frame is not supported.')
            
            market_code = self.get_market_code_in_feeder(symbol=symbol, base_market=base_market)

            params = {
                "AUTH": "",
                "EXCD": market_code,
                "SYMB": symbol,
                "GUBN": gubn,
                "BYMD": end.strftime('%Y%m%d'),
                "MODP": "1",
                "KEYB": ""
            }

            response = self.fetchOHLCVforUS(self.extend(params))
        else:
            return self.get_error_response(error_code='market_error', error_message=f'{base_market} market is not yet supported.')

        return self.parse_historical_data(response=response, base_market=base_market)
    
    def parse_historical_data(self, response: dict, base_market: str= 'KRW'):
        data = self.safe_value(response, 'output1')
        data_ohlcv = self.safe_value(response, 'output2')
        if data is None or data_ohlcv is None:
            return response
        
        result = self.get_common_successful_response(response=response)

        ohlcv = [self.parse_ohlcva(_, base_market) for _ in data_ohlcv]
        sorted_ohlcv = self.sort_by(ohlcv, 0)

        result.update({
            # 종목코드
            'symbol': self.safe_value(data, 'stck_shrn_iscd'),
            # ohlcv
            'history' : sorted_ohlcv
        })
    
        return result
    
    def parse_ohlcv(self, ohlcv, base_market: str= 'KRW'):
        # convert datetime to timestamp
        ts = self.safe_string(ohlcv, 'stck_bsop_date')

        if base_market == 'KRW':
            return [
                # timestamp
                ts,
                # open
                self.safe_number(ohlcv, 'stck_oprc'),
                # high
                self.safe_number(ohlcv, 'stck_hgpr'),
                # low
                self.safe_number(ohlcv, 'stck_lwpr'),
                # close
                self.safe_number(ohlcv, 'stck_clpr'),
                # volume
                self.safe_number(ohlcv, 'acml_vol'),
            ]
        elif base_market == 'USD':            
            return [
                # timestamp
                ts,
                # open
                self.safe_number(ohlcv, 'ovrs_nmix_oprc'),
                # high
                self.safe_number(ohlcv, 'ovrs_nmix_hgpr'),
                # low
                self.safe_number(ohlcv, 'ovrs_nmix_lwpr'),
                # close
                self.safe_number(ohlcv, 'ovrs_nmix_prpr'),
                # volume
                self.safe_number(ohlcv, 'acml_vol'),
            ]
        else:
            return []
    
    def parse_ohlcva(self, ohlcva, base_market: str= 'KRW'):
        if base_market == 'KRW':
            # convert datetime to timestamp
            ts = self.safe_string(ohlcva, 'stck_bsop_date')

            return [
                # timestamp
                ts,
                # open
                self.safe_number(ohlcva, 'stck_oprc'),
                # high
                self.safe_number(ohlcva, 'stck_hgpr'),
                # low
                self.safe_number(ohlcva, 'stck_lwpr'),
                # close
                self.safe_number(ohlcva, 'stck_clpr'),
                # volume
                self.safe_number(ohlcva, 'acml_vol'),
                # amount
                self.safe_number(ohlcva, 'acml_tr_pbmn')
            ]
        elif base_market == 'USD':
            # convert datetime to timestamp
            ts = self.safe_string(ohlcva, 'xymd')

            return [
                # timestamp
                ts,
                # open
                self.safe_number(ohlcva, 'open'),
                # high
                self.safe_number(ohlcva, 'high'),
                # low
                self.safe_number(ohlcva, 'low'),
                # close
                self.safe_number(ohlcva, 'clos'),
                # volume
                self.safe_number(ohlcva, 'tvol'),
                # amount
                self.safe_number(ohlcva, 'tamt')
            ]
        else:
            return []
    
    @RestExchange.check_token
    def fetch_is_holiday(self, dt: datetime, base_market: str= 'KRW'):
        params = {
            "BASS_DT": dt.strftime('%Y%m%d'),
            "CTX_AREA_NK": '',
            "CTX_AREA_FK": ''
        }

        if base_market == 'KRW':
            response = self.fetchIsHoliday(self.extend(params))
            if response['response']['success'] != '0':
                return response
            
            result = self.parse_is_holiday(response=response)

            return self.safe_boolean(result['holiday'], dt.strftime('%Y%m%d'))
        else:
            return self.get_error_response(error_code='market_error', error_message=f'{base_market} market is not yet supported.')
    
    def parse_is_holiday(self, response: dict):
        data = self.safe_value(response, 'output')
        if data is None:
            return response
        
        info = {}
        for _ in data:
            info.update(self._parse_is_holiday(_))
        
        return {
            'response': {
                # 성공 실패 여부
                'success' : self.safe_string(response, 'rt_cd'),
                # 응답코드
                'code': self.safe_string(response, 'msg_cd'),
                # 응답메세지
                'message': self.safe_string(response, 'msg1'),
            },
            # 원본 데이터
            'info': response,

            # 휴장일 정보
            'holiday': info
        }
    
    def _parse_is_holiday(self, info):
        return {
            # 날짜 (YYYYMMDD) : 개장일 여부 (Y/N)
            self.safe_string(info, 'bass_dt') : (not self.safe_boolean(info, 'opnd_yn')),
        }

    
    # endregion public feeder

    # region private feeder
    @RestExchange.check_token
    def fetch_balance(self, acc_num: str, base_market: str= 'KRW'):
        if base_market == 'KRW':
            params = {
                "CANO": acc_num[:8],
                "ACNT_PRDT_CD": acc_num[-2:],
                "AFHR_FLPR_YN": 'N',
                "OFL_YN": '',
                "INQR_DVSN": '01',
                "UNPR_DVSN": '01',
                "FUND_STTL_ICLD_YN": "N",
                "FNCG_AMT_AUTO_RDPT_YN": 'N',
                "PRCS_DVSN": '01',
                "CTX_AREA_FK100": '',
                "CTX_AREA_NK100": ''
            }

            response = self.fetchBalance(self.extend(params))
        elif base_market == 'USD':
            market_code = self.get_market_code_in_feeder(symbol='ALL', base_market=base_market)
            params = {
                "CANO": acc_num[:8],
                "ACNT_PRDT_CD": acc_num[-2:],
                "OVRS_EXCG_CD": market_code,
                "TR_CRCY_CD": 'USD',
                "CTX_AREA_FK200": '',
                "CTX_AREA_NK200": ''
            }

            response = self.fetchBalanceForUS(self.extend(params))
        else:
            return self.get_error_response(error_code='market_error', error_message=f'{base_market} market is not yet supported.')

        return self.parse_balance(response=response, base_market=base_market)
    
    def parse_balance(self, response: dict, base_market: str= 'KRW'):
        data = self.safe_value(response, 'output1')
        if data is None:
            return response
        
        result = self.get_common_successful_response(response=response)
        
        balances = [self._parse_balance(_, base_market) for _ in data]
        sorted_balances = self.sort_by(balances, 'symbol')

        result.update({
            'balance': sorted_balances
        })
        
        return result

    def _parse_balance(self, balance, base_market: str= 'KRW'):
        if base_market == 'KRW':
            total = self.safe_number(balance, 'hldg_qty')
            free = self.safe_number(balance, 'ord_psbl_qty')

            return {
                    'symbol': self.safe_string(balance, 'pdno'),
                    'name': self.safe_string(balance, 'prdt_name'),
                    'position': 'long',
                    'price': self.safe_number(balance, 'pchs_avg_pric'),
                    'qty':{
                        'total': total,
                        'free': free,
                        'used': total - free,
                    },
                    'amount': self.safe_number(balance, 'pchs_amt'),
            }
        elif base_market == 'USD':
            total = self.safe_number(balance, 'ovrs_cblc_qty')
            free = self.safe_number(balance, 'ord_psbl_qty')

            return {
                    'symbol': self.safe_string(balance, 'ovrs_pdno'),
                    'name': self.safe_string(balance, 'ovrs_item_name'),
                    'position': 'long',
                    'price': self.safe_number(balance, 'pchs_avg_pric'),
                    'qty':{
                        'total': total,
                        'free': free,
                        'used': total - free,
                    },
                    'amount': self.safe_number(balance, 'frcr_pchs_amt1'),
            }
        else:
            return self.get_error_response(error_code='market_error', error_message=f'{base_market} market is not yet supported.')
    
    @RestExchange.check_token
    def fetch_cash(self, acc_num: str, base_market: str= 'KRW'):
        if base_market == 'KRW':
            params = {
                "CANO": acc_num[:8],
                "ACNT_PRDT_CD": acc_num[-2:],
                "AFHR_FLPR_YN": 'N',
                "OFL_YN": '',
                "INQR_DVSN": '01',
                "UNPR_DVSN": '01',
                "FUND_STTL_ICLD_YN": "N",
                "FNCG_AMT_AUTO_RDPT_YN": 'N',
                "PRCS_DVSN": '01',
                "CTX_AREA_FK100": '',
                "CTX_AREA_NK100": ''
            }

            response = self.fetchCash(self.extend(params))
        elif base_market == 'USD':
            params = {
                "CANO": acc_num[:8],
                "ACNT_PRDT_CD": acc_num[-2:],
                # 01: 원화, 02: 외화
                "WCRC_FRCR_DVSN_CD": "02",
                "NATN_CD": "840",
                "TR_MKET_CD": "00",
                "INQR_DVSN_CD": "00"
            }

            response = self.fetchCashForUS(self.extend(params))
        else:
            return self.get_error_response(error_code='market_error', error_message=f'{base_market} market is not yet supported.')
        
        return self.parse_cash(response=response, base_market=base_market)
    
    def parse_cash(self, response:dict, base_market: str= 'KRW'):
        result = self.get_common_successful_response(response=response)
        data = self.safe_value(response, 'output2')
        if data is None:
            return response

        if base_market == 'KRW':
            data = data[0]

            result.update({
                # 정산금액 (KR: D+2 예수금)
                'cash': self.safe_number(data, 'prvs_rcdl_excc_amt')
            })
        elif base_market == 'USD':
            data = next(filter(lambda x: x['crcy_cd'] == base_market, data), None)
            if data is None:
                return response
            
            result.update({
                # 정산금액 (US: D+3 예수금)
                # TODO : 실전투자에서 D+3 예수금을 정상적으로 조회하는지 검증 필요
                'cash': self.safe_number(data, 'frcr_dncl_amt_2')
            })
        
        return result
    
    @RestExchange.check_token
    def fetch_screener_list(self, user_id, base_market: str= 'KRW'):
        params = {
            "USER_ID": user_id
        }

        if base_market == 'KRW':
            response = self.fetchScreenerList(self.extend(params))
            return response
        else:
            return self.get_error_response(error_code='market_error', error_message=f'{base_market} market is not yet supported.')
    
    @RestExchange.check_token
    def fetch_screener(self, user_id: str, screen_id: str, base_market: str= 'KRW'):
        if base_market == 'KRW':
            params = {
                "USER_ID": user_id,
                "SEQ" : screen_id
            }

            response = self.fetchScreener(self.extend(params))
        elif base_market == 'USD':
            market_code = self.get_market_code_in_feeder(symbol='ALL', base_market=base_market)
            params = {
                "AUTH": "",
                "EXCD": market_code,
                "CO_YN_PRICECUR": 1
            }
            response = self.fetchScreenerForUS(self.extend(params))

            # FIXME : when implement parsing logic remove below logic.
            response = self.get_common_successful_response(response=response)
        else:
            return self.get_error_response(error_code='market_error', error_message=f'{base_market} market is not yet supported.')
        
        # FIXME: screener parsing logic

        return response
    # endregion private feeder

    # region broker
    @RestExchange.check_token
    def create_order(self, acc_num: str, symbol: str, ticket_type: str, price: float, qty: float, otype: str, base_market: str= 'KRW'):
        if base_market == 'KRW':
            if otype.upper() == 'limit'.upper():
                order_dvsn = '00'
            elif otype.upper() == 'market'.upper():
                order_dvsn = '01'

            body = {
                "CANO": acc_num[:8],
                "ACNT_PRDT_CD": acc_num[-2:],
                "PDNO": symbol,
                "ORD_DVSN": order_dvsn,
                "ORD_QTY": str(qty),    # string type 으로 설정
                "ORD_UNPR": str(price), # string type 으로 설정
            }

            if ticket_type == 'entry_long':
                response = self.sendOrderEntry(self.extend(body))
            elif ticket_type == 'exit_long':
                response = self.sendOrderExit(self.extend(body))
            else:
                return
        elif base_market == 'USD':
            if otype.upper() == 'limit'.upper():
                order_dvsn = '00'
            elif otype.upper() == 'market'.upper():
                # 미국장은 시장가를 세부적으로 구분하여 지원함. -> 시장가 거래를 우선 지원하지 않는다.
                # https://apiportal.koreainvestment.com/apiservice/apiservice-overseas-stock#L_e4a7e5fd-eed5-4a85-93f0-f46b804dae5f
                return self.get_error_response(error_code='market_error', error_message=f'{base_market} market is not yet supported.')

            if ticket_type == 'entry_long':
                sell_type = ''
            elif ticket_type == 'exit_long':
                sell_type = '00'
            else:
                return

            market_code = self.get_market_code_in_broker(symbol=symbol, base_market=base_market)
            body = {
                "CANO": acc_num[:8],
                "ACNT_PRDT_CD": acc_num[-2:],
                "OVRS_EXCG_CD": market_code,
                "PDNO": symbol,
                "ORD_DVSN": order_dvsn,
                "ORD_QTY": str(qty),    # string type 으로 설정
                "SLL_TYPE": sell_type,
                "OVRS_ORD_UNPR": str(price), # string type 으로 설정
                "ORD_SVR_DVSN_CD": "0"
            }

            if ticket_type == 'entry_long':
                response = self.sendOrderEntryForUS(self.extend(body))
            elif ticket_type == 'exit_long':
                response = self.sendOrderExitForUS(self.extend(body))
            else:
                return
        else:
            return self.get_error_response(error_code='market_error', error_message=f'{base_market} market is not yet supported.')

        return self.parse_order_response(response=response, base_market=base_market)
    
    @RestExchange.check_token
    def cancel_order(self, acc_num: str, order_id: str, symbol: Optional[str] = '', qty: float = 0, *args, base_market: str= 'KRW'):
        if base_market == 'KRW':
            body = {
                "CANO": acc_num[:8],
                "ACNT_PRDT_CD": acc_num[-2:],
                "KRX_FWDG_ORD_ORGNO": "",
                "ORGN_ODNO":str(order_id),
                "RVSE_CNCL_DVSN_CD":"02",
                "ORD_DVSN":"00",
                "ORD_QTY":str(qty),
                "ORD_UNPR":str(0),
                "QTY_ALL_ORD_YN": "N",
            }

            # 수량 미입력시 전량 취소
            if qty == 0:
                body['QTY_ALL_ORD_YN'] = 'Y'

            response = self.sendCancelOrder(self.extend(body))
        elif base_market == 'USD':
            if qty == 0:
                return self.get_error_response(error_code='qty_error', error_message=f'{base_market} cancel order need to set qty.')
            
            market_code = self.get_market_code_in_broker(symbol=symbol, base_market=base_market)
            body = {
                "CANO": acc_num[:8],
                "ACNT_PRDT_CD": acc_num[-2:],
                "OVRS_EXCG_CD": market_code,
                "PDNO": symbol,
                "ORGN_ODNO":str(order_id),
                "RVSE_CNCL_DVSN_CD":"02",
                "ORD_QTY":str(qty),
                "OVRS_ORD_UNPR":str(0),
            }

            response = self.sendCancelOrderForUS(self.extend(body))
        else:
            return self.get_error_response(error_code='market_error', error_message=f'{base_market} market is not yet supported.')
        
        return self.parse_order_response(response=response, base_market=base_market)
    
    @RestExchange.check_token
    def modify_order(self, acc_num: str, order_id: str, price: float, qty: float, *args, symbol: Optional[str] = '', base_market: str= 'KRW'):
        if base_market == 'KRW':
            body = {
                "CANO": acc_num[:8],
                "ACNT_PRDT_CD": acc_num[-2:],
                "KRX_FWDG_ORD_ORGNO": "",
                "ORGN_ODNO":str(order_id),
                "RVSE_CNCL_DVSN_CD":"01",
                "ORD_DVSN":"00",
                "ORD_QTY":str(qty),
                "ORD_UNPR":str(price),
                "QTY_ALL_ORD_YN": "N",
            }

            # 수량 미입력시 전량 수정
            if qty == 0:
                body['QTY_ALL_ORD_YN'] = 'Y'

            response = self.sendModifyOrder(self.extend(body))
        elif base_market == 'USD':
            market_code = self.get_market_code_in_broker(symbol=symbol, base_market=base_market)
            body = {
                "CANO": acc_num[:8],
                "ACNT_PRDT_CD": acc_num[-2:],
                "OVRS_EXCG_CD": market_code,
                "PDNO": symbol,
                "ORGN_ODNO":str(order_id),
                "RVSE_CNCL_DVSN_CD":"01",
                "ORD_QTY":str(qty),
                "OVRS_ORD_UNPR":str(price),
            }

            response = self.sendModifyOrderForUS(self.extend(body))
        else:
            return self.get_error_response(error_code='market_error', error_message=f'{base_market} market is not yet supported.')
        
        return self.parse_order_response(response=response, base_market=base_market)
    
    def parse_order_response(self, response: dict, base_market: str='KRW'):
        result = self.get_common_successful_response(response=response)

        data = response['output']
        time = self.safe_string(data, 'ORD_TMD')
        today = datetime.today()
        dt = datetime.combine(today, datetime.strptime(time, '%H%M%S').time())

        result.update({
            # 주문 날짜 (YYYY-mm-DD HH:MM:SS)
            'datetime': datetime.strftime(dt, '%Y-%m-%d %H:%M:%S'),
            # 주문번호
            'order_id': self.safe_string(data, 'ODNO')    
        })

        return result
    
    @RestExchange.check_token
    def fetch_open_order(self, acc_num: str, symbol: Optional[str] = '', start: Optional[str] = None, end: Optional[str] = None, base_market: str= 'KRW'):
        if start is None:
            start = KoreaInvest.now(base_market=base_market)
        
        if end is None:
            end = KoreaInvest.now(base_market=base_market)

        if base_market == 'KRW':
            params = {
                'CANO': acc_num[:8],
                'ACNT_PRDT_CD': acc_num[-2:],
                'INQR_STRT_DT': start.strftime('%Y%m%d'),
                'INQR_END_DT' : end.strftime('%Y%m%d'),
                'SLL_BUY_DVSN_CD' : '00',
                'INQR_DVSN': '00',
                'PDNO': symbol,
                'CCLD_DVSN': '02',
                'ORD_GNO_BRNO': '',
                'ODNO': '',
                'INQR_DVSN_3': '00',
                'INQR_DVSN_1': '',
                'CTX_AREA_FK100': '',
                'CTX_AREA_NK100': ''
            }
            
            response = self.fetchOpenedOrder(self.extend(params))
        elif base_market == 'USD':
            market_code = self.get_market_code_in_broker('ALL', base_market=base_market)
            params = {
                'CANO': acc_num[:8],
                'ACNT_PRDT_CD': acc_num[-2:],
                'PDNO': symbol if symbol is not None else '%',
                'OVRS_EXCG_CD': market_code,
                'SORT_SQN': 'DS',   # DS : 정순, AS : 역순
                'CTX_AREA_NK200': '',
                'CTX_AREA_FK200': ''
            }
            
            response = self.fetchOpenedOrderForUS(self.extend(params))
        else:
            return self.get_error_response(error_code='market_error', error_message=f'{base_market} market is not yet supported.')

        return self.parse_open_order(response=response, base_market=base_market)
    
    def parse_open_order(self, response: dict, base_market: str='KRW'):
        if base_market == 'KRW':
            data = self.safe_value(response, 'output1')
        elif base_market == 'USD':
            data = self.safe_value(response, 'output')
        else:
            return self.get_error_response(error_code='market_error', error_message=f'{base_market} market is not yet supported.')
        
        if data is None:
            return response
        
        result = self.get_common_successful_response(response=response)

        orders = [self.parse_open_order_history(_, base_market) for _ in data]
        sorted_orders = self.sort_by(orders, 'datetime')

        result.update({
            # 주문 정보
            'orders': sorted_orders
        })

        return result

    def parse_open_order_history(self, order: dict, base_market: str='KRW'):
        date = self.safe_string(order, 'ord_dt')
        time = self.safe_string(order, 'ord_tmd')
        dt = datetime.combine(datetime.strptime(date, '%Y%m%d'), datetime.strptime(time, '%H%M%S').time())

        position = self.safe_string(order, 'sll_buy_dvsn_cd')
        if position == '01':
            position = 'exit_long'
        elif position == '02':
            position = 'entry_long'
        else:
            position = None

        result = {
            # 주문 날짜 (YYYY-mm-DD HH:MM:SS)
            'datetime': datetime.strftime(dt, '%Y-%m-%d %H:%M:%S'),
            # 주문번호
            'order_id': self.safe_string(order, 'odno'),
            # 원주문번호
            'org_order_id': self.safe_string(order, 'orgn_odno'),
            # long or short
            'position': position,
            # 종목코드
            'symbol': self.safe_string(order, 'pdno'),
        }

        if base_market == 'KRW':
            result.update({
                # 주문구분
                'order_type': self.safe_string(order, 'ord_dvsn_cd'),
                # 주문단가
                'price': self.safe_number(order, 'ord_unpr'),
                'qty': {
                    # 주문수량
                    'total': self.safe_number(order, 'ord_qty'),
                    # 체결수량
                    'used': self.safe_number(order, 'tot_ccld_qty'),
                    # 잔여수량
                    'free': self.safe_number(order, 'rmn_qty')
                }
            })
        elif base_market == 'USD':
            result.update({
                # 주문구분
                'order_type': 'limit',
                # 주문단가
                'price': self.safe_number(order, 'ft_ord_unpr3'),
                'qty': {
                    # 주문수량
                    'total': self.safe_number(order, 'ft_ord_qty'),
                    # 체결수량
                    'used': self.safe_number(order, 'ft_ccld_qty'),
                    # 잔여수량
                    'free': self.safe_number(order, 'nccs_qty')
                }
            })
        
        return result
    
    @RestExchange.check_token
    def fetch_closed_order(self, acc_num: str, symbol: Optional[str] = '', start: Optional[str] = None, end: Optional[str] = None, base_market: str= 'KRW'):
        if start is None:
            start = KoreaInvest.now(base_market=base_market)
        
        if end is None:
            end = KoreaInvest.now(base_market=base_market)

        if base_market == 'KRW':
            params = {
                'CANO': acc_num[:8],
                'ACNT_PRDT_CD': acc_num[-2:],
                'INQR_STRT_DT': start.strftime('%Y%m%d'),
                'INQR_END_DT' : end.strftime('%Y%m%d'),
                'SLL_BUY_DVSN_CD' : '00',
                'INQR_DVSN': '00',
                'PDNO': symbol,
                'CCLD_DVSN': '01',
                'ORD_GNO_BRNO': '',
                'ODNO': '',
                'INQR_DVSN_3': '00',
                'INQR_DVSN_1': '',
                'CTX_AREA_FK100': '',
                'CTX_AREA_NK100': ''
            }
            
            response = self.fetchClosedOrder(self.extend(params))
        elif base_market == 'USD':
            market_code = self.get_market_code_in_broker('ALL', base_market=base_market)
            params = {
                'CANO': acc_num[:8],
                'ACNT_PRDT_CD': acc_num[-2:],
                'PDNO': symbol if symbol is not None else '%',
                'ORD_STRT_DT': start.strftime('%Y%m%d'),
                'ORD_END_DT' : end.strftime('%Y%m%d'),
                'SLL_BUY_DVSN' : '00',
                'CCLD_NCCS_DVSN' : '01' if not self.is_dev else '00',
                'OVRS_EXCG_CD': market_code,
                'SORT_SQN': 'DS', # DS : 정순, AS : 역순
                'ORD_DT': '',
                'ORD_GNO_BRNO': '',
                'ODNO': '',
                'CTX_AREA_NK200': '',
                'CTX_AREA_FK200': ''
            }

            response = self.fetchClosedOrderForUS(self.extend(params))

        return self.parse_closed_order(response=response, base_market=base_market)
    
    def parse_closed_order(self, response: dict, base_market: str='KRW'):
        if base_market == 'KRW':
            data = self.safe_value(response, 'output1')
        elif base_market == 'USD':
            data = self.safe_value(response, 'output')
        else:
            return self.get_error_response(error_code='market_error', error_message=f'{base_market} market is not yet supported.')
        
        if data is None:
            return response
        
        result = self.get_common_successful_response(response=response)

        orders = [self.parse_closed_order_history(_, base_market) for _ in data]
        sorted_orders = self.sort_by(orders, 'datetime')

        result.update({
            # 주문 정보
            'orders': sorted_orders
        })

        return result
    
    def parse_closed_order_history(self, order: dict, base_market: str='KRW'):
        date = self.safe_string(order, 'ord_dt')
        time = self.safe_string(order, 'ord_tmd')
        dt = datetime.combine(datetime.strptime(date, '%Y%m%d'), datetime.strptime(time, '%H%M%S').time())

        position = self.safe_string(order, 'sll_buy_dvsn_cd')
        if position == '01':
            position = 'exit_long'
        elif position == '02':
            position = 'entry_long'
        else:
            position = None

        result = {
            # 주문 날짜 (YYYY-mm-DD HH:MM:SS)
            'datetime': datetime.strftime(dt, '%Y-%m-%d %H:%M:%S'),
            # 주문번호
            'order_id': self.safe_string(order, 'odno'),
            # 원주문번호
            'org_order_id': self.safe_string(order, 'orgn_odno'),
            # long or short
            'position': position,
            # 종목코드
            'symbol': self.safe_string(order, 'pdno'),
        }

        if base_market == 'KRW':
            result.update({
                # 주문구분
                'order_type': self.safe_string(order, 'ord_dvsn_cd'),
                # 주문단가
                'price': self.safe_number(order, 'ord_unpr'),
                # 체결수량
                'qty': self.safe_number(order, 'tot_ccld_qty')
            })

        elif base_market == 'USD':
            result.update({
                # 주문구분
                'order_type': 'limit',
                # 주문단가
                'price': self.safe_number(order, 'ft_ccld_unpr3'),
                # 체결수량
                'qty': self.safe_number(order, 'ft_ccld_qty')
            })

        return result
    
    # endregion broker

    def get_common_successful_response(self, response) -> dict:
        if type(response) == dict:
            return {
                'response': {
                    # 성공 실패 여부
                    'success' : self.safe_string(response, 'rt_cd'),
                    # 응답코드
                    'code': self.safe_string(response, 'msg_cd'),
                    # 응답메세지
                    'message': self.safe_string(response, 'msg1'),
                },
                # 원본 데이터
                'info': response,
            }
        else:
            return {
                'response': {
                    # 성공 실패 여부
                    'success' : '0',
                    # 응답코드
                    'code': 'success',
                    # 응답메세지
                    'message': '',
                },
                # 원본 데이터
                'info': response
            }

    def get_market_code_in_feeder(self, symbol: str, base_market: str= 'KRW'):
        if base_market == 'KRW':
            return ''
        elif base_market == 'USD':
            if symbol.upper() == 'ALL':
                return 'NASD'
            
            response = self.fetch_security(symbol=symbol, base_market=base_market)
            return response['exchange']
        else:
            return ''
        
    def get_market_code_in_broker(self, symbol: str, base_market: str= 'KRW'):
        if base_market == 'KRW':
            return ''
        elif base_market == 'USD':
            if symbol.upper() == 'ALL':
                return 'NASD'
            
            response = self.fetch_security(symbol=symbol, base_market=base_market)
            exname = response['exchange']
            if exname == 'NYS':
                return 'NYSE'
            elif exname == 'NAS':
                return 'NASD'
            elif exname == 'AMS':
                return 'AMEX'
            else:
                return ''
        else:            
            return ''
            
            