"""
定义全局变量的模块
程序使用的所有全局变量定义在这里
python模块自动是单例模式，因此，在多个py文件中引用该模块，多个py模块中的变量对象是同一个
"""
from yangke.stock.dataset.tushareData import StockData
import argparse
import os
import pickle
from pymysql.cursors import Cursor
from sqlalchemy.engine.base import Engine

namespace = argparse.Namespace()


class GlobalVar:
    def __init__(self, encoding='utf8', data_folder=None, tsd: StockData = None, cmd=None,
                 symbol=None, storage=None):
        self.encoding = encoding
        self.data_folder = data_folder  # 股票数据存储的目录
        self.tsd = tsd  # StockData类的对象，其构造函数会初始化tushare账户的口令
        self.cmd = cmd  # 调用程序的命令
        self.symbol = symbol  # 操作哪只股票，symbol对应股票代码
        self.storage = storage  # 数据的存储方式，默认是mysql，也可以取值为"file"，表示本地存储


class RunState:
    """
    储存一些软件运行状态参数
    """

    def __init__(self, last_update_time=None, stocks=None):
        # -------------- 最后更新的股票列表和更新时间 ----------------
        self.stocks = stocks
        self.last_update_time = last_update_time
        # -------------- 最后更新的股票列表和更新时间 ----------------

        folder = os.path.join(dataDirectory, 'state')
        self.file = os.path.abspath(os.path.join(folder, 'RunState'))

    def load(self):
        if os.path.exists(self.file):
            with open(self.file, 'rb') as f:
                state = pickle.load(f)
        else:
            return self
        return state

    def dump(self):
        os.makedirs(os.path.dirname(self.file), exist_ok=True)
        with open(self.file, 'wb') as f:
            pickle.dump(self, f, 0)

    def __repr__(self):
        return str(self.__dict__)

    def __str__(self):
        return str(self.__dict__)


def test():
    state = RunState()
    state.__setattr__('code', 'updated')  # 可以动态向RunState中添加属性
    print(state)

    state.dump()

    state1 = RunState().load()
    print(state1)
