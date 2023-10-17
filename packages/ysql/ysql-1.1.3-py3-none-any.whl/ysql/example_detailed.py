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
# Dao定义数据操作接口，提供表级控制
# Database集成Dao便于统一对外，提供库级控制


# ====================================================================================================================
# 数据表类的定义形式
@Entity  # 两个装饰器的位置先后可任意
@dataclass  # 显式的使用dataclass装饰器，可以在IDE中获取代码补全
class Student:  # 类名即表名
    picture: bytes
    name: str = Constraint.not_null, Constraint.unique  # 用逗号分个多个约束
    weight: float = 50, Constraint.not_null  # 若该字段存在默认值，同样以逗号分隔，但仅支持int、float、str、bytes类型的默认值；或者使用Constraint.default()实现约束
    student_id: int = Constraint.auto_primary_key


@Entity
@dataclass
class Score:
    score: float
    student_id: int = Constraint.auto_primary_key, \
                      Constraint.foreign_key(entity=Student,
                                             field='student_id',
                                             delete_link=Constraint.cascade,
                                             update_link=Constraint.set_default)  # 设置外键的具体约束


# ====================================================================================================================
# Dao类的定义形式
@Dao(entity=Student)  # 使用Dao装饰器，并传递对应的entity类
class DaoStudent:

    # 内置insert(entity)方法的返回值为刚插入记录的row id
    # 缺点是在IDE的自动补全无法提示该方法的存在
    # @Insert  # 如需重新定义插入方法，可使用sql装饰器并传递相应的sql语句，或者直接使用Insert装饰器，也可自动实现。
    # def insert(self, entity):
    #   pass
    # 如果使用了@Insert（包括内置的insert方法），被装饰方法会自动返回插入记录的主键

    @Sql("select * from student where student_id=? and name=?;")  # 对方法使用Sql装饰器，并传入sql语句即可
    def get_student(self, student_id, name):  # 参数名可任意，但顺序需要与sql语句中?的传值顺序一致
        pass  # 方法本身无需实现
        # 使用select的时候返回结果为list[named_tuple]，其中每条记录会自动解析为具名元组。


@Dao(entity=Score)  # 也可直接传入对应的entity
class DaoScore:

    # 涉及使用对应entity的表名时，可以使用__代替符，但相应的不允许sql语句在其他位置使用__字符。
    @Sql(f"select * from __ where student_id=?;")
    def get_score(self, student_id):
        pass  # 方法本身无需实现


# ====================================================================================================================
# 数据库类的定义形式
db_path = "db_folder/test_detailed.db"  # 此处是需要每次运行均删除数据库，故额外定义路径变量
@Path(db_path)  # 使用Path装饰器传递数据库的路径，可直接传路径字符串
class MyDatabase(MetaDatabase):  # 还需额外继承MetaDatabase类，原因是若采用装饰器实现，则无法获得自动补全的方法提示，查看MetaDatabase源码了解外部可调用的方法
    # 需将全部Dao类分别定义为类中静态变量，以便集成Dao到一个数据类中对外访问
    dao_student = DaoStudent()
    dao_score = DaoScore()


if __name__ == '__main__':
    # 删除已存在的数据库文件，方便每次重置
    if os.path.exists(db_path):
        os.remove(db_path)

    db = MyDatabase()
    db.connect()
    db.create_tables()

    db.dao_student.insert(Student(name="好家伙", picture=b'1235'))  # 插入一条student记录
    db.dao_score.insert(Score(score=59.5, student_id=1))  # 插入一条score记录
    db.commit()  # 提交改动

    result1 = db.dao_student.get_student(student_id=1, name='好家伙')  # 获取一条student记录
    result2 = db.dao_score.get_score(student_id=1)

    # 查询结果以列表形式返回
    print(f"查询结果1：{result1}\n查询结果2：{result2}")

    # 查询结果的单条记录为具名元组
    for result in result1:
        print(f"结果1中的姓名：{result.name}；图片：{result.picture}")

    db.disconnect()  # 关闭数据库连接
