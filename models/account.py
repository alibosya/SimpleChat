#! -*- coding: utf-8 -*-

import time

from models import ModelBase
from settings import md5


class Account(ModelBase):
    """账户"""

    def __init__(self, acc):
        self.acc = acc
        self._attrs = {
            'passwd': '',
            'reg_time': '',
            'uname': '',
            'friends': [],
            'chat_log': {},
            'gender': '',
            'is_cold': False,
            'last_online_time': '',
            'mk': '',
            'apply_msg': {},
            'send_apply_msg': {},
        }

        super(Account, self).__init__(acc=self.acc)

    @classmethod
    def check_exist(cls, acc):
        """
        检查账号是否存在
        :param acc:
        :return:
        """
        key = cls.make_key(acc)
        return cls.rds.exists(key)

    def check_passwd(self, passwd):
        """
        检查密码
        :param passwd:
        :return:
        """
        return self.passwd == md5(passwd)

    def update_passwd(self, passwd):
        """
        更新密码
        :param passwd:
        :return:
        """
        self.passwd = md5(passwd)

    def add_friend(self, f_acc):
        """
        添加好友
        :param acc:
        :return:
        """
        if self.is_friend(f_acc):
            return 1, {}  # 已经是好友
        if f_acc == self.acc:
            return 2, {}  # 不能添加自己为好友
        if not self.__class__.check_exist(f_acc):
            return 3, {}  # 账号不存在
        self.friends.append(f_acc)
        f_obj = self.__class__.get(f_acc)
        f_obj.friends.append(self.acc)

    def update_chat_log(self, f_acc, c_time, log):
        """
        更新聊天记录
        :param f_acc:
        :param c_time:
        :param log:
        :return:
        """
        if not self.chat_log.get(f_acc, []):
            self.chat_log[f_acc] = []
        self.chat_log[f_acc].append(c_time, log)

    def del_friend(self, f_acc):
        """
        删除好友
        :param f_acc:
        :return:
        """
        if f_acc not in self.friends:
            return 1, {}  # 此账号不是该用户好友
        self.friends.remove(f_acc)
        f_obj = self.__class__.get(f_acc)
        f_obj.friends.remove(self.acc)

    def is_friend(self, f_acc):
        """
        是否是好友
        :param f_acc:
        :return:
        """
        return f_acc in self.friends

    def add_apply_friend_msg(self, f_acc):
        """
        好友申请信息
        :param f_acc:
        :return:
        """
        now = int(time.time())
        self.send_apply_msg[f_acc] = now
        f_obj = self.__class__.get(f_acc)
        f_obj.apply_msg[self.acc] = now
