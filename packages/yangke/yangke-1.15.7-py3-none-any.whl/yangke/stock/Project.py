from yangke.stock.dataset.tushareData import StockData


class Project:
    def __init__(self, settings=None, encoding='utf8', data_folder=None, cmd=None,
                 symbol=None, storage=None):
        if settings is not None and len(settings) > 0:
            self.encoding = settings.get("encoding")
            self.cmd = settings.get("cmd")
            self.symbol = settings.get("symbol")
            self.storage = settings.get("storage")  # 记录存储类型，可取值"Mysql数据库", "Sqlite数据库"或"本地目录"
            self.data_folder = settings.get("data_folder")  # 本地目录存储时需要
            self.db_name = settings.get("db_name")  # sqlite或mysql数据库存储时需要
            self.db_user = settings.get("db_user")  # mysql数据库存储时需要
            self.db_passwd = settings.get("db_passwd")  # mysql数据库存储时需要
            self.db_ip = settings.get("db_ip")  # mysql数据库存储时需要
            self.db_port = settings.get("db_port")  # mysql数据库存储时需要
        else:
            self.encoding = encoding
            self.data_folder = data_folder  # 股票数据存储的目录
            self.cmd = cmd  # 调用程序的命令
            self.symbol = symbol  # 操作哪只股票，symbol对应股票代码
            self.storage = storage or 'Sqlite数据库'  # 数据的存储方式，默认是mysql，也可以取值为"file"，表示本地存储
            self.data_folder = None  # 本地目录存储时需要
            self.db_name = None  # sqlite或mysql数据库存储时需要
            self.db_user = None  # mysql数据库存储时需要
            self.db_passwd = None  # mysql数据库存储时需要
            self.db_ip = None  # mysql数据库存储时需要
            self.db_port = None  # mysql数据库存储时需要
        self.tsd = StockData(self)  # StockData类的对象，其构造函数会初始化tushare账户的口令

    def to_dict(self):
        return {
            "encoding": self.encoding,
            "data_folder": self.data_folder,
            "tsd": self.tsd,
            "cmd": self.cmd,
            "symbol": self.symbol,
            "storage": self.storage,
            "db_name": self.db_name,
            "db_user": self.db_user,
            "db_passwd": self.db_passwd,
            "db_ip": self.db_ip,
            "db_port": self.db_port,
        }

    def set_storage(self, storage):
        self.tsd.storage = storage
        self.storage = storage

    def get_storage(self):
        return self.storage
