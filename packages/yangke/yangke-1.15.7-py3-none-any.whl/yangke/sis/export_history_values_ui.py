import os

from yangke.common.qt import YkWindow, run_app
from yangke.common.QtImporter import QFileDialog, QMessageBox
from yangke.sis.export_history_values import load_history_file, find_condition


class MainFrame(YkWindow):
    def __init__(self):
        super(MainFrame, self).__init__()
        self.setWindowTitle("历史工况查询工具")
        self.enable_input_panel()
        self.enable_table()

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


if __name__ == "__main__":
    os.chdir(os.path.dirname(__file__))
    run_app(MainFrame)
