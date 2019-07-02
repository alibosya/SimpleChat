#! -*- coding: utf-8 -*-

import redis

from ast import literal_eval


class ModelTools(object):
    """"""
    def __init__(self, host='localhost', port=6379, password=None, db=0):
        pool = redis.ConnectionPool(host=host, port=port, password=password, db=db)
        self.rds = redis.Redis(connection_pool=pool)

    @classmethod
    def _key_prefix(cls):
        return "%s||%s" % (cls.__module__, cls.__name__)

    def make_key(self, acc=''):
        if not acc:
            acc = self.acc
        return self.__class__._key_prefix() + "||%s" % str(acc)


class ModelBase(ModelTools):
    """"""

    def __new__(cls, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        cls._attr_base = {}
        cls._attrs = {}

    def __init__(self, acc=None):
        """

        :param acc:
        """
        if not self._attrs:
            raise ValueError, 'attr_base must be not empty'
        self._attr_base.update(self._attrs)
        self.__dict__.update(self._attr_base)
        self.acc = str(acc)
        self.mm = None
        self._model_key = None
        super(ModelBase, self).__init__()

    @classmethod
    def loads(cls, acc, data, o=None):
        """
        数据反序列化(将数据库中的数据赋值到自身)
        :param acc:
        :param data:
        :param o:
        :return:
        """
        o = o or cls(acc)
        for k in cls._attr_base:
            v = data.get(k)
            if v is None:
                v = o._attr_base[k]
            setattr(o, k, v)
        return o

    def dumps(self):
        """
        数据序列化(将自身数据取出来)
        :param compress:
        :return:
        """
        r = {}
        for k in self._attr_base:
            data = getattr(self, k)
            r[k] = data
        return r

    def save(self, acc=''):
        """
        保存
        :param acc:
        :return:
        """
        _key = self._model_key
        if not _key:
            _key = self.make_key(acc)
        s = self.dumps()
        self.rds.set(_key, s)

    def get(self, acc, mm=None, *args, **kwargs):
        """
        获得数据
        :param acc:
        :param mm:
        :param args:
        :param kwargs:
        :return:
        """
        _key = self.__class__.make_key(acc=acc)
        o = self.__class__(acc)
        o._model_key = _key
        redis_data = self.rds.get(_key)
        if not redis_data:
            o.inited = True
            o.mm = mm
        else:
            try:
                redis_data = literal_eval(redis_data)
            except Exception as e:
                raise ValueError('redis_data evel fail')
            o = self.__class__.loads(acc, redis_data, o)
            o.inited = False
            o.mm = mm
        return o

    def reset(self, save=True):
        """
        重置数据
        :param save:
        :return:
        """
        self.__dict__.update(self._attrs)
        if save:
            self.save()

    def reload(self):
        """
        重新加载数据
        :return:
        """
        self.__dict__.update(self.get(self.acc).__dict__)

    def delete(self):
        """
        删除数据
        :return:
        """
        _key = self._model_key
        self.rds.delete(_key)

    def pre_use(self):
        pass
