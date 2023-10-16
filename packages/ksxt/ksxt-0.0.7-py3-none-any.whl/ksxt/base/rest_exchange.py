import json
import os
from datetime import datetime
from typing import Any, Dict, Optional

from ksxt.base.exchange import Exchange
from ksxt.config import CONFIG_DIR


class RestExchange(Exchange):
    required_credentials = {
        'open_key': True,
        'secret_key': True,
        'uid': False,
        'login': False,
        'password': False,
        'token': False
    }

    headers = None
    token = None
    token_expired = None
    type = 'rest'

    def __init__(self, config: Dict=None) -> None:
        super().__init__()

        self.headers = dict() if self.headers is None else self.headers

        if config is None:
            config = {}

        settings = self.deep_extend(self.describe(), config)
        Exchange.set_attr(self, settings)

        apis = self._get_api_from_file()
        Exchange.set_attr(self, apis)
        
        self.set_token()

    def check_token(func):
        def wrapper(self, *args, **kwargs):
            import time
            if self.token_expired is None or time.strftime('%Y-%m-%d %H:%M:%S') >= self.token_expired:
                self.set_token()

            return func(self, *args, **kwargs)
        return wrapper

    def _get_api_from_file(self):
        tr_config_filename = 'tr_dev.json' if self.is_dev else 'tr_app.json'

        config_path = os.path.join(CONFIG_DIR, tr_config_filename)

        with open(config_path, encoding='utf-8',) as f:
            c = json.load(f)
            return { 'apis': c[self.name] }

    def set_token(self):
        pass

    def prepare_request_headers(self, headers=None):
        headers = headers or {}

        if self.session:
            headers.update(self.session.headers)

        self.headers.update(headers)

        headers.update({"content-type":"application/json"})
        #headers.update({'appKey':self.open_key})
        #headers.update({'appsecret':self.secret_key})

        return headers


    def describe(self) -> Dict:
        return {}

    def fetch(self, url, method='GET', headers=None, body=None, params=None):
        request_headers = headers #self.prepare_request_headers(headers=headers)
        request_body = body
        request_params = params

        self.session.cookies.clear()

        http_response = None
        http_status_code = None
        http_status_text = None
        json_response = None

        try:
            response = self.session.request(
                method=method,
                url=url,
                headers=request_headers,
                data=request_body,
                params=request_params,
                timeout=int(self.timeout / 1000)
            )

            response.encoding = 'utf-8'

            headers = response.headers
            http_status_code = response.status_code
            http_status_text = response.reason
            http_response = response.text.strip()
            json_response = self.parse_json(http_response)

        except TimeoutError as e:
            details = ' '.join([self.id, method, url])
            raise TimeoutError(details) from e
        
        if json_response:
            return json_response

    def sign(self, path, market, module, api: Any = 'public', method='GET', headers: Optional[Any] = None, body: Optional[Any] = None, params: Optional[Any] = None, config={}):
        pass

    def fetch2(self, path, market, module, api: Any = 'public', method='GET', params={}, headers: Optional[Any] = None, body: Optional[Any] = None, config={}):
        # Rate Limit 체크 후 throttle 처리

        is_activate = self.apis[self.type][market][module][path]['activate']
        if not is_activate:
            return {
                'response': {
                # 성공 실패 여부
                'success' : '-1',
                # 응답코드
                'code': 'fail',
                # 응답메세지
                'message': f'지원하지 않는 함수({path}) 입니다.'
            }}

        request = self.sign(path, market, module, api, method, headers, body, params, config)
        return self.fetch(request['url'], request['method'], request['headers'], request['body'], request['params'])

    def request(self, path, market, module, api: Any='public', method='GET', params={}, headers: Optional[Any] = None, body: Optional[Any] = None, config={}):
        return self.fetch2(path, market, module, api, method, params, headers, body, config)


    # region public feeder
    @check_token
    def fetch_markets(self, market_name: str):
        pass
    
    @check_token
    def fetch_security(self, symbol: str, base_market: str = 'KRW'):
        pass
    
    @check_token
    def fetch_ticker(self, symbol: str, base_market: str= 'KRW'):
        pass
    
    @check_token
    def fetch_historical_data(self, symbol: str, time_frame: str, start: Optional[str] = None, end: Optional[str] = None, base_market: str= 'KRW'):
        pass
    
    @check_token
    def fetch_is_holiday(self, dt: datetime, base_market: str= 'KRW'):
        pass    
    # endregion public feeder

    # region private feeder
    @check_token
    def fetch_user_info(self, base_market: str= 'KRW'):
        pass
    
    @check_token
    def fetch_balance(self, acc_num: str, base_market: str= 'KRW'):
        pass
    
    @check_token
    def fetch_cash(self, acc_num: str, base_market: str= 'KRW'):
        pass
    
    @check_token
    def fetch_screener_list(self, base_market: str= 'KRW'):
        pass
    
    @check_token
    def fetch_screener(self, screen_id: str, base_market: str= 'KRW'):
        pass
    
    @check_token
    def fetch_deposit_history(self, acc_num: str, base_market: str= 'KRW'):
        pass
    
    @check_token
    def fetch_withdrawal_history(self, acc_num: str, base_market: str= 'KRW'):
        pass
    # endregion private feeder

    # region broker
    @check_token
    def create_order(self, acc_num: str, symbol: str, ticket_type: str, price: float, qty: float, otype: str, base_market: str= 'KRW'):
        pass
    
    @check_token
    def cancel_order(self, acc_num: str, order_id: str, symbol: Optional[str] = '', qty: float = 0, *args, base_market: str= 'KRW'):
        pass
    
    @check_token
    def modify_order(self, acc_num: str, order_id: str, price: float, qty: float, *args, symbol: Optional[str] = '',  base_market: str= 'KRW'):
        pass
    
    @check_token
    def fetch_open_order(self, acc_num: str, symbol: Optional[str] = '', start: Optional[str] = None, end: Optional[str] = None, base_market: str= 'KRW'):
        pass
    
    @check_token
    def fetch_closed_order(self, acc_num: str, symbol: Optional[str] = '', start: Optional[str] = None, end: Optional[str] = None, base_market: str= 'KRW'):
        pass
    
    @check_token
    def reserve_order(self, acc_num:str, symbol: str, price: float, qty: float, target_date: str, base_market: str= 'KRW'):
        pass
    # endregion broker