# -*- coding: utf-8 -*-

import os
import shutil


def get_example():
    """复制本文件的工具函数"""
    # 获取当前文件的路径
    src = os.path.join(os.path.dirname(__file__), 'example_simple.py')
    dst = "ysql_example_simple.py"
    shutil.copy(src, dst)
    print('已生成示例文件：ysql_example_simple.py')

    src = os.path.join(os.path.dirname(__file__), 'example_detailed.py')
    dst = "ysql_example_detailed.py"
    shutil.copy(src, dst)
    print('已生成示例文件：ysql_example_detailed.py')
