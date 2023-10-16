from collections import namedtuple


class APIResponse:
    #응답코드, 응답헤더, Output, 오류코드, 오류메시지
    def __init__(self, resp):
        self._response_code = resp.status_code
        self._resp = resp
        self._header = self._set_header()
        self._body = self._set_body()
        self._err_code = self._body.rt_cd
        self._err_message = self._body.msg1

    #
    def get_response_code(self):
        return self._response_code

    def _set_header(self):
        fld = dict()
        for x in self._resp.headers.keys():
            if x.islower():
                fld[x] = self._resp.headers.get(x)
        _th_ = namedtuple('header', fld.keys())

        return _th_(**fld)

    def _set_body(self):
        _tb_ = namedtuple('body', self._resp.json().keys())

        return _tb_(**self._resp.json())

    def get_header(self):
        return self._header

    def get_body(self):
        return self._body

    def get_response(self):
        return self._resp

    def is_ok(self):
        try:
            if (self.get_body().rt_cd == '0'):
                return True
            else:
                return False
        except Exception as ex:
            return False

    def get_error_code(self):
        return self._err_code

    def get_error_message(self):
        return self._err_message

    def print_all(self):
        # print(self._resp.headers)
        print("<Header>")
        for x in self.get_header()._fields:
            print(f'\t-{x}: {getattr(self.get_header(), x)}')
        print("<Body>")
        for x in self.get_body()._fields:
            print(f'\t-{x}: {getattr(self.get_body(), x)}')

    def print_error(self):
        print('-------------------------------\nError in response: ', self.get_response_code())
        print(self.get_body().rt_cd, self.get_error_code(), self.get_error_message())
        print('-------------------------------')