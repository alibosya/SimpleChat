#! -*- coding: utf-8 -*-

import time

from settings import check_name, check_acc
from models.account import Account


def register(hm):
    """
    注册账号
    :param hm:
    :return:
    """
    mm = hm.mm
    passwd = hm.get_argument('passwd', '')
    verify_pwd = hm.get_argument('verify_pwd', '')
    if passwd != verify_pwd:
        return 11, {}  # 两次输入密码不一致
    uaccount = hm.get_argument('uaccount', '')
    uname = hm.get_argument('uname', '')
    if not check_name(uname):
        return 22, {}  # 用户名不符合规范
    if not check_acc(uaccount):
        return 33, {}  # 账号不符合规范
    if Account.check_exist(uaccount):
        return 44, {}  # 账号已存在

    now = int(time.time())
    acc_obj = mm.account.get(uaccount)
    acc_obj.acc = uaccount
    acc_obj.update_passwd(passwd)
    acc_obj.uname = uname
    acc_obj.reg_time = now
    acc_obj.last_online = now
    acc_obj.save()
    return 0, {'is_success': True}


def login(hm):
    """
    登录
    :param hm:
    :return:
    """
    mm = hm.mm
    acc = hm.get_argument('uaccount', '')
    passwd = hm.get_argument('passwd', '')
    if not acc or not passwd:
        return 1, {}  # 信息不全
    if not Account.check_exist(acc):
        return 2, {}  # 账号不存在
    acc_obj = mm.account.get(acc)
    if acc_obj.is_cold:
        return 3, {}  # 账户被冻结
    if not acc_obj.check_passwd(passwd):
        return 4, {}  # 密码不正确
    return 0, {'is_success': True}


def logout(hm):
    """
    登出
    :param hm:
    :return:
    """
    mm = hm.mm
    acc = hm.get_argument('uaccount', '')
    if not acc:
        return 1, {}  # 参数错误
    if not Account.check_exist(acc):
        return 2, {}  # 账号不存在
