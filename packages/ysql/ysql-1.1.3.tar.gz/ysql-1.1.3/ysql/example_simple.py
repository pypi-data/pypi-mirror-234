# -*- coding: utf-8 -*-
import os
from dataclasses import dataclass

from ysql import Dao, Sql
from ysql import Path, MetaDatabase
from ysql import Entity, Constraint


# ====================================================================================================================
# 项目gitee地址：https://gitee.com/darlingxyz/ysql（请于此查看项目详细信息，如README文件）
# 如果直接下载源码使用，请将ysql文件夹放置在根目录中，与venv目录同级，否则需要重新导入其中各文件的依赖项
# 通过pip安装时，可以在任何py文件中运行以下代码来生成此示例文件
# from ysql import get_example
# get_example()
# ====================================================================================================================
# 结构说明：
# Entity定义数据表
# Dao定义数据表的操作接口，提供表级控制
# Database集成Dao便于统一对外，提供库级控制


# ====================================================================================================================
# 数据表类的定义形式
@Entity  # 使用Entity装饰器
@dataclass  # 指定为原生的dataclass数据类
class Student:
    score: float
    picture: bytes
    name: str = '好家伙', Constraint.not_null  # 同时设置默认值和约束，以逗号分开即可
    student_id: int = Constraint.auto_primary_key  # Constraint类提供多种字段约束，请查看源码了解


# ====================================================================================================================
# Dao类的定义形式
@Dao(Student)  # 通过Dao装饰器传入对应的数据类
class DaoStudent:
    # 已内置insert(entity)方法，可直接调用DaoStudent().insert(entity)，参数entity应为对应数据类的实例

    @Sql("select name, score, picture from student where student_id=?;")  # 通过Sql装饰器传递标准sql语句
    def get_student(self, student_id):
        pass  # 装饰器会自动实现该方法
        # 使用select的时候返回结果为list[named_tuple]，其中每条记录会自动解析为具名元组。


# ====================================================================================================================
# 数据库类的定义形式
db_path = "db_folder/test_simple.db"
@Path(db_path)  # 需通过Path装饰器传递数据库的路径
class MyDatabase(MetaDatabase):  # 需继承MetaDatabase类，请查看其源码了解可调用的方法
    dao_student = DaoStudent()  # 需将Dao类写为Database类的静态类变量，以便集成Dao到一个数据类中对外访问


if __name__ == '__main__':
    if os.path.exists(db_path):
        os.remove(db_path)

    db = MyDatabase()  # 创建数据库类的实例
    db.connect()  # 连接数据库
    db.create_tables()  # 创建表

    db.dao_student.insert(Student(name="好家伙", score=95.6, picture=b'1235'))  # 插入一条student记录
    db.commit()  # 提交改动

    result = db.dao_student.get_student(student_id=1)  # 获取一条记录
    # 查询结果以列表形式返回
    print(f"查询结果：{result}")

    db.disconnect()  # 关闭数据库连接
