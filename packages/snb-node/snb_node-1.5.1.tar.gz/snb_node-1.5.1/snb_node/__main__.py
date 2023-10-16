# -*- coding: utf-8 -*-
"""
@Time    : 2022/7/28
@Author  : wangxinyi
"""
from snb_node import smartnotebookapp as app
from snb_node.snbInitLib import snbPipLib

if __name__ == '__main__':
    snbPipLib()
    app.launch_new_instance()