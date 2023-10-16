import types
from typing import Union


class Entry:
    def __init__(self, path, market, module, api, method, config):
        # function key
        self.path = path

        # market type : stock, derivative, oversea_stock, oversea_derivative
        self.market = market

        # Feeder / Broker
        self.module = module

        # Token / Hash / Private / Public
        self.api = api

        # GET / POST
        self.method = method

        self.config = config

        def unbound_method(_self, params={}):
            return _self.request(self.path, self.market, self.module, self.api, self.method, params, config=self.config)

        self.unbound_method = unbound_method

    def __get__(self, instance, owner):
        if instance is None:
            return self.unbound_method
        else:
            return types.MethodType(self.unbound_method, instance)

    def __set_name__(self, owner, name):
        self.name = name


IndexType = Union[str, int]