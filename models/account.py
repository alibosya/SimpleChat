#! -*- coding: utf-8 -*-

from models import ModelBase


class Account(ModelBase):
    """"""

    def __init__(self, acc):
        self.acc = acc
        self._attrs = {}

        super(Account, self).__init__(acc=acc)

    def pre_use(self):
        pass



