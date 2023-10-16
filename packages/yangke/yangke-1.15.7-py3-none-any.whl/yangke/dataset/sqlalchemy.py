import datetime
import traceback
from typing import Any

import pandas as pd
import sqlalchemy.sql.dml
from sqlalchemy import create_engine, MetaData, Column, inspect, Table, String, text, insert, delete, update, select
from sqlalchemy.dialects.mysql import INTEGER, DOUBLE, BIGINT, VARCHAR, CHAR, TEXT, DATETIME
from sqlalchemy.engine import Engine, Row
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, Query
from sqlalchemy.sql import Select

from yangke.common.config import logger

# # 创建基类, 使用ORM方式操作数据库是继承该类
Base = declarative_base()
# noinspection all
修改时间记录表 = 'modify_time'


class YkTable(Table):
    def __init__(self, name, metadata, columns=None):
        if columns is None:
            columns = []
        super().__init__(name, metadata, *columns)


class YkColumn(Column):
    def __init__(self, name, dtype, primary_key=False, nullable=False):
        """
        Sqlite数据库不只是foreignKey关键字
        """
        super().__init__(name, dtype, primary_key=primary_key, nullable=nullable)


# class Base(Base_):
#     __tablename__ = "default"  # 也可以是 __tablename__
#
#     def __init__(self):
#         # super().__init__()
#         ...


class ModifyTime(Base):
    """
    用来记录数据库表格最后更新时间的表格，因为目前MySql和Sqlite数据库均无法查询表格的最后更新时间，因此使用数据库表格记录所有表格的最后更新
    时间
    """
    __tablename__ = 修改时间记录表
    table = Column(String(50), nullable=False, primary_key=True)  # autoincrement=True
    datetime = Column(DATETIME, nullable=False)

    def __init__(self, table, date_time):
        self.table = table
        self.datetime = date_time

    def __repr__(self):
        return f"ModifyTime(table={self.table}, 修改时间={self.datetime})"


class SqlOperator:
    def __init__(self, engine: Engine = None):
        """
        SQL数据库操作类，同时支持MySql和Sqlite数据库，使用示例：
        engine = create_engine("mysql+mysqlconnector://root:password@localhost:3306", pool_recycle=7200)
        engine = create_engine('sqlite:///stocks.db', echo=True)
        so = SqlOperator(engine=engine)
        然后可以调用so的增删改查等方法，所有方法均同时支持MySql和Sqlite数据库

        可能遇到的问题：
        1.sqlalchemy.exc.InterfaceError: (mysql.connector.errors.InterfaceError) 2003: Can't connect to MySQL server on
        'disk.yangke.site:3306' (10060 由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。)
        解决方法： 不使用mysqlconnector连接，pip install mysql后使用：create_engine("mysql://root:password@localhost:3306")
        """
        # 创建数据库引擎，ps:这里并没有连接具体数据库
        # engine = create_engine("mysql+mysqlconnector://root:password@localhost:3306/db?charset=utf8", pool_recycle=7200)

        # 连接时，如果报Character set 'utf8' unsupported错误，且数据库文件中没有非ascii字符，可以尝试切换charset的值。
        # 已知charset可取值包括(ascii, utf8, utf8mb4, gbk, cp1250)，可以执行show collation语句查看mysql数据库支持的字符集。

        self.engine = engine
        self.insp = inspect(self.engine)
        self.meta_data = MetaData()  # 兼容sqlalchemy 2.0版本的写法，bind参数写在reflect()方法中
        self.meta_data.reflect(bind=engine)
        self.session = sessionmaker(bind=engine)()  # 使用sessionmaker保持数据库会话连接
        self.base = Base
        self.connect = self.engine.connect()

    def create_table(self, table_name, columns):
        """
        创建数据库表，如果同名表存在，会报错
        示例1：
        self.create_table(table_name=f"daily{symbol}",
                          columns=[
                              YkColumn('trade_date', DATE(), primary_key=True),
                              YkColumn('open', Float()),
                              YkColumn('high', Float()),
                              YkColumn('low', Float()),
                              YkColumn('close', Float()),
                              YkColumn('vol', Float()),
                              YkColumn('amount', Float()),
                          ])
        """
        table = Table(table_name, self.meta_data, *columns)
        logger.debug(f"创建表格")
        table.create(bind=self.connect)  # bind=self.engine时，部分情况下会卡住

    def create_all_base_table(self):
        """
        创建所有继承自Base类的Python类的映射数据库表。也就是说，只要定义了继承自本模块中Base类的类，则该类会被映射成一个数据库表，
        本方法会自动创建所有映射的数据库表。
        """
        self.base.metadata.create_all(self.engine)

    def get_type_of_column(self, table_name=None, column_name=None):
        """
        获取mysql表中字段的类型，如果不设置column_name则返回所有的字段类型
        :param table_name:
        :param column_name: 为空则依次返回所有列的类型，封装为一个列表
        :return:
        """
        cols = self.insp.get_columns(table_name)
        res = None
        if column_name is None:
            res = {}
            for col in cols:
                res.update({col["name"]: col["type"]})
        else:
            for col in cols:
                if col["name"] == column_name:
                    res = col["type"]
                    break
        return res

    def get_column_names(self, table_name):
        """
        获取表格中的列名，返回列名列表
        """
        cols = self.insp.get_columns(table_name)
        res = [col["name"] for col in cols]
        return res

    def get_update_time_of_table(self, table_name):
        """
        获取表的最后更新时间
        """
        if self.has_table(table_name):
            # 查询modifyTime表，modifyTime表中记录了所有表格的最后更新时间
            if self.has_table(修改时间记录表):
                table: Table = self.get_table(修改时间记录表)
                select: Select = table.select().where(table.c.table == table_name)  # 构建一个选择语句
                res = self.session.execute(select)  # 执行选择语句并获取结果
                res = res.fetchone()
                if res is None:
                    return None
                return res.datetime  # 改写法兼容sqlalchemy1.4和2.0
                # return res["datetime"]  # 改写发不兼容sqlalchemy2.0
            else:
                return None
        else:
            return None

    def update_update_time_of_table(self, table_name):
        """
        更新表的最后更新时间
        """
        if not self.has_table(修改时间记录表):
            self.create_all_base_table()

        now = datetime.datetime.now()
        if self.exists_in_table(table_name=修改时间记录表, col_name='table', value=table_name):
            # stmt = update(table).where(table.c.table == table_name).values(datetime=now)  # 兼容写法
            # self.connect.execute(stmt)
            self.update_item(table_name=修改时间记录表, conditions={"table": table_name}, values={"datetime": now})
        else:
            self.session.add(ModifyTime(table_name, now))
        self.session.commit()

    def exists_in_table(self, table_name: str = None, col_name: str = None, value: str = None,
                        condition_dict: dict = None,
                        return_result: bool = False):

        """
        表tableName中是否存在列col_name的值位value的行

        :param table_name: 表名
        :param col_name: 列名
        :param value: 列的值
        :param condition_dict: 查询的键值对字典值，优先于col_name和value传入的值，即会覆盖col_name和value传入的值
        :param return_result: 是否需要返回查找到的数据行，如果为真，则返回所有符合查找条件的数据行
        :return:
        """
        if return_result:
            first_or_all = 'all'
        else:
            first_or_all = 'first'

        condition_dict = condition_dict or {}
        if col_name is not None and value is not None:
            condition_dict.update({col_name: value})

        res = self.select_item(table_name, condition_dict, first_or_all=first_or_all)
        if res is not None:
            return True
        else:
            return False

    def select_in_table(self, table_name=None, condition_dict: dict = None, result_col: list | str = None, limit=10,
                        offset=0,
                        fuzzy=False, first_or_all="first", result_type=None, cls=None, **kwargs) -> Row | list | Any:
        """
        查

        精确查询，设置fuzzy为True，且condition_dict中的value为字符串值
        模糊查询，设置fuzzy为False，日期列不能使用模糊查询，只能使用范围查询
        范围查询，设置fuzzy为True，且condition_dict中的value为长度为2的列表，列表第一、二项分别为范围下、上限，且包含上下限

        当result_type=="json"时，返回的是一个list(dict)的json对象，即[{col1: value1, col2: value2,...}, ...}的json对象
        列表的每一项对应一条匹配的查询结果
        每一项的字典分别是{列名：值}

        kwargs={"date_format": "%Y-%m-%d %H:%M:%S"} 如果mysql中存在日期列，需要将日期转换为字符串，该参数定义日期字符串格式

        示例1：
        fetch = self.sql.select_in_table(cls=Holiday, condition_dict={"calendarDate": day_datetime},
                                         result_col=['isOpen'])

        :param table_name: 当使用传统查询方式时，需要传入数据库表名
        :param cls: 当使用ORM模型时，只需要传入数据库表在python中对应的映射类名，如果通过该方法查询，则查询到的数据会被自动转换为cls对象
        :param condition_dict:
        :param result_col: 不传入或传入空列表，则返回数据库中所有列
        :param limit:
        :param offset:
        :param fuzzy: 是否模糊查询
        :param first_or_all: 返回满足条件的第一个还是所有，支持"first", "all",
        :param result_type: 返回类型，如果为json，则返回为json格式的字符串
        :return: None或查询的列值列表或数据条的列表或sqlalchemy.engine.Row对象，出错时返回None，如列明不存在等；否则返回一个tuple类型的数据，长度为0表示未查询到满足条件的数据
        """
        # ---------------------- 如果使用table_name查询，则构建Table对象 ------------------------
        # Table对象可以当cls一样使用
        if cls is None:
            if self.has_table(table_name):
                table: Table = self.get_table(table_name)
                if table is None:
                    return None
                cls = table
        # ---------------------- 如果使用table_name查询，则构建Table对象 ------------------------
        # ----------------------- 根据条件字典，构建查询条件 --------------------------------
        if condition_dict is None:  # 查询表格中某列的所有值
            if result_col is None:
                return
            elif isinstance(result_col, str):
                res = self.session.execute(select(cls.c.get(result_col))).fetchall()
                res = [i._data[0] for i in res]
            else:  # list
                n = len(result_col)
                _1 = []
                for i in range(n):
                    _1.append(f"cls.c.get(result_col[{i}])")
                _2 = ",".join(_1)

                _3 = f"select({_2})"
                try:
                    _4 = eval(_3)
                    res = self.session.execute(_4).fetchall()
                    res = [i._data for i in res]
                except:
                    traceback.print_exc()
                    logger.error(f"检查返回列的名称是否正确：{result_col=}")
                    res = None
            return res
        # condition = []
        # for col, val in condition_dict.items():
        #     if isinstance(val, datetime.datetime) or isinstance(val, datetime.date):
        #         condition.append(f"{col}={val.__repr__()}")
        #     else:
        #         condition.append(f"{col}='{val}'")
        # condition = ",".join(condition)
        # ----------------------- 根据条件字典，构建查询条件 --------------------------------

        # .filter_by(node=node, password=password).all()  # filter()不支持组合查询，filter_by支持
        # _: Query = self.session.query(cls)
        # expression = f"_.filter_by({condition})"
        # _: Query = eval(expression)
        # item = eval(f"_.{first_or_all}()")

        _1 = []
        vals = []
        i = 0
        for k, v in condition_dict.items():
            vals.append(v)  # 为了兼容v为datetime或date类型的参数
            _1.append(f"cls.c.{k}==vals[{i}]")
            i += 1
        _2 = ",".join(_1)

        _3 = f"select(cls).where({_2})"
        items = self.session.execute(eval(_3)).fetchall()
        if len(items) == 0 or items is None:
            return None
        if first_or_all == "first":
            item = items[0]
        else:
            item = items

        # ------------------------ 如果指定了返回的数据列，则取出数据列并返回 -----------------------
        if isinstance(item, str):
            item = [item]
        if item is None or len(item) == 0:
            return item
        else:
            try:
                if isinstance(item, Row):  # item是个sqlalchemy.engine.row.Row对象，如读取Holiday表时会出现该情况
                    if result_col is None:
                        return item
                    elif isinstance(result_col, str):
                        # sqlalchemy2.0中，item.__getattr__(result_col)语法是正确的
                        # sqlalchemy1.4中，item.__getitem__(result_col)语法是正确的
                        res = eval(f"item.{result_col}")  # 该写法兼容sqlalchemy2.0
                        return res
                    elif isinstance(result_col, list) and len(result_col) == 1:
                        res = eval(f"item.{result_col[0]}")  # 该写法兼容sqlalchemy2.0
                        return res
                # noinspection all
                _ = [getattr(item, col) for col in item]  # table_name和cls两种方法都适用
                if len(_) == 1:
                    _ = _[0]
                return _
            except AttributeError:
                logger.error(item)
        # ------------------------ 如果指定了返回的数据列，则取出数据列并返回 -----------------------

    def select_item(self, table_name=None, condition_dict: dict = None, result_col: list | str = None, limit=10,
                    offset=0, first_or_all="first",
                    fuzzy=False, result_type=None):
        """
        查

        精确查询，设置fuzzy为True，且condition_dict中的value为字符串值
        模糊查询，设置fuzzy为False，日期列不能使用模糊查询，只能使用范围查询
        范围查询，设置fuzzy为True，且condition_dict中的value为长度为2的列表，列表第一、二项分别为范围下、上限，且包含上下限

        当result_type=="json"时，返回的是一个list(dict)的json对象，即[{col1: value1, col2: value2,...}, ...}的json对象
        列表的每一项对应一条匹配的查询结果
        每一项的字典分别是{列名：值}

        kwargs={"date_format": "%Y-%m-%d %H:%M:%S"} 如果mysql中存在日期列，需要将日期转换为字符串，该参数定义日期字符串格式

        示例1：
        fetch = self.sql.select_in_table(cls=Holiday, condition_dict={"calendarDate": day_datetime},
                                         result_col=['isOpen'])

        :param table_name: 当使用传统查询方式时，需要传入数据库表名
        :param condition_dict:
        :param result_col: 不传入或传入空列表，则返回数据库中所有列
        :param limit:
        :param offset:
        :param fuzzy: 是否模糊查询
        :param first_or_all: 返回满足条件的第一个还是所有，支持"first", "all",
        :param result_type: 返回类型，如果为json，则返回为json格式的字符串
        :return: None或查询的列值列表或数据条的列表或sqlalchemy.engine.Row对象，出错时返回None，如列明不存在等；否则返回一个tuple类型的数据，长度为0表示未查询到满足条件的数据
        """
        return self.select_in_table(table_name=table_name, condition_dict=condition_dict, result_col=result_col,
                                    limit=limit, offset=offset,
                                    fuzzy=fuzzy, first_or_all=first_or_all, result_type=result_type)

    def update_item(self, table_name, conditions: dict, values):
        """
        self.update_item('user', {"id": 1}, values={"name": "Tom"})

        兼容sqlalchemy 1.4及2.0以上版本。
        query.filter()或query.filter_by()的写法无法同时兼容sqlalchemy 1.4和2.0版本

        Parameters
        ----------
        table_name
        conditions: 数据表的索引列的值，必须唯一确定某一个记录
        values: 数据表中其他列的值，可以只设置部分列的值

        Returns
        -------

        """
        table: Table = self.get_table(table_name)
        # _1 = self.session.query(table)
        update_obj = update(table)
        for col_title, col_value in conditions.items():
            update_obj = update_obj.where(table.c.get(col_title) == col_value)  # 兼容写法

        dict_str = "{"
        objs = []
        i = 0
        for title, value in values.items():
            # if isinstance(value, datetime):
            #     dict_str = f"{dict_str}table.c.{title}: value,"
            objs.append(value)
            dict_str = f"{dict_str} table.c.{title}: objs[{i}],"  # 这样的写法是为了解决value是datetime或date类型时的兼容写法
            i += 1
        dict_str += "}"
        values = eval(dict_str)
        update_obj = update_obj.values(values)
        self.session.execute(update_obj)
        self.session.commit()

    def get_primary_col(self, table_name):
        """
        获取表的主键

        Parameters
        ----------
        table_name

        Returns
        -------

        """
        table = self.get_table(table_name)
        if isinstance(table, Table):
            # noinspection all
            for col in table.columns:
                if col.primary_key:
                    return col
        return None

    def insert_dataframe(self, table_name, df: pd.DataFrame, if_exists="append", index=False, dtype=None):
        """
        将DataFrame对象写入数据库中。兼容mysql和sqlite。df对象可以包含数据库中不存在的列，该方法会忽略这些列。

        pandas的to_sql方法存在以下问题：1.表格存在时，如果使用replace，则新创建的表的主键会丢失；2.append时会报重复键错误；

        批量插入数据时，
        简单说明：同样添加10W行数据，插入时间比
        1，Session.add(obj)   使用时间：6.89754080772秒
        2，Session.add(obj)注意：手动添加了主键id   使用时间：4.09481811523秒
        3，bulk_save_objects([obj1, obj2])   使用时间：1.65821218491秒
        4，bulk_insert_mappings(DBmodel, [dict1, dict2])  使用时间： 0.466513156781秒
        5，SQLAlchemy_core(DBmodel.__table__insert(), [dict1, dict2]) 使用时间：0.21024107933秒
        6，直接执行execute(str_sql_insert)  直接执行sql插入语句 使用时间：0.137335062027秒
        ————————————————
        版权声明：本文为CSDN博主「DHogan」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
        原文链接：https://blog.csdn.net/dongyouyuan/article/details/79236673

        Parameters
        ----------
        table_name
        df
        if_exists: 参数参加pandas.DataFrame().to_sql()方法，可取值append, replace, fail
        index
        dtype : 指定df中各列的数值类型

        Returns
        -------

        """
        if self.has_table(table_name):  # 逐条插入，只要表存在，则不要使用pandas的to_sql方法，因为to_sql方法会覆盖原表，导致丢失主键
            primary_col = self.get_primary_col(table_name)
            primary_key = primary_col.name
            items_exist = self.select_item(table_name, result_col=primary_key)  # 获取数据库中表现有的数据记录的唯一标记
            if isinstance(items_exist, list):
                table: Table = self.get_table(table_name)
                # ---------------------- 判断需要插入的和需要更新的数据 ---------------------------
                df = df.fillna(0)  # 有些股票的交易量为nan，例如600607的1993-12-23日的交易量为nan
                df['new'] = df.apply(func=lambda row: False if row[primary_key] in items_exist else True, axis=1)
                # 2.0版本需要将Timestamp转换为str类型，pandas中的字符串在插入数据库时，会由str强制转换成DATE类型
                if len(df) > 0:
                    row1: pd.Series = df.iloc[0]  # df中的第一个记录
                    for title, value in row1.items():
                        if isinstance(value, pd.Timestamp):
                            df[title] = df[title].astype(str)

                df_new = df[df['new']]
                df_old = df[df['new'] == 0]  # 已存在的数据，视情况忽略或更新，0==False
                # ---------------------- 判断需要插入的和需要更新的数据 ---------------------------

                # ---------------------- 判断是否需要执行插入操作 ---------------------------------
                if if_exists == "append":  # 存在的数据不操作，只添加不存在的数据
                    if len(df_new) == 0:  # 如果只是追加不存在的数据，且插入的数据全部存在，则无须执行插入操作
                        return
                # ---------------------- 判断是否需要执行插入操作 ---------------------------------

                cols_table = self.get_column_names(table_name)

                # 按数据库表的列顺序排列dataframe列，无论if_exists取replace还是append，都要插入新值
                values_new = [dict(zip(cols_table, item)) for _, item in df_new[cols_table].iterrows()]
                try:
                    self.session.execute(table.insert(), values_new)  # 该方法速度仅次于直接执行sql语句，尽量使用该方法

                    if if_exists == "replace":  # 如果存在的数据需要替换
                        values_old = [dict(zip(cols_table, item)) for _, item in df_old[cols_table].iterrows()]
                        # self.session.bulk_update_mappings(table, values_old)
                        self.session.execute(table.update(), values_old)
                except:
                    traceback.print_exc()
                    logger.debug(f"{table=}, {values_new=}")
            else:
                logger.warning("未处理的数据插入")
        else:
            # 插入大数据量是特别慢，尤其是数据库已有重复记录时
            logger.warning(f"df.to_sql方法创建的表{table_name}没有主键，建议先创建表后，再插入数据")
            df.to_sql(table_name, self.engine, if_exists=if_exists, index=index)  # 该方法设置的数据库表没有主键

    def insert_item(self, table_name: str = None, values: list = None,
                    col_names: list = None, ignore=False,
                    replace=False, filter_warning=None):
        """
        向数据库中插入数据，这里传入的列名不要用反引号括起来，增

        values中的数据类型需要与表中每列的数据类型一致，数据库和python中数据类型对应如下：
        SqlAlchemy          python
        DATETIME            datetime.datetime/datetime.date
        VARCHAR             str

        cols_names和values两个列表一一对应。

        :param table_name: 表名
        :param values:
        :param col_names: 列名，如果是插入带有auto_increment属性的表数据，则必须指定列名，否则就需要指定auto_increment属性的字段的值
        :param ignore: 当插入数据重复时，是否忽略
        :param replace: 当插入数据重复时，是否替换，ignore和replace不能同时为True
        :param filter_warning: 过滤警告信息，[1062, 1265, 1366]，分别对应["Duplicate", "Data truncated", "Incorrect integer value"]
        """
        _: Table = self.get_table(table_name)

        # ------------------ 该段语句在sqlite服务器上测试成功，但mysql5.6服务器上测试数据不更新 -------------------
        # if col_names is None:
        #     col_names = self.get_column_names(table_name)
        # paras = []
        # for col, val in zip(col_names, values):
        #     if isinstance(val, datetime.datetime) or isinstance(val, datetime.date):
        #         val = val.__repr__()
        #         paras.append(f"{col}={val}")
        #     else:
        #         paras.append(f"{col}='{val}'")
        # paras = ",".join(paras)
        # state = f"_.insert().values({paras})"
        # eval(state)
        # self.session.commit()
        # ------------------ 该段语句在sqlite服务器上测试成功，但mysql5.6服务器上测试数据不更新 -------------------

        # ------------------ mysql5.6以下语句测试成功 -------------------------------
        if replace:
            columns = ""
            self.insert_item()
        else:
            ins = _.insert(values=dict(zip(col_names, values)))
            self.connect.execute(ins)
            self.session.commit()

    def has_table(self, table_name):
        """
        判断数据库中是否存在某个表
        """
        # return self.engine.has_table(table_name) # 该写法不兼容sqlalchemy 2.0版本
        return self.engine.dialect.has_table(self.engine.connect(), table_name)  # 该写法兼容sqlalchemy1.4和2.0版本

    def exist_table(self, table_name):
        """
        同has_table()
        """
        return self.has_table(table_name)

    def get_table(self, table_name=None):
        """
        获取表名为table_name的表对象，返回的是 Table()对象。
        如果不传入table_name，则返回数据库中的所有表，返回的是Table()对象的列表。
        """
        tables = [i for i in self.meta_data.tables.values()]
        if table_name is not None:
            for table in tables:
                if table.name == table_name:
                    return table
            return None
        return [i for i in self.meta_data.tables.values()]
