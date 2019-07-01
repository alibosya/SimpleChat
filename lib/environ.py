#! -*- coding: utf-8 -*-


class HandlerManager(object):
    """请求管理类"""

    def __init__(self, request_handler):
        self.req = request_handler
        # self.params = self.req.params
        self.uid = self.req.get_argument('user_token', '')
        if self.uid:
            self.mm = ModelManager(self.uid)
            self.action = self.req.get_argument('method', '')
            # self.args = self.params()
        else:
            self.mm = None
    
    _ARG_DEFAULT = []

    def get_argument(self, name, default=_ARG_DEFAULT, is_int=False):
        value = self.req.get_argument(name, default=default)
        if not value:
            return 0 if is_int else ''
        return abs(int(float(value))) if is_int else value


class ModelManager(object):
    """管理类"""

    _register_base = {}
    
    def __init__(self, uid):
        self.uid = uid
        self._model = {}

    def register_model(self, model_name, model):
        if model_name not in self.__class__._register_base:
            self.__class__._register_base[model_name] = model
            setattr(self.__class__, model_name, property(self.get_obj()))
        else:
            old_model = self.__class__._register_base[model_name]
            raise RuntimeError('model [%s] already exists \n'
                               'Conflict between the [%s] and [%s]' %
                               (model_name, old_model, model))

    def get_obj(self, model_name):
        """获取model对象"""
        key = str(model_name)
        if key in self._model:
            obj = self._model[key]
        elif model_name in self._register_base:
            obj = self._register_base[model_name].get(self.uid, mm=self)
            obj._model_name = model_name
            setattr(obj, 'mm', self)
            self._model[key] = obj
            if hasattr(obj, 'pre_use'):
                obj.pre_use()
        else:
            obj = None
        return obj
    
    def get_mm(self, uid):
        """获取ModelManager对象"""
        if uid == self.uid:
            return self
        else:
            mm_obj = self.__class__(uid)
        return mm_obj
