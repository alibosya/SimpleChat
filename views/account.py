#! -*- coding: utf-8 -*-

from logics.account import AccountLogics
from settings import check_name


def register(hm):
    mm = hm.mm
    passwd = hm.get_argument('passwd', '')
    verify_pwd = hm.get_argument('verify_pwd', '')
    if passwd != verify_pwd:
        return 11, {}  # 两次输入密码不一致
    uname = hm.get_argument('uname', '')
    if check_name(uname):
        return 22, {}  # 用户名不符合规范
    nickname = hm.get_argument('nickname', '')
    if not uname or nickname:
        return 33, {}  # 请填写完整注册信息
    # email = hm.get_argument('email', '')
    phone_num = hm.get_argument('phone_num', '')

    al = AccountLogics(mm)
    rc, data = al.register(uname, passwd, nickname, phone_num)
    if rc:
        return rc, {}  # 注册失败
    return rc, data
    return 0, {}


def login(hm):
    # mm = hm.mm
    # uname = hm.get_argument('uname', '')
    # passwd = hm.get_argument('passwd', '')
    # if not uname or not passwd:
    #     return 1, {}  # 信息不全
    # al = AccountLogics(mm)
    # rc, data = al.login(uname, passwd)
    # if rc:
    #     return rc, {}
    # return rc, data
    return 0, {}


def logout(hm):
    mm = hm.mm
    uname = hm.get_argument('uname', '')
    al = AccountLogics(mm)
    rc, data = al.logout(uname)
    if rc:
        return rc, {}  # 退出异常
    return rc, data
