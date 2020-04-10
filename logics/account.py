#! -*- coding: utf-8 -*-


class AccountLogics():
    def __init__(self, mm):
        self.mm = mm
        self.uid = 0

    def register(self, uname, passwd, nickname, phone_num):
        obj = self.mm.account.get_obj_by_uname()
        if obj:
            return 1, {}  # 用户名已存在  # 后续弄成ajax的
        
    def login(self, uname, passwd):
        pass

    def logout(self, uname):
        pass
