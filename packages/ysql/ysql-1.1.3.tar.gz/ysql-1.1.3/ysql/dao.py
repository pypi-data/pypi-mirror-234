# -*- coding: utf-8 -*-

from ysql.entity import Constraint, get_constraint_from_field

# 约定的表名代替符，在sql语句中凡是涉及本表表名的，均可采取此代替符，内部可自动替换。
TABLE_SUBSTITUTE = '__'


# ====================================================================================================================
# 装饰器方法
def Dao(entity):
    """dao类的统一装饰器"""

    def decorator(cls):
        # 新增cursor属性
        setattr(cls, "__cursor", None)
        # 新增entity属性
        setattr(cls, "entity", entity)
        # 新增更新游标方法
        setattr(cls, update_cursor.__name__, update_cursor)
        # 新增生成表方法
        setattr(cls, get_sql_create_table.__name__, get_sql_create_table)
        # 新增插入方法
        setattr(cls, "insert", insert)
        return cls

    return decorator


def Sql(sql_command):
    """一般化执行sql语句的装饰器"""

    def decorator(func):  # noqa
        def wrapper(self, *args, **kwargs):
            new_command = __convert_entity_name(sql_command=sql_command,
                                                entity=self.entity)
            self.__cursor.execute(new_command, __combine_args_and_kwargs(args, kwargs))
            return self.__cursor.fetchall()

        return wrapper

    return decorator


def Insert(func):  # noqa
    """插入装饰器，无需外部实现sql"""

    def wrapper(self, entity):
        """entity参数是传入的数据类实例
        而self.entity的数据类
        """

        # 获取entity类的属性名和类型
        fields = [field_name for field_name, _ in self.entity.__annotations__.items()]

        # 过滤掉有自增主键约束的属性
        fields = [field_name for field_name in fields
                  if Constraint.auto_primary_key[0]
                  not in get_constraint_from_field(getattr(self.entity, field_name, None))]

        sql_command = f"insert into {self.entity.__name__} " \
                      f"({', '.join(field_name for field_name in fields)}) " \
                      f"values ({', '.join('?' for _ in fields)});"
        # 判断传入的参数是否是数据类的实例
        if isinstance(entity, self.entity):
            values = [getattr(entity, field_name) for field_name in fields]
        else:
            # 如果不是，抛出一个类型错误异常
            raise TypeError(f"传入参数类型和Entity不一致，应传入 {self.entity.__name__} 实例")

        self.__cursor.execute(sql_command, values)
        return self.__cursor.lastrowid

    return wrapper


# ====================================================================================================================
# 新增方法
def update_cursor(self, cursor):
    """更新dao中的游标"""
    self.__cursor = cursor


def get_sql_create_table(self):
    """自动实现的建表语句"""
    table_name = self.entity.__name__.lower()
    # 获取字段名称和类型的字典
    fields = self.entity.__annotations__

    field_definitions = []
    foreign_key_constraints = []

    for field_name, field_type in fields.items():
        # 获取字段的SQL类型
        sql_type = __get_sql_type(field_type)
        # 获取描述符对象，即字段的约束条件
        field_value = getattr(self.entity, field_name, None)
        constraints = get_constraint_from_field(field_value=field_value)

        foreign_key_constraint = [item for item in constraints
                                  if isinstance(item, tuple)]
        constraints = [item for item in constraints
                       if item not in foreign_key_constraint]
        # 有外键
        if len(foreign_key_constraint) == 1:
            foreign_key_constraint = __get_foreign_key(field_name=field_name,
                                                       constraint=foreign_key_constraint[0])
            foreign_key_constraints.append(foreign_key_constraint)

        elif len(foreign_key_constraint) > 1:
            raise TypeError('一个属性只能指定一个外键')

        # 合并其他约束条件
        constraint = " ".join(constraints)

        # 拼接字段定义
        field_definition = f"{field_name} {sql_type} {constraint}"
        field_definitions.append(field_definition)
    # 将外键约束列表添加到字段定义列表的末尾
    field_definitions.extend(foreign_key_constraints)
    # 默认为严格的数据类型约束
    sql_create_table = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(field_definitions)});"
    return sql_create_table


@Insert
def insert(self, entity) -> int:  # noqa
    pass


# ====================================================================================================================
# 模块内使用的方法
def __get_sql_type(python_type):
    """转换python注释类型为sql类型"""
    if python_type in {int, bool}:
        return "INTEGER"
    elif python_type == str:
        return "TEXT"
    elif python_type == float:
        return "REAL"
    elif python_type == bytes:
        return "BLOB"

    raise ValueError(f"ysql不支持该python数据类型: {python_type}")  # noqa


def __get_foreign_key(constraint: tuple, field_name: str):
    """生成外键约束的sql语句"""
    foreign_key_entity, foreign_key_name, foreign_key_delete_link, foreign_key_update_link = constraint

    if foreign_key_delete_link is None and foreign_key_update_link is None:
        return f"FOREIGN KEY ({field_name}) " \
               f"REFERENCES {foreign_key_entity}({foreign_key_name})"

    # 存在表关联的情况
    elif foreign_key_delete_link is not None and foreign_key_update_link is None:
        return f"FOREIGN KEY ({field_name}) " \
               f"REFERENCES {foreign_key_entity}({foreign_key_name}) ON DELETE {foreign_key_delete_link}"
    elif foreign_key_delete_link is None and foreign_key_update_link is not None:
        return f"FOREIGN KEY ({field_name}) " \
               f"REFERENCES {foreign_key_entity}({foreign_key_name}) ON UPDATE {foreign_key_update_link}"
    elif foreign_key_delete_link is not None and foreign_key_update_link is not None:
        return f"FOREIGN KEY ({field_name}) " \
               f"REFERENCES {foreign_key_entity}({foreign_key_name}) " \
               f"ON DELETE {foreign_key_delete_link} ON UPDATE {foreign_key_update_link} "


def __combine_args_and_kwargs(*args):  # 不能传入**kwargs，这由调用条件决定了
    """一维展开不定参数，返回列表形式"""

    def flatten_args(arg):
        if isinstance(arg, (list, tuple)):
            # 如果是列表或元组，递归展开每个元素
            return [item for sublist in map(flatten_args, arg) for item in sublist]
        elif isinstance(arg, dict):
            # 如果是字典，取出所有值并递归展开
            return flatten_args(list(arg.values()))
        else:
            # 否则返回单个值
            return [arg]

    args_list = flatten_args(args)
    return tuple(args_list)


def __convert_entity_name(sql_command: str, entity):
    """将表名代替符替换为真正的表名"""
    if sql_command.count(TABLE_SUBSTITUTE) > 1:
        raise TypeError(f"sql语句非法使用了表名代替符：{TABLE_SUBSTITUTE}")

    return sql_command.replace(TABLE_SUBSTITUTE, entity.__name__.upper())
