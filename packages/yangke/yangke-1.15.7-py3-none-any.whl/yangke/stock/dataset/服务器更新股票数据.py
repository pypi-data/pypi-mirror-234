"""
本模块用于更新mysql服务器中的数据
"""
from yangke.dataset.sqlalchemy import SqlOperator
from sqlalchemy import create_engine
from yangke.base import execute_function_every_day
from yangke.stock.Project import Project


class UpdateDataBase:
    def __init__(self, ip, port, user, passwd, db):
        self.ip = ip
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db
        self.project = Project(settings={
            "storage": "Mysql数据库",
            "db_name": self.db,
            "db_user": self.user,
            "db_passwd": self.passwd,
            "db_ip": self.ip,
            "db_port": self.port,
        })

        self.tsd = self.project.tsd

    def update(self):
        """
        更新一次股票数据
        """
        # stocks = self.tsd.get_all_stock_basic_info()
        self.tsd.download_all_stocks()

    def start(self):
        execute_function_every_day(self.update, hour=18, minute=0)


if __name__ == "__main__":
    # udb = UpdateDataBase(ip="182.43.65.44", port=3306, user="stock", passwd="admin", db="stock")
    udb = UpdateDataBase(ip="disk.yangke.site", port=3306, user="stock", passwd="123456", db="stock")
    udb.update()
