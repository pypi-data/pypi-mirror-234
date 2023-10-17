# -*- coding: utf-8 -*-

from typing import Union


def Entity(cls):
    """更改返回的值，如果不使用此装饰器，则始终完整返回默认值（包括约束），这在单独使用数据类的时候很不便，但对于建表（需要知道约束）和插入（需要知道主键约束）不影响
    仅在单独使用数据类的时候有效"""
    orig_getattribute = cls.__getattribute__

    def new_getattribute(self, name):
        value = orig_getattribute(self, name)
        return get_value_from_field(value)

    cls.__getattribute__ = new_getattribute
    return cls


class Constant:
    """存储特殊形式的常量"""
    PRIMARY_KEY = ("PRIMARY KEY",)
    AUTO_PRIMARY_KEY = ("PRIMARY KEY AUTOINCREMENT",)
    NOT_NULL = ("NOT NULL",)
    UNIQUE = ("UNIQUE",)

    NO_ACTION = 'NO ACTION'
    RESTRICT = 'RESTRICT'
    CASCADE = 'CASCADE'
    SET_NULL = 'SET NULL'
    SET_DEFAULT = 'SET DEFAULT'


class Constraint:
    """提供对字段的各种约束"""

    # =================================================================================================================
    # 1.可直接使用的约束常量
    primary_key = Constant.PRIMARY_KEY  # 主键
    auto_primary_key = Constant.AUTO_PRIMARY_KEY  # 自增主键
    not_null = Constant.NOT_NULL  # 非空
    unique = Constant.UNIQUE  # 唯一

    # 针对外键的约束
    no_action = Constant.NO_ACTION
    cascade = Constant.CASCADE
    set_null = Constant.SET_NULL
    restrict = Constant.RESTRICT
    set_default = Constant.SET_DEFAULT

    # =================================================================================================================
    # 2.需要外部传值的约束
    @staticmethod
    def default(default_value: Union[int, str, float, bytes]):
        """默认值约束"""
        if type(default_value) in {int, str, float, bytes}:
            return (f'DEFAULT {default_value}',)  # noqa
        raise TypeError(f'数据类型不匹配，允许的数据类型为：int, str, float, bytes')

    @staticmethod
    def check(check_condition: str):
        """条件约束"""
        if type(check_condition) in {str}:
            return (f'CHECK({check_condition})',)  # noqa
        raise TypeError(f'数据类型不匹配，允许的数据类型为：str')

    @staticmethod
    def foreign_key(entity, field, delete_link=None, update_link=None):
        """外键约束"""
        return ((entity.__name__, field, delete_link, update_link),)  # noqa

    @staticmethod
    def comment(comment: str):
        """字段注释"""
        if type(comment) in {str}:
            return (f'-- {comment}\n',)  # noqa
        raise TypeError(f'数据类型不匹配，允许的数据类型为：str')


def get_constraint_from_field(field_value):
    """从属性值中解析出约束条件"""
    if not isinstance(field_value, tuple):
        return []

    # 单元素元组
    if len(field_value) == 1:
        return list(field_value)

    # 多元素元组
    elif len(field_value) >= 1:
        constraints = []

        for item in field_value:

            if not isinstance(item, tuple):
                continue
            # 元素也是元组，说明是约束条件
            if len(item) == 1:
                constraints.append(item[0])
            else:
                raise TypeError(f'约束条件必须为长度为1的元组，错误的数据：{item}')

        return constraints


def get_value_from_field(field_value):
    """从属性值中解析出是基本类型的唯一属性默认值"""
    # 属性值就是基本类型
    if isinstance(field_value, (int, str, float, bytes)) or field_value is None:
        return field_value

    # 检查是否为元组
    if not isinstance(field_value, tuple):
        raise TypeError('该属性值的类型不满足要求，只允许基本类型和元组')

    # 用列表保存匹配到的基本属性值，用来进一步检验该值是否唯一
    value_list = []
    for value in field_value:
        if isinstance(value, (int, str, float, bytes)):
            value_list.append(value)

    list_length = len(value_list)
    # 没有默认值
    if list_length == 0:
        return None
    # 有唯一的默认值
    elif list_length == 1:
        return value_list[0]
    else:
        raise TypeError('错误传递了多个基本数据类型的默认值，只允许有一个默认值')
