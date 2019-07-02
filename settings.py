#! -*- coding: utf-8 -*-

import re
import time
import hashlib


def set_env(env_name, server=None, cw_num=1, *args, **kwargs):
    """

    :param env_name: 环境名
    :param server: 服务类型  login/config/app/admin/pament
    :param cw_num: celery_worker数量
    :param args:
    :param kwargs:
    :return:
    """
    # game_config里面的配置都是只读的, copy的时候改回原始类型
    start = time.time()
    pattern = re.compile('^[a-zA-Z][a-zA-Z0-9_]{5,15}$').match
    globals()['UID_PATTERN'] = pattern

    print 'set_env_spend_time: ', time.time() - start


def check_acc(acc):
    """
    检查account格式是否正确
    :param uid:
    :return:
    """
    return False if not globals()['UID_PATTERN'](acc) else True


def check_name(name):
    """
    # 名字只能是汉字, 字母或数字
    # 名字只能是字母 数字 下划线
    :param name:
    :return:
    """
    new_name = re.findall(r'[\d,a-z,A-Z]+|[\u4e00-\u9fa5]+', name)
    if len(''.join(new_name)) != len(name):
        return False
    return True


def result_generator(rc, data, mm):
    """统一生成返回格式"""
    rd = {
        'status': rc,
        'data': data,
    }
    return rd


def md5(s):
    return hashlib.md5(str(s)).hexdigest()
