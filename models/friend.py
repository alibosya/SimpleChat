#! -*- coding: utf-8 -*-

from models import ModelBase


class Friend(ModelBase):
    def __init__(self, acc):
        self.acc = acc
        self._attrs = {}

        super(Friend, self).__init__(acc=acc)
