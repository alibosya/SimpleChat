#! -*- coding: utf-8 -*-

import importlib
from tornado import web

from settings import result_generator
from lib.environ import HandlerManager


class AccountHandler(web.RequestHandler):

    def initialize(self):
        self.hm = HandlerManager(self)

    def get(self):
        self.handler()

    def post(self):
        self.handler()

    def handler(self):
        rc, data, mm = self.api()
        result = result_generator(rc, data, mm)
        self.write(result)
    
    def result_info(self, rc, data=None):
        """返回信息"""
        if not data:
            data = {}
        return rc, data, self.hm.mm

    def api(self):
        method_name = self.get_argument('method', '')
        if not method_name:
            method_name = 'login'
        try:
            module = importlib.import_module('views.account')
        except ImportError:
            print '---------ImportError-----views.account---------'
            return self.result_info('err_module')
        method = getattr(module, method_name)
        if callable(method):
            rc, data = method(self.hm)
            return self.result_info(rc, data)
        return self.result_info('err_not_call_method')


class APIRequestHandler(web.RequestHandler):
    """全部API处理公共接口"""

    def initialize(self):
        """初始化操作"""
        self.hm = HandlerManager(self)

    def get(self):
        self.handler()

    def post(self):
        self.handler()
    
    def handler(self):
        # method_param = self.get_argument('method', '')
        # module_name, method_name = method_param.split(".")
        # print 'module_name, method_name ==>', module_name, method_name
        rc, data, mm = self.api()
        result = result_generator(rc ,data, mm)
        self.write(result)

    def api(self):
        """api统一调用方法"""
        print '-' * 50
        method_param = self.get_argument('method', '')
        module_name, method_name = method_param.split(".")

        try:
            module = importlib.import_module('views.%s' % module_name)
        except ImportError:
            print '---------ImportError-----%s---------' % module_name
            return self.result_info('err_module')
        method = getattr(module, method_name, None)
        if not method:
            return self.result_info('err_method')
        if callable(method):
            rc, data = method(self.hm)
            return self.result_info(rc, data)
        return self.result_info('err_not_call_method')

    def result_info(self, rc, data=None):
        """返回信息"""
        if not data:
            data = {}
        return rc, data, self.hm.mm
