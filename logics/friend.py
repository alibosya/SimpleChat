#! -*- coding: utf-8 -*-


class FriendLogics():
    def __init__(self, mm):
        self.mm = mm

    def index(self):
        pass

    def process_msg(self, f_id, msg, is_receive=0):
        f_obj = self.mm.friend.get_friend_obj_by_uid(f_id)
        if not f_obj:
            return 2, {}  # 好友不存在
        if not is_receive:
            pass
        else:
            pass

    def get_friend_list(self):
        pass

    def del_friend(self):
        pass

    def add_friend(self):
        pass
