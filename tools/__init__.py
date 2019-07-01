#! -*- coding: utf-8 -*-


def result_generator(rc, data, mm):
    """统一生成返回格式"""
    rd = {
        'status': rc,
        'data': data,
    }
    return rd
