import os

import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidgetItem, QApplication
from yangke.base import execute_function_by_interval

from yangke.common.config import logger
from yangke.common.qt import YkWindow, run_app, YkDataTableWidget, YkConsole
from yangke.common.QtImporter import QFileDialog, QMessageBox
from yangke.sis.export_history_values import load_history_file, find_condition
from yangke.sis.dll_file import read_data


class MainFrame(YkWindow):
    def __init__(self):
        super(MainFrame, self).__init__()
        self.setWindowTitle("历史工况查询工具")
        self.enable_input_panel()
        self.enable_table()
        self.console = YkConsole()
        self.add_panel('终端', self.console, Qt.BottomDockWidgetArea)
        logger.add(sink=self.console)  # 日志将打印到GUI界面上

    def choose_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "选择历史数据文件", os.getcwd(), "*.xlsx;;*.*")
        if os.path.exists(file):
            self.statusBar().showMessage("正在加载历史数据文件，请耐心等待！")
            self.df = load_history_file(file)
            self.statusBar().showMessage("就绪")

    def get_condition(self):
        """
        根据输入面板内容获取符合条件的工况

        :return:
        """
        values = self.get_value_of_panel(need_dict=True, need_unit=False)
        unit_condition = [("凝汽器热负荷", float(values.get("凝汽器热负荷")), "1%"),
                          ("环境温度", float(values.get("环境温度")), "±2"),
                          ("环境湿度", float(values.get("环境湿度")), "±10"),
                          ]
        cold_condition = {"循泵方式": values.get("循泵方式"), "机力塔数量": int(values.get("机力塔数量"))}
        auto_loose = values.get("自动放宽条件限制")
        auto_loose = True if auto_loose == "是" else False

        self.res = find_condition(self.df, unit_condition=unit_condition, cold_condition=cold_condition,
                                  auto_loose=auto_loose)
        if self.res is None:
            # 弹窗提示
            QMessageBox.information(self, '提示信息', '历史数据中不存在满足指定条件的工况')
            self.statusBar().showMessage("就绪")
        else:
            self.replace_table(table_ui_file="ui/ui_table.yaml")
            self._table_widget.display_dataframe(self.res)
            self.statusBar().showMessage(f"指定工况下的平均背压为{self.res.mean(numeric_only=True)['当前背压']}")

    def set_points(self):
        self.replace_table("ui/ui_table_set_points.yaml")
        # self.table_widget.set_cell_value(1, 1, "设置导数测点清单")
        # self.table_widget.set_cell_value(2, 1, "测点名")
        # self.table_widget.set_cell_value(2, 2, "标签名")

    def test_points(self):
        _ = os.path.join(os.path.dirname(__file__), "ui", "ui_dcs_test.yaml")
        self.add_content_tab(widget=YkDataTableWidget(from_file=_, root_window=self), tab_name='DCS测点测试')
        self._content_tab.activate_tab('DCS测点测试')

    def _get_value_dcs(self):
        """
        获取DCS测点测试面板上的数据标签名，并更新数据
        """
        table: YkDataTableWidget = self._content_tab.get_tab_panel('DCS测点测试')
        rows = table.rowCount()
        df = table.read_data_in_range(2, rows, 1, 2)
        _ = df.duplicated(subset='测点描述')
        if _.any():
            logger.debug(f"测点描述有重复！")
            return

        _ = df.duplicated(subset='标签名')
        if _.any():
            logger.debug(f"测点标签名有重复")
            return

        if df.shape[0] == 0:
            logger.debug("无待测试的测点！")
            return
        snapshot = read_data(tag_des_read=dict(zip(df['测点描述'], df["标签名"])))
        snapshot.drop(columns="DateTime", inplace=True)
        for col in snapshot.columns:
            _ = table.findItems(col, Qt.MatchExactly)
            if len(_) == 1:
                widget: QTableWidgetItem = _[0]
                x, y = widget.row(), widget.column()
                table.set_cell_value(x, y + 2, snapshot[col].values.item())
            else:
                logger.debug(f"表格中描述可能出现了修改，导致结果无法复制给指定参数！")
        logger.debug("数据更新")

    def _start_get_value_(self, b):
        if b:
            self.info['scheduler'] = execute_function_by_interval(self._get_value_dcs, minute=0, second=10,
                                                                  daemon=False)
        else:
            if self.info.get('scheduler') is not None:
                self.info['scheduler'].shutdown()
                self.info['scheduler'] = None
                logger.debug("测试线程已停止，数据不再更新")

    def export_points_enum_code(self):
        table: YkDataTableWidget = self._content_tab.get_tab_panel('DCS测点测试')
        rows = table.rowCount()
        df = table.read_data_in_range(2, rows, 1, 2)
        lines = []
        for idx, row in df.iterrows():
            line = f'{row["测点描述"]} = "{row["标签名"]}"'
            lines.append(line)
        if len(lines) == 0:
            logger.debug("未检测到测点信息，生成测点信息代码为空")
            return

        _code = """
from enum import Enum, unique
from yangke.base import get_key_value, is_number


@unique
@get_key_value
class TagsRead(Enum):
"""
        _ = "\n\t".join(lines)
        out_code = f"测点信息代码如下（测点描述应为合法的变量标识符，否则导出的代码变量名不合法）：\n{_code}\t{_}"
        logger.info(out_code)
        self._content_tab.activate_tab('终端')


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    run_app(MainFrame)
