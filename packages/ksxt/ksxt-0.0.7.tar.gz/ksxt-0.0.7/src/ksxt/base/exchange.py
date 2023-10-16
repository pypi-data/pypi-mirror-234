import collections
from distutils.util import strtobool
import json
from datetime import datetime
import pytz
from typing import Dict, Optional

from requests import Session

from ksxt.base.types import IndexType


class Exchange:
    id = None
    name = None
    version = None
    is_dev = False

    session = None
    timeout = 10000 # milliseconds = seconds * 1000

    required_credentials = {
        'open_key': False,
        'secret_key': False,
        'uid': False,
        'login': False,
        'password': False,
        'token': False
    }

    def __init__(self):
        if not self.session:
            self.session = Session()

    def __del__(self):
        if self.session:
            try:
                self.session.close()
            except Exception as e:
                pass

    def __str__(self):
        return self.name

    # region public feeder
    def fetch_markets(self, market_name: str):
        """
        Market 정보 조회

        Args:
            market_name (str, optional): Market 구분 코드.
        """
        pass

    def parse_market(self, response: dict, base_market: str= 'KRW'):
        return {
            'response': {
                # 성공 실패 여부
                'success' : 0,
                # 응답코드
                'code': '',
                # 응답메세지
                'message': '',
            },
            # 원본 데이터
            'info': response,

            # 종목 코드
            'symbol': self.safe_value(response, ''),
            # 종목 이름
            'name': self.safe_value(response, ''),
            # 거래소 정보 (KOSPI, KOSDAQ, NYSE, NASDAQ, AMEX, .....)
            'exchange': self.safe_value(response, ''),
            # 거래 통화
            'currency': self.safe_value(response, ''),
        }
    
    def fetch_security(self, symbol: str, base_market: str = 'KRW'):
        """
        종목 정보 조회

        Args:
            symbol (str): 종목코드
            base_market (str, optional): Market 구분 코드. Defaults to 'KRW'.
        """
        pass

    def parse_security(self, response, base_market: str = 'KRW'):
        return {
            'response': {
                # 성공 실패 여부
                'success' : 0,
                # 응답코드
                'code': '',
                # 응답메세지
                'message': '',
            },
            # 원본 데이터
            'info': response,

            # 종목 코드
            'symbol': self.safe_value(response, ''),
            # 종목 이름
            'name': self.safe_value(response, ''),
            # 거래소 정보 (KOSPI, KOSDAQ, NYSE, NASDAQ, AMEX, .....)
            'exchange': self.safe_value(response, ''),
            # 거래 통화
            'currency': self.safe_value(response, ''),
        }
    
    def fetch_ticker(self, symbol: str, base_market: str= 'KRW'):
        """
        시세 정보 조회

        Args:
            symbol (str): 종목코드
            base_market (str, optional): Market 구분 코드. Defaults to 'KRW'.
        """
        pass

    def parse_ticker(self, response: dict, base_market: str= 'KRW'):
        return {
            'response': {
                # 성공 실패 여부
                'success' : 0,
                # 응답코드
                'code': '',
                # 응답메세지
                'message': '',
            },
            # 원본 데이터
            'info': response,
            
            # 종목 코드
            'symbol': self.safe_value(response, ''),
            # 현재가
            'price': self.safe_value(response, ''),
        }
    
    def fetch_historical_data(self, symbol: str, time_frame: str, start: Optional[str] = None, end: Optional[str] = None, base_market: str= 'KRW'):
        """
        과거 봉 정보 조회

        Args:
            symbol (str): 종목코드
            time_frame (str): 봉조회기준
            start (Optional[str], optional): 조회 시작일. Defaults to None.
            end (Optional[str], optional): 조회 종료일. Defaults to None.
            base_market (str, optional): Market 구분 코드. Defaults to 'KRW'.
        """
        pass

    def parse_historical_data(self, response: dict, base_market: str= 'KRW'):
        return {
            'response': {
                # 성공 실패 여부
                'success' : 0,
                # 응답코드
                'code': '',
                # 응답메세지
                'message': '',
            },
            # 원본 데이터
            'info': response,

            'history': [
                {
                    # 종목코드
                    'symbol': self.safe_value(response, ''),
                    # 날짜
                    'date': self.safe_string(response, ''),
                    # 시가
                    'open': self.safe_value(response, ''),
                    # 고가
                    'high': self.safe_value(response, ''),
                    # 저가
                    'low': self.safe_value(response, ''),
                    # 종가
                    'close': self.safe_value(response, ''),
                    # 거래량
                    'volume': self.safe_value(response, ''),
                    # 거래대금
                    'amount': self.safe_value(response, '')
                },
                {
                    # 종목코드
                    'symbol': self.safe_value(response, ''),
                    # 날짜
                    'date': self.safe_string(response, ''),
                    # 시가
                    'open': self.safe_value(response, ''),
                    # 고가
                    'high': self.safe_value(response, ''),
                    # 저가
                    'low': self.safe_value(response, ''),
                    # 종가
                    'close': self.safe_value(response, ''),
                    # 거래량
                    'volume': self.safe_value(response, ''),
                    # 거래대금
                    'amount': self.safe_value(response, '')
                },
            ]
            
        }
    
    def parse_ohlcv(self, ohlcv, base_market: str= 'KRW'):
        if isinstance(ohlcv, list):
            return [
                self.safe_string(ohlcv, 0),  # timestamp
                self.safe_number(ohlcv, 1),  # open
                self.safe_number(ohlcv, 2),  # high
                self.safe_number(ohlcv, 3),  # low
                self.safe_number(ohlcv, 4),  # close
                self.safe_number(ohlcv, 5),  # volume
            ]
        return ohlcv
    
    def parse_ohlcva(self, ohlcva, base_market: str= 'KRW'):
        if isinstance(ohlcva, list):
            return [
                self.safe_string(ohlcva, 0),  # timestamp
                self.safe_number(ohlcva, 1),  # open
                self.safe_number(ohlcva, 2),  # high
                self.safe_number(ohlcva, 3),  # low
                self.safe_number(ohlcva, 4),  # close
                self.safe_number(ohlcva, 5),  # volume
                self.safe_number(ohlcva, 6),  # amount
            ]
        return ohlcva
    
    def resample(self, df, timeframe: str, offset):
        ohlcv = {
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }
        
        result = df.resample(timeframe.upper(), offset=offset).apply(ohlcv)
        return result
    
    def fetch_is_holiday(self, dt: datetime, base_market: str= 'KRW'):
        """
        휴장일 조회

        Args:
            dt (datetime): 조회 날짜 (YYYYMMDD)
            base_market (str, optional): Market 구분 코드. Defaults to 'KRW'.
        """
        pass

    def parse_is_holiday(self, response: dict):
        return {
            'response': {
                # 성공 실패 여부
                'success' : 0,
                # 응답코드
                'code': '',
                # 응답메세지
                'message': '',
            },
            # 원본 데이터
            'info': response,

            # 날짜 (YYYYMMDD)
            'date': self.safe_string(response, ''),
            # 개장일 여부 (Y/N)
            'is_open': self.safe_boolean(response, ''),
        }
    
    # endregion public feeder

    # region private feeder
    def fetch_user_info(self, base_market: str= 'KRW'):
        """
        회원 정보 조회

        Args:
            base_market (str, optional): Market 구분 코드. Defaults to 'KRW'.
        """
        pass
    
    def fetch_balance(self, acc_num: str, base_market: str= 'KRW'):
        """
        보유 자산 조회

        Args:
            acc_num (str): 계좌 번호
            base_market (str, optional): Market 구분 코드. Defaults to 'KRW'.
        """
        pass

    def parse_balance(self, response: dict, base_market: str= 'KRW'):
        return {
            'response': {
                # 성공 실패 여부
                'success' : 0,
                # 응답코드
                'code': '',
                # 응답메세지
                'message': '',
            },
            # 원본 데이터
            'info': response,

            'balance': [
                {
                    # 종목코드
                    'symbol': self.safe_string(response, ''),
                    # 종목명
                    'name': self.safe_string(response, ''),
                    # Long or Short
                    'position': self.safe_string(response, ''),
                    # 매입평균가격
                    'price': self.safe_number(response, ''),
                    'qty': {
                        # 매입 수량
                        'total': self.safe_number(response, ''),
                        # 주문 가능 수량
                        'free': self.safe_number(response, ''),
                        # 기주문 수량 (total - free)
                        'used': self.safe_number(response, '') - self.safe_number(response, '') 
                    },
                    # 매입금액
                    'amount': self.safe_number(response, '')
                },
                {
                    # 종목코드
                    'symbol': self.safe_string(response, ''),
                    # 종목명
                    'name': self.safe_string(response, ''),
                    # Long or Short
                    'position': self.safe_string(response, ''),
                    # 매입평균가격
                    'price': self.safe_number(response, ''),
                    'qty': {
                        # 매입 수량
                        'total': self.safe_number(response, ''),
                        # 주문 가능 수량
                        'free': self.safe_number(response, ''),
                        # 기주문 수량 (total - free)
                        'used': self.safe_number(response, '') - self.safe_number(response, '') 
                    },
                    # 매입금액
                    'amount': self.safe_number(response, '')
                }
            ]
        }
    
    def _parse_balance(self, balance, base_market: str= 'KRW'):
        if isinstance(balance, list):
            return {
                'symbol': self.safe_string(balance, 0),
                'name': self.safe_string(balance, 1),
                'position': self.safe_string(balance, 2),
                'price': self.safe_number(balance, 3),
                'qty': 
                {
                    # 매입 수량
                    'total': self.safe_number(balance, 4),
                    # 주문 가능 수량
                    'free': self.safe_number(balance, 5),
                    # 기주문 수량 (total - free)
                    'used': self.safe_number(balance, 4) - self.safe_number(balance, 5) 
                },
                'amount': self.safe_number(balance, 6),
            }
        
        if isinstance(balance, dict):
            return {
                'symbol': self.safe_string(balance, ''),
                'name': self.safe_string(balance, ''),
                'position': self.safe_string(balance, ''),
                'price': self.safe_number(balance, ''),
                'qty': 
                {
                    # 매입 수량
                    'total': self.safe_number(balance, ''),
                    # 주문 가능 수량
                    'free': self.safe_number(balance, ''),
                    # 기주문 수량 (total - free)
                    'used': self.safe_number(balance, '') - self.safe_number(balance, '') 
                },
                'amount': self.safe_number(balance, ''),
            }
        
        return balance

    def fetch_cash(self, acc_num: str, base_market: str= 'KRW'):
        """
        예수금 조회

        Args:
            acc_num (str): 계좌 번호
            base_market (str, optional): Market 구분 코드. Defaults to 'KRW'.
        """
        pass

    def parse_cash(self, response: dict, base_market: str= 'KRW'):
        return {
            'response': {
                # 성공 실패 여부
                'success' : 0,
                # 응답코드
                'code': '',
                # 응답메세지
                'message': '',
            },
            # 원본 데이터
            'info': response,

            # 정산금액 (KR: D+2 예수금)
            'cash': self.safe_number(response, '')
        }
    
    def fetch_screener_list(self, base_market: str= 'KRW'):
        """
        조건식 리스트 조회

        Returns:
            _type_: 조건식 리스트
        """
        pass
    
    def fetch_screener(self, screen_id: str, base_market: str= 'KRW'):
        """
        조건식 조회 결과

        Args:
            screen_id (str): Screener 조회 값 (조건식 조회 결과)
            base_market (str, optional): Market 구분 코드. Defaults to 'KRW'.
        """
        pass
    
    def fetch_deposit_history(self, acc_num: str, base_market: str= 'KRW'):
        """
        입금 내역 조회

        Args:
            acc_num (str): 계좌 번호
            base_market (str, optional): Market 구분 코드. Defaults to 'KRW'.
        """
        pass
    
    def fetch_withdrawal_history(self, acc_num: str, base_market: str= 'KRW'):
        """
        출금 내역 조회

        Args:
            acc_num (str): 계좌 번호
            base_market (str, optional): Market 구분 코드. Defaults to 'KRW'.
        """
        pass
    # endregion private feeder

    # region broker
    def create_order(self, acc_num: str, symbol: str, ticket_type: str, price: float, qty: float, otype: str, base_market: str= 'KRW'):
        """
        주문 발행

        Args:
            acc_num (str): 계좌정보(계좌번호, 지갑정보)
            symbol (str): 종목정보(종목코드)
            ticket_type (str): EntryLong, EntryShort, ExitLong, ExitShort, ... 
            price (float): 가격
            qty (float): 수량
            otype (str): 시장가, 지정가, ...
            base_market (str, optional): Market 구분 코드. Defaults to 'KRW'.
        """
        pass

    def cancel_order(self, acc_num: str, order_id: str, symbol: Optional[str] = '', qty: float = 0, *args, base_market: str= 'KRW'):
        """
        미체결 주문 취소

        Args:
            acc_num (str): 계좌정보(계좌번호, 지갑정보)
            order_id (str): 주문 정보(주문 id)
            symbol (str, optional): 종목정보(종목코드). Defaults to ''.
            qty (float, optional): 수량. Defaults to 0..
            base_market (str, optional): Market 구분 코드. Defaults to 'KRW'.
        """
        pass
    
    def modify_order(self, acc_num: str, order_id: str, price: float, qty: float, *args, symbol: Optional[str] = '',  base_market: str= 'KRW'):
        """
        미체결 주문 정정

        Args:
            acc_num (str): 계좌정보(계좌번호, 지갑정보)
            order_id (str): 주문 정보(주문 id)
            price (float): 가격
            qty (float): 수량
            symbol (str, optional): 종목정보(종목코드). Defaults to ''.
            base_market (str, optional): Market 구분 코드. Defaults to 'KRW'.
        """
        pass

    def parse_order_response(self, response: dict, base_market: str='KRW'):
        time = self.safe_string(response, '')
        today = datetime.today()
        dt = datetime.combine(today, datetime.strptime(time, '%H%M%S').time())

        return {
            'response': {
                # 성공 실패 여부
                'success' : 0,
                # 응답코드
                'code': '',
                # 응답메세지
                'message': '',
            },
            # 원본 데이터
            'info': response,

            # 주문 날짜 (YYYY-mm-DD HH:MM:SS)
            'datetime': datetime.strftime(dt, '%Y-%m-%d %H:%M:%S'),
            # 주문번호
            'order_id': self.safe_string(response, ''),
        }
    
    def fetch_open_order(self, acc_num: str, symbol: Optional[str] = '', start: Optional[str] = None, end: Optional[str] = None, base_market: str= 'KRW'):
        """
        미체결 주문 내역 조회

        Args:
            acc_num (str): 계좌정보(계좌번호, 지갑정보)
            symbol (str, optional): 종목정보(종목코드) Defaults to ''.
            start (str, optional): 조회 시작일자(YYYYMMDD). Defaults to None.
            end (str, optional): 조회 종료일자(YYYYMMDD). Defaults to None.
            base_market (str, optional): Market 구분 코드. Defaults to 'KRW'.
        """
        pass

    def parse_open_order(self, response: dict, base_market: str='KRW'):
        data = self.safe_value(response, '')
        if data is None:
            return response
        
        orders = [self.parse_open_order_history(_) for _ in data]
        sorted_orders = self.sort_by(orders, 0)

        return {
            'response': {
                # 성공 실패 여부
                'success' : 0,
                # 응답코드
                'code': '',
                # 응답메세지
                'message': '',
            },
            # 원본 데이터
            'info': response,
            # 주문 정보
            'orders': sorted_orders
        }
    
    def parse_open_order_history(self, order:dict, base_market: str='KRW'):
        date = self.safe_string(order, '')
        time = self.safe_string(order, '')
        dt = datetime.combine(datetime.strptime(date, '%Y%m%d'), datetime.strptime(time, '%H%M%S').time())

        return {
            # 주문 날짜 (YYYY-mm-DD HH:MM:SS)
            'datetime': datetime.strftime(dt, '%Y-%m-%d %H:%M:%S'),
            # 주문번호
            'order_id': self.safe_string(order, ''),
            # 원주문번호
            'org_order_id': self.safe_string(order, ''),
            # 주문구분
            'order_type': self.safe_string(order, ''),
            # long or short
            'position': self.safe_string(order, ''),
            # 종목코드
            'symbol': self.safe_string(order, ''),
            # 주문단가
            'price': self.safe_number(order, ''),
            'qty': {
                # 주문수량
                'total': self.safe_number(order, ''),
                # 체결수량
                'used': self.safe_number(order, ''),
                # 잔여수량
                'free': self.safe_number(order, '')
            }
        }
    
    def fetch_closed_order(self, acc_num: str, symbol: Optional[str] = '', start: Optional[str] = None, end: Optional[str] = None, base_market: str= 'KRW'):
        """
        체결 주문 내역 조회

        Args:
            acc_num (str): 계좌정보(계좌번호, 지갑정보)
            symbol (str, optional): 종목정보(종목코드) Defaults to ''.
            start (str, optional): 조회 시작일자(YYYYMMDD). Defaults to None.
            end (str, optional): 조회 종료일자(YYYYMMDD). Defaults to None.
            base_market (str, optional): Market 구분 코드. Defaults to 'KRW'.
        """
        pass

    def parse_closed_order(self, response: dict, base_market: str='KRW'):
        data = self.safe_value(response, '')
        if data is None:
            return response
        
        orders = [self.parse_closed_order_history(_) for _ in data]
        sorted_orders = self.sort_by(orders, 0)

        return {
            'response': {
                # 성공 실패 여부
                'success' : 0,
                # 응답코드
                'code': '',
                # 응답메세지
                'message': '',
            },
            # 원본 데이터
            'info': response,
            # 주문 정보
            'orders': sorted_orders
        }
    
    def parse_closed_order_history(self, order:dict, base_market: str='KRW'):
        date = self.safe_string(order, '')
        time = self.safe_string(order, '')
        dt = datetime.combine(datetime.strptime(date, '%Y%m%d'), datetime.strptime(time, '%H%M%S').time())

        return {
            # 주문 날짜 (YYYY-mm-DD HH:MM:SS)
            'datetime': datetime.strftime(dt, '%Y-%m-%d %H:%M:%S'),
            # 주문번호
            'order_id': self.safe_string(order, ''),
            # 원주문번호
            'org_order_id': self.safe_string(order, ''),
            # 주문구분
            'order_type': self.safe_string(order, ''),
            # long or short
            'position': self.safe_string(order, ''),
            # 종목코드
            'symbol': self.safe_string(order, ''),
            # 평균가
            'price': self.safe_number(order, ''),
            # 체결수량
            'qty': self.safe_number(order, '')
        }
    
    def reserve_order(self, acc_num:str, symbol: str, price: float, qty: float, target_date: str, base_market: str= 'KRW'):
        """
        예약 주문 발행

        Args:
            acc_num (str): 계좌정보(계좌번호, 지갑정보)
            symbol (str): 종목정보(종목코드)
            price (float): 가격
            qty (float): 수량
            target_date (str): 예약일자
            base_market (str, optional): Market 구분 코드. Defaults to 'KRW'.
        """
        pass
    # endregion broker

    def get_error_response(self, error_code, error_message):
        return {
            'response': {
                # 성공 실패 여부
                'success' : '-1',
                # 응답코드
                'code': error_code,
                # 응답메세지
                'message': error_message,
            }
        }
    
    @staticmethod
    def now(base_market: str = 'KRW'):
        if base_market == 'KRW':
            return datetime.now(tz=pytz.timezone('Asia/Seoul'))
        elif base_market == 'USD':
            return datetime.now(tz=pytz.timezone('US/Eastern'))
        else:
            return datetime.now(tz=pytz.utc)

    @staticmethod
    def set_attr(self, attrs):
        for key in attrs:
            if hasattr(self, key) and isinstance(getattr(self, key), dict):
                setattr(self, key, self.deep_extend(getattr(self, key), attrs[key]))
            else:
                setattr(self, key, attrs[key])

    @staticmethod
    def extend(*args):
        if args is not None:
            result = None
            if type(args[0]) is collections.OrderedDict:
                result = collections.OrderedDict()
            else:
                result = {}
            
            for arg in args:
                result.update(arg)

            return result
        
        return {}

    @staticmethod
    def deep_extend(*args):
        result = None
        for arg in args:
            if isinstance(arg, dict):
                if not isinstance(result, dict):
                    result = {}
                for key in arg:
                    result[key] = Exchange.deep_extend(result[key] if key in result else None, arg[key])
            else:
                result = arg

        return result
    
    @staticmethod
    def implode_params(string, params):
        if isinstance(params, dict):
            for key in params:
                if not isinstance(params[key], list):
                    string = string.replace('{' + key + '}', str(params[key]))

        return string
    
    @staticmethod
    def omit(d, *args):
        if isinstance(d, dict):
            result = d.copy()
            for arg in args:
                if type(arg) is list:
                    for key in arg:
                        if key in result:
                            del result[key]
                else:
                    if arg in result:
                        del result[arg]
            return result
        return d
    
    def implode_hostname(self, url: str, hostname):
        return self.implode_params(url, {'hostname': hostname})

    def parse_json(self, http_response):
        return json.loads(http_response, parse_float=str, parse_int=str)
    
    # region safe method
    @staticmethod
    def key_exists(dictionary, key):
        if hasattr(dictionary, '__getitem__') and not isinstance(dictionary, str):
            if isinstance(dictionary, list) and type(key) is not int:
                return False
            try:
                value = dictionary[key]
                return value is not None and value != ''
            except LookupError:
                return False
        return False
    
    @staticmethod
    def safe_value(dictionary, key, default_value=None):
        return dictionary[key] if Exchange.key_exists(dictionary, key) else default_value
    
    @staticmethod
    def safe_string(dictionary, key, default_value=''):
        return str(dictionary[key]) if Exchange.key_exists(dictionary, key) else default_value
    
    @staticmethod
    def safe_number(dictionary, key, default_value=0):
        value = Exchange.safe_string(dictionary, key)
        if value == '':
            return default_value
        
        try:
            return float(value)
        except Exception:
            return default_value
    
    @staticmethod
    def safe_boolean(dictionary, key, default_value=False):
        value = Exchange.safe_string(dictionary, key)
        if value == '':
            return default_value
        
        try:
            return bool(strtobool(value))
        except Exception:
            return default_value

    # endregion safe method

    @staticmethod
    def keysort(dictionary):
        return collections.OrderedDict(sorted(dictionary.items(), key=lambda t: t[0]))

    @staticmethod
    def sort_by(array, key, descending=False):
        return sorted(array, key=lambda k: k[key] if k[key] is not None else "", reverse=descending)

    @staticmethod
    def sort_by_2(array, key1, key2, descending=False):
        return sorted(array, key=lambda k: (k[key1] if k[key1] is not None else "", k[key2] if k[key2] is not None else ""), reverse=descending)

    @staticmethod
    def index_by(array, key):
        result = {}
        if type(array) is dict:
            array = Exchange.keysort(array).values()
        is_int_key = isinstance(key, int)
        for element in array:
            if ((is_int_key and (key < len(element))) or (key in element)) and (element[key] is not None):
                k = element[key]
                result[k] = element
        return result
    
    @staticmethod
    def to_array(value):
        return list(value.values()) if type(value) is dict else value

    def filter_by_array(self, objects, key: IndexType, values=None, indexed=True):
        objects = self.to_array(objects)

        # return all of them if no values were passed
        if values is None or not values:
            return self.index_by(objects, key) if indexed else objects
        
        results = []
        for i in range(0, len(objects)):
            if self.in_array(objects[i][key], values):
                results.append(objects[i])
        
        return self.index_by(results, key) if indexed else results