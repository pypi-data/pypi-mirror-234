# -*- coding: utf-8 -*-

import os
import sqlite3

from collections import namedtuple


# 传递路数据库路径参数的装饰器
def Path(path: str):
    def wrapper(cls):
        # 确保目录存在
        db_folder = os.path.dirname(path)
        if db_folder != '' and not os.path.exists(db_folder):
            os.makedirs(db_folder, exist_ok=True)
        # 新增数据库路径属性
        setattr(cls, "db_path", path)
        return cls

    return wrapper


class MetaDatabase:
    """数据库类，提供库级的操作"""

    # ================================================================================================================
    # 对外提供的可调用方法
    def connect(self, if_allow_multithreading=True):
        """连接数据库"""
        # 设置多线程连接
        self.connection = sqlite3.connect(self.db_path, check_same_thread=not if_allow_multithreading)  # noqa
        # 修改row_factory，使得返回结果为具名元组
        self.connection.row_factory = self.dict_factory
        self.cursor = self.connection.cursor()
        self.__update_cursor()

    def disconnect(self):
        """断开数据库连接"""
        if self.connection:
            self.connection.close()

    def create_tables(self):
        """创建全部表"""
        for dao in self.__dao_list:
            sql_command = dao.get_sql_create_table()
            self.cursor.execute(sql_command)
        self.commit()

    def commit(self):
        """提交事务"""
        self.connection.commit()

    def rollback(self):
        """回滚事务"""
        self.connection.rollback()

    # ================================================================================================================
    # 非外部调用方法
    def __new__(cls, *args, **kwargs):
        # 获取子类的所有属性
        subclass_attrs = dir(cls)

        # 初步筛选静态变量（不包括方法和特殊属性）
        static_attrs = [attr for attr in subclass_attrs
                        if not callable(getattr(cls, attr)) and not attr.startswith("__")]
        # 根据是否具有entity属性筛选出最终dao属性
        dao_list = [getattr(cls, attr) for attr in static_attrs
                    if hasattr(getattr(cls, attr), "entity")
                    and hasattr(getattr(cls, attr), "update_cursor")]

        # 赋值dao_list为类属性，以便在类内部可见
        cls.__dao_list = dao_list

        # 暂不支持单例模式
        return super().__new__(cls, *args, **kwargs)

    def __init__(self):
        self.connection = None
        self.cursor = None

    # ================================================================================================================
    # 类内使用的方法
    def __update_cursor(self):
        for dao in self.__dao_list:
            dao.update_cursor(cursor=self.cursor)

    @staticmethod
    def dict_factory(cursor, row: tuple):
        """转换查询结果格式为具名元组"""
        # 获取列描述信息
        fields = [column[0] for column in cursor.description]
        cls = namedtuple("Record", fields)
        return cls._make(row)  # noqa
