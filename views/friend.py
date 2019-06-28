#! -*- coding: utf-8 -*-

from logics.friend import FriendLogics


def index(hm):
    mm = hm.mm
    fl = FriendLogics(mm)
    rc, data = fl.index()
    if rc:
        return rc, {}
    return rc, data


def send_msg(hm):
    mm = hm.mm
    f_id = hm.get_argument('friend_id', 0)
    msg = hm.get_argument('massage', '')
    if not f_id or not msg:
        return 1, {}
    fl = FriendLogics(mm)
    rc, data = fl.process_msg(f_id, msg)
    if rc:
        return rc, {}
    return rc, data


def receive_msg(hm):
    mm = hm.mm
    f_id = hm.get_argument('friend_id', 0)
    msg = hm.get_argument('massage', '')
    if not f_id or not msg:
        return 1, {}
    fl = FriendLogics(mm)
    rc, data = fl.process_msg(f_id, msg, is_receive=1)
    if rc:
        return rc, {}
    return rc, data


def add_friend(hm):
    mm = hm.mm


def del_friend(hm):
    mm = hm.mm
