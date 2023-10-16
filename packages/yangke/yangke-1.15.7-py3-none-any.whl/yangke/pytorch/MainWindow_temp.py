from yangke.base import AutoSavePara
import os

from yangke.common.config import logger
from yangke.common.qt import YkWindow, run_app, YkItem
from PyQt5.QtWidgets import QFileDialog
from yangke.common.fileOperate import read_csv_ex
from yangke.base import auto_save_para



class MainWindow(YkWindow, AutoSavePara):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.enable_input_panel()
        self.file = self.update_auto_save_para('self.file', None)
        self.set_value_of_panel({"数据文件": self.file})

    def choose_file(self):
        files, _ = QFileDialog.getOpenFileName(self, '选择数据文件', os.getcwd(), "All Files(*)")
        self.set_value_of_panel({"数据文件": files})
        self.file = self.update_auto_save_para('self.file', files)
        print("选择文件")

    def read_data(self):
        files = self.get_value_of_panel(need_unit=False, need_dict=True)['数据文件']
        if isinstance(files, list):
            for file in files:
                if os.path.exists(file):
                    df = read_csv_ex(file)
        else:
            if os.path.exists(files):
                df = read_csv_ex(files)
        self.enable_table()
        self._table_widget.display_dataframe(df)
        items = [
            YkItem(label="选择神经网络数据参数："),
            YkItem(unit=["1", "2"])
        ]
        self._input_panel.append_item(items)

    def append_item_in_input_panel(self):
        items = [
            YkItem(label="选择神经网络输入参数："),
            YkItem(unit=["1", "2"])
        ]
        self._input_panel.append_item(items)
