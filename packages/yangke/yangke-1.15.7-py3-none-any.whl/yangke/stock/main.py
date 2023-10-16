"""
股票功能的入口文件
"""
import os.path
import sys
import traceback
from datetime import datetime

from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
from pyecharts.options import CandleStickItem

from yangke.common.QtImporter import QtCore, Qt

import yangke.stock.globalVar as gv  # 所有的全局变量定义在该模块中，使用全局变量需要引入该模块
from yangke.common.config import logger
from yangke.stock.Project import Project
from yangke.stock.StockListView import StockItemDelegate
from yangke.common.crawler import start_scrapy_start

from yangke.common.qt import YkWindow, run_app, YkListViewWidget, YkInputPanel, YkDialog, YkItem, YkStandardItemModel, \
    html_widget, opts
from yangke.common.QtImporter import QComboBox, QFileDialog
from pyecharts.charts import Candlestick, Bar


class MainWindow(YkWindow):
    def __init__(self):
        super().__init__()  # 170, 124, 1244, 786
        if len(self.proj) > 0:
            self.project = Project(self.proj)
        else:
            self.project = Project()
        # self.enable_input_panel()
        self.symbols = self.get_stock_symbols()

        # ---------------------------- 初始化股票列表页 ------------------------------
        infos = self.get_stock_basic_infos()
        list_model = []
        for idx, row in infos.T.items():
            _ = {"name": row["symbol"], "名称": row["name"]}
            list_model.append(_)
        self.symbols_model = YkStandardItemModel(list_model)
        self.stock_list_lv = YkListViewWidget(self.symbols_model)
        self.stock_list_lv.setItemDelegate(StockItemDelegate())
        # noinspection all
        self.stock_list_lv.add_item_clicked_listener(self.stock_lv_item_clicked)
        self.add_panel("股票列表", self.stock_list_lv)
        # ---------------------------- 初始化股票列表页 ------------------------------

        self.start_ws_server()
        self.temp_ = None  # 用于传递临时数据的参数
        # self.add_content_tab(widget=html_widget(
        #     local_file=r"D:\PycharmProjects\lib4python\yangke\stock\ui\echarts\index.html"),
        #     tab_name="chart", replace=True)

    def stock_lv_item_clicked(self, index: QtCore.QModelIndex):
        """

        """

        # ------------------------- 获取股票的日线数据 ------------------------------------
        if isinstance(index, str):
            code = index
            name = self.project.tsd.get_name(code)
        else:
            data = index.data(Qt.UserRole)
            code = data.get("name")
            name = data.get("名称")
        df = self.project.tsd.download(code=code)
        df.sort_values(by='trade_date', inplace=True)
        # ------------------------- 获取股票的日线数据 ------------------------------------
        # ------------------------- 绘制K线图 ------------------------------------
        # x_data = df["trade_date"].apply(lambda x: str(x)[:10]).tolist()
        # y_data = df[["open", "close", "low", "high"]].values.tolist()
        df["sign"] = df.apply(lambda r: 1 if r['close'] >= r['open'] else -1, axis=1)  # 是否涨
        self.start_ws_server()
        _send_data = df[["trade_date", "open", "high", "low", "close", "vol", "sign"]].copy()
        _send_data['trade_date'] = _send_data['trade_date'].apply(lambda e: str(e)[:10])
        self.echarts_update_data({"data": _send_data})

        # ------------------------- 绘制K线图 ------------------------------------

    def get_stock_symbols(self):
        """
        获取A股所有的股票列表
        """
        symbols = self.project.tsd.get_all_stock_basic_info()
        return list(symbols['symbol'])

    def get_stock_basic_infos(self):
        info = self.project.tsd.get_all_stock_basic_info()
        return info

    def refresh(self):
        """
        刷新股票列表
        """
        infos = self.get_stock_basic_infos()
        list_model = []
        for idx, row in infos.T.items():
            _ = {"name": row["symbol"], "名称": row["name"]}
            list_model.append(_)
        self.symbols_model.update_item(list_model)

    def set_storage(self):
        """
        设置数据存储的位置
        """
        _ = os.path.abspath(os.path.join(os.path.dirname(__file__), "ui", "ui_panel.yaml"))
        input_panel = YkInputPanel(from_file=_, domain="set_storage", parent=self)
        dialog = YkDialog(self, widget=input_panel)
        dialog.set_size(400, 500)
        input_panel.apply_btn_connect()
        self.temp_ = {"input_panel": input_panel, "dialog": dialog}

        if self.project.storage is not None:
            box: QComboBox = input_panel.get_item("保存类型").value
            box.setCurrentIndex(0)
            box.setCurrentText(self.project.storage)

        # engine = create_engine(r'sqlite:///C:\path\to\foo.db')
        # self.storage = engine

    def _change_storage_type(self):
        input_panel: YkInputPanel = self.temp_.get("input_panel")
        type_ = input_panel.get_item("保存类型").get_value()
        input_panel.remove_item(index=list(range(1, input_panel.get_items_count())))
        if type_ == "本地目录":
            input_panel.append_item(
                YkItem("保存至本地目录", "", '<button on-click="choose_data_folder">选择文件</button>',
                       size=[50, 80, 40]),
            )
            input_panel.set_value("保存至本地目录", value=self.project.data_folder or "")
        elif type_ == "Sqlite数据库":
            input_panel.append_item(
                [YkItem("数据库名", "", "",
                        size=[50, 80, 40]),
                 ]
            )
            input_panel.set_value("数据库名", value=self.project.db_name or "")
        elif type_ == "Mysql数据库":
            input_panel.append_item(
                [
                    YkItem("服务器地址", "", "", size=[50, 80, 40]),
                    YkItem("端口号", "", "", size=[50, 80, 40]),
                    YkItem("用户名", "", "", size=[50, 80, 40]),
                    YkItem("密码", "", "", size=[50, 80, 40]),
                    YkItem("数据库名", "", "", size=[50, 80, 40]),
                ]
            )
            input_panel.set_value("服务器地址", value=self.project.db_ip or "")
            input_panel.set_value("端口号", value=self.project.db_port or "")
            input_panel.set_value("用户名", value=self.project.db_user or "")
            input_panel.set_value("密码", value=self.project.db_passwd or "")
            input_panel.set_value("数据库名", value=self.project.db_name or "")

    def save_storage(self):
        input_panel: YkInputPanel = self.temp_.get("input_panel")
        info = input_panel.get_values_and_units(need_unit=False, need_label=True, need_dict=True)
        self.project.set_storage(info.get("保存类型"))
        if self.project.storage == "Sqlite数据库":
            self.project.db_name = info.get("数据库名")
        elif self.project.storage == "本地目录":
            self.project.data_folder = info.get("保存至本地目录")
        elif self.project.storage == "Mysql数据库":
            self.project.db_user = info.get("用户名")
            self.project.db_passwd = info.get("密码")
            self.project.db_ip = info.get("服务器地址")
            self.project.db_port = info.get("端口号")
            self.project.db_name = info.get("数据库名")
        dialog: YkDialog = self.temp_.get("dialog")
        dialog.close()

    def choose_data_folder(self):
        """
        选择股票数据文件保存的路径
        """
        data_folder = QFileDialog.getExistingDirectory(self, '选择错误工况模型保存目录', os.getcwd(),
                                                       QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if data_folder:
            self.project.data_folder = data_folder
            self.temp_.get("input_panel").set_value("保存至本地目录", data_folder)

    def save(self):
        self.proj = self.project.to_dict()
        super().save()

    def save_as(self):
        self.proj = self.project.to_dict()
        super().save_as()


def start():
    start_time = datetime.datetime.now()  # 用来统计执行时间

    if gv.command == "download":
        gv.tsd.download(gv.symbol, append=True)

    elif gv.command == "getName":
        gv.tsd.get_name()

    elif gv.command == "getOpenLimitUp":
        gv.tsd.get_open_limit('up')

    elif gv.command == "getOpenLimitDown":
        gv.tsd.get_open_limit_and_lastdays('down')

    elif gv.command == "getSymbols":
        symbols = gv.tsd.get_all_stock_basic_info()  # 会生成allsymbols.csv
        # for symbol in symbols:#传递参数太多，不适合outputStream传递，使用硬盘文件传递
        #     print("py to java:{}".format(symbol))
        # print(np.array(symbols))

    elif gv.command == "getStockNum":
        symbols = gv.tsd.get_all_stock_basic_info()
        print("共有 {} 只股票".format(len(symbols)))

    elif gv.command == "getNewStocks":
        # 查询当前所有正常上市交易的股票列表 ts_code     symbol     name     area industry    list_date(上市日期)
        data = gv.tsd.api.query('stock_basic', exchange='', list_status='L',
                                fields='ts_code,symbol,name,area,industry,list_date')
        sortedData = data.sort_values(by="list_date", ascending=False)
        for index, row in sortedData[0:20].iterrows():
            print(row["list_date"], row["name"], row["area"], row["industry"], row["symbol"])

    elif gv.command == "getBottomOut":
        symbols, _ = gv.tsd.get_bottom_out(int(gv.symbol))
        print("{}天内触底反弹股票列表如下：".format(gv.symbol))
        print(symbols)

    elif gv.command == "debug":
        gv.tsd.download(gv.symbol, append=True)
        # tsd.download_daily(date.today())
        # gv.tsd.get_open_limit()
        # gv.tsd.get_bottom_out(10)
        # logging.debug("最后一个交易日：{}".format(tsd.get_last_working_day()))
        # logging.debug("查询股票{}今天的交易数据：".format(symbol, tsd.get_data_of_day(symbol)))
        # gv.logger.debug("目前上市的股票代码：\n{}".format(pd.Series(gv.tsd.get_all_stock_symbol())))
        # gv.logger.debug("最近的工作日列表:\n{}".format(pd.Series(gv.tsd.get_last_n_working_day(30))))
        # tsd.get_open_limit_of_n_trading_days(30, 'up', 'ascend')
        # gv.tsd.get_open_limit_of_n_trading_days(30, 'down', 'ascend')
        # gv.tsd.get_open_limit_and_lastdays(last_date=datetime.date.fromisoformat("2019-12-31"))
        # gv.tsd.recent_30_open_limit_down_to_file(days=30)

        # 模拟交易
        symbols = gv.tsd.get_all_stock_basic_info()
        # db.test1()
        # Main.test1()

        # 神经网络预测
        # pad.test1()
        # pad.test2()
        # pad.test3()
        # pad.test4()
        # datafile = os.path.join(gv.dataDirectory, gv.symbol + '.csv')
        # pps.prediction1(datafile)

        # import prediction.pytorch_pred as ptp
        # ptp.start_mysql_service()

        import yangke.stock.prediction.pytorch_pred_stock as ptps

        ptps.lstm_stock_use_in_build_rnn_fit(gv.symbol)
        # ptps.lstm_stock_classify(gv.symbol)

        # start_mysql_service()

        start_scrapy_start(r"start_stock10jqka.py")
        # start_scrapy_spider(r"jqka_spider.py")  # 因为在start_stock10jqka.py中还初始化了数据库，因此只能从start_...开始执行爬虫

        # stocks = gv.tsd.download_all_stocks(exclude=['000029', '600145', '688086', '601696'])  # 排除掉两个停牌了很多年的傻逼股票
        # pred_df = ptps.prediction(stocks, 'fit')
        # pred_df.sort_values(by=['p_change'], inplace=True, ascending=False)
        # gv.logger.info("预测涨幅最大的5只股票为：\n{}".format(pred_df[:5]))

    else:
        gv.logger.error("Unknown command: {}".format(gv.command))
        sys.exit(0)
    end_time = datetime.datetime.now()
    print("执行用时：{}s".format((end_time - start_time)))


if __name__ == "__main__":
    # run_app(MainWindow, theme='dark_lightgreen.xml')
    run_app(MainWindow, theme='default_dark.xml')
    # run_app(MainWindow, None)
