# ysql框架

项目地址：[ysql (gitee.com)](https://gitee.com/darlingxyz/ysql)

### **1.开发环境**

|                IDE                 | 开发语言  | 主要使用 | 第三方库依赖 |
| :--------------------------------: | :-------: | :------: | :----------: |
| PyCharm Community Edition 2020.3.4 | Python3.9 | sqlite3  |      无      |

基于Python官方库实现的Sqlite数据库框架，借鉴了安卓Room框架的设计，进行了一些个人理解上的设计优化。



### 2.使用方式

**方式1**：通过pip安装

```
pip install ysql
```

然后在python中使用以下函数来获取示例文件

```
from ysql import get_example

get_example()
```

**方式2**：通过gitee下载项目源码，将ysql文件夹放置到项目根目录中，如使用pycharm则应与venv目录同级。



### 3.设计分析

![框架设计](asset/design.svg)

**Entity**：基于python内置的dataclass类和本框架定义的Entity装饰器共同实现。由于采取装饰器和使用元编程、描述符向该类中增添功能，但装饰后的数据类仍然是独立完整的dataclass，与其他结构解耦，可以单独使用。

**Dao**：通过Dao装饰器注册该类对应的Entity类；隐藏了cursor对象的使用，用户只需关心数据库的connection；对类方法提供了Sql装饰器，仅需传递sql语句，无需具体实现该方法；提供了insert装饰器以及默认的insert方法，可以直接插入对硬的数据类对象至数据库中。

**Database**：通过将Dao类写为类中静态变量来集成全部的Dao类，是对外访问的唯一接口；具体通过继承MetaDatabase，以及Path装饰器传递数据库路径实现（由于装饰器是动态生成属性，在静态开发的时候不利于IDE的自动补全，因此采取了继承的策略）。



### 4.特性介绍

**特性1**：整体操作分为表定义(Entity)、表操作(Dao)、库操作(Database)三种，由Entity到Dao再到Database，层层向上，不存在越级关系，模块解耦程度高。

**特性2**：Entity和Dao均采用装饰器方式实现，避免了大量的约定规则，仅需添加一行代码。

```python
@Entity  # 使用Entity装饰器
@dataclass  # 指定为原生的dataclass数据类
class Student:
    score: float
    picture: bytes
    name: str = '好家伙', Constraint.not_null  # 同时设置默认值和约束，以逗号分开即可
    student_id: int = Constraint.auto_primary_key  # Constraint类提供多种字段约束
```

**特性3**：Dao中实现了@Insert和@Sql两个装饰器。Dao类仅需定义方法名称和参数，并在@Sql装饰器中编写原生sql语句即可，Dao装饰器将自动实现其余代码。

```python
@Dao(Student)  # 通过Dao装饰器传入对应的数据类
class DaoStudent:
    # 已内置insert(entity)方法，可直接调用DaoStudent().insert(entity)，参数entity应为对应数据类的实例，返回值为刚插入记录的row id

    @Sql("select name, score, picture from student where student_id=?;")  # 通过Sql装饰器传递标准sql语句
    def get_student(self, student_id):
        pass  # 装饰器会自动实现该方法
        # 使用select的时候返回结果为list[named_tuple]，其中每条记录会自动解析为具名元组。
```

**特性4**：@Sql装饰器自动转换查询结果为具名元组，无论编写的sql语句查询的是*还是指定字段，@Sql将解析并转换各个查询字段名，并生成具名元组来存储单条记录（全部查询结果使用列表存储）。避免了在应用层直接使用结果元组或者字典，改动数据结构时可以大大降低对应用层的影响。



### 5.使用建议

![推荐编写结构](asset/advice.svg)

1.分文件编写各个Entity，可避免容易发生的引用问题。

2.将Entity与对应Dao写入同一文件中。

3.Dao类仅实现基础的操作方法，将复杂操作放至DataRepo中进行。



### 6.待开发

1.导出数据库结构，并实现表的可视化。

2.测试并解决Database单例模式和多线程的冲突。

3.完善异常捕捉。



**作者**：大风起兮呼呼呼

**邮箱**：dfqxhhh@163.com

**时间**：2023-9-9