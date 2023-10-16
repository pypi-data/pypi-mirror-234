import os
import re
import traceback

import pandas as pd
from yangke.common.QtImporter import QColor, QFileDialog, QApplication

from yangke.base import dynamic_for
from yangke.common.config import logger
from yangke.ebsilon.ebsilon import EbsApp, EbsModel
from yangke.common.fileOperate import write_line
from yangke.common.qt import YkWindow, run_app, YkConsole


class MainWindow(YkWindow):
    def __init__(self):
        super().__init__()
        panel_ui_file = os.path.join(os.path.dirname(__file__), "UI", "ui_panel_ebsilon.yaml")
        table_ui_file = os.path.join(os.path.dirname(__file__), "UI", "ui_table_ebsilon.yaml")
        self.enable_input_panel(panel_ui_file, force=True)
        self.enable_table(table_ui_file, force=True)
        self.file_model: str | None = self.proj.get("file_model")
        self.file_summary: str | None = self.proj.get("file_summary")
        self.start_from = self.proj.get("start_from")
        self.err_folder = self.proj.get("err_folder")
        self.profile = self.proj.get("profile")
        self.cwd = self.proj.get("cwd")
        self._input_panel.set_value("Ebsilon模型", self.file_model)
        self._input_panel.set_value("结果保存至", self.file_summary)
        self._input_panel.set_value("开始计算序号", self.start_from)
        self._input_panel.set_value("错误模型保存目录", self.err_folder)
        self._input_panel.set_value("变工况Profile名", self.profile)
        self._table_widget.display_dataframe(self.proj.get("input_data"), row_index=2, col_index=0, header=None,
                                             index=None)
        self._table_widget.set_cell_value(1, 3, "参数描述")
        self._table_widget.item(1, 3).setBackground(QColor("#dfc2ea"))
        self._table_widget.display_dataframe(self.proj.get("output_data"), row_index=2, col_index=5, header=None,
                                             index=None)
        self.model: EbsModel | None = None
        self.ebs: EbsApp | None = None
        self.console = YkConsole()
        self.add_content_tab(self.console, "终端", True)
        logger.add(self.console)

    def choose_ebs_model(self):
        self.file_model, _ = QFileDialog.getOpenFileName(self, "打开项目", self.cwd,
                                                         "项目文件(*.ebs);;所有文件(*)")
        if self.file_model is not None:
            self._input_panel.set_value("Ebsilon模型", self.file_model)
            self.proj["file_model"] = self.file_model
            self.cwd = os.path.dirname(self.file_model)

    def choose_summary_file(self):
        self.file_summary, _ = QFileDialog.getSaveFileName(self, '保存项目', self.cwd,
                                                           "项目文件(*.csv);;所有文件(*)")
        if self.file_summary:
            self.proj["file_summary"] = self.file_summary
            self._input_panel.set_value("结果保存至", self.file_summary)

    def choose_error_folder(self):
        self.err_folder = QFileDialog.getExistingDirectory(self, '选择错误工况模型保存目录', self.cwd,
                                                           QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if self.err_folder:
            self.proj["err_folder"] = self.err_folder
            self._input_panel.set_value("错误模型保存目录", self.err_folder)

    def apply(self):
        _ = self._input_panel.get_values_and_units(need_unit=False, need_dict=True)
        self.file_summary = _.get("结果保存至")
        self.file_model = _.get("Ebsilon模型")
        self.err_folder = _.get("错误模型保存目录")
        self.profile = _.get("变工况Profile名")
        self.start_from = float(_.get("开始计算序号"))
        self.proj.update({
            "file_summary": self.file_summary,
            "file_model": self.file_model,
            "err_folder": self.err_folder,
            "start_from": self.start_from,
            "profile": self.profile
        })
        self.read_input_output_para()

    def read_input_output_para(self):
        input_data = self._table_widget.read_data_in_range(2, 30, 1, 4, with_column=True)
        output_data = self._table_widget.read_data_in_range(2, 30, 6, 8, with_column=True)

        self.proj["input_data"] = input_data
        self.proj["output_data"] = output_data
        if self.proj_file is not None:
            self.save()

    def start_batch(self):
        self.apply()
        self._content_tab.activate_tab("终端")
        self.ebs = EbsApp()
        self.ebs.describe()
        self.batch_all_conditions()

    def batch_all_conditions(self):
        self.read_model()  # 读入ebsilon模型文件
        model = self.model
        model.activate_profile(self.profile)  # 切换到专为批量计算设计的batch工况

        i = 0
        input_data: pd.DataFrame = self.proj.get("input_data")
        # 删除input_data中以=开头的行，这些行是参数设置，不从循环中设置
        # 将input_data转换为list类型的二位数组
        data_for = []
        data_set_value = []
        components = []
        des_input = []
        paras = []
        _ = input_data.T
        for idx, row in _.items():  # .items()方法只能按列遍历，因此需要先转置
            if row["参数取值"].startswith("="):
                data_set_value.append(row)
            else:
                data_for.append(eval(row["参数取值"]))
                components.append(row["组件名"])
                paras.append(row["参数名"])
                des_input.append(row["参数描述"])

        # ------------------------------------- 写输出文件的标题行 -------------------------------------
        res_para_description = []
        _ = self.proj.get("output_data").T
        for idx, row in _.items():
            res_para_description.append(row["参数描述"])
        line = ["序号", *des_input, *res_para_description, "计算结果"]
        line = ",".join(line)
        write_line(self.file_summary, f"{line}\n")
        # ------------------------------------- 写输出文件的标题行 -------------------------------------

        # ------------------------------------- 剔除不满足限制条件的工况 -------------------------------------

        # ------------------------------------- 剔除不满足限制条件的工况 -------------------------------------


        for input_values in dynamic_for(data_for):
            self.process_events()
            if i < self.start_from:
                i = i + 1
                continue
            logger.debug(f"=========================={i} start===========================")
            logger.debug(f"输入参数为：{des_input} = {input_values}")
            # 循环设置每个参数
            for com, par, dat in zip(components, paras, input_values):
                try:
                    try:
                        dat = float(dat)
                    except:
                        pass
                    model.set_value(com, par, dat)
                except (AttributeError, NameError):
                    logger.error(f"设置模型的值时发生错误")
                    traceback.print_exc()
                    return

            # 循环设置条件参数，有些参数的取值为条件语句，如 当Comp_1.Q<=0时，com.par取1，否则取2，则dat="=1 if Comp_1.Q<=0 else 2"
            for row in data_set_value:
                com, par, dat, _ = row.values
                res = re.findall(r"=(.+) if (.+) else (.+)", dat)[0]  # dat = "=1 if Comp_1.Q<=0 else 2"
                if len(res) == 3:
                    _com_prefer, _par_refer, _op, _val = re.findall(r"(.+?)\.(.+?)([<=>]+)(.+?)", res[1])[0]
                    _val_act = model.get_value(_com_prefer, _par_refer)
                    expression = f"{_val_act}{_op}{_val}"
                    if eval(expression):
                        val = res[0]
                    else:
                        val = res[2]

                model.set_value(com, par, val)

            result = model.simulate_new()
            cal_res_description = result.get_result_summary()
            logger.debug(cal_res_description)

            if result.success(no_error_as_success=True):
                # 计算成功，则组装计算结果
                output_values = []
                _ = self.proj.get("output_data").T
                for idx, row in _.items():
                    com = row["组件名"]
                    par = row["参数名"]
                    des = row["参数描述"]

                    if par.startswith("="):
                        # 说明结果是公式
                        val = self.evaluate_equation(par)
                    else:
                        val = model.get_value(com, par)
                    output_values.append(val)

                logger.debug(f"输出参数为：{res_para_description} = {output_values}")
                output_line = [i, *input_values, *output_values, cal_res_description]
            else:
                # 输出错误信息
                self.model.save_as(os.path.join(self.err_folder,
                                                f"model{i}.ebs"))
                output_line = [i, *input_values, *[None] * len(res_para_description), cal_res_description]

            output_line = [str(_) for _ in output_line]
            output_line = ",".join(output_line)
            write_line(self.file_summary, line=f"{output_line}\n", append=True)
            logger.debug(f"=========================={i} end===========================")
            i = i + 1

    def process_events(self):
        QApplication.processEvents()

    def evaluate_equation(self, equations: str):
        """
        根据字符串表达的公式计算公式的值
        """
        # ------------------------------- 分析公式 ---------------------------------
        if equations.startswith("="):
            equations = equations[1:]
        reg1 = "[A-Za-z]+[A-Za-z\d_]*\."  # 匹配以字母开头，后续跟任意数量的[字母数字下划线字符]，然后接一个小数点
        reg2 = "[A-Za-z]+[A-Za-z\d_]*"  # 匹配以字母开头，后续跟任意数量的[字母数字下划线字符]
        reg = f"({reg1}{reg2})"  # 组合后，即匹配 组件名.变量名 的字符串结果
        res = re.findall(reg, equations)  # 可能会有重复的，但不影响结果，去重操作计算量可能大于直接替换，因为大部分情况无重复
        for para in res:
            com, par = para.split('.')
            val = self.model.get_value(com, par)
            equations = equations.replace(para, str(val))
        _ = eval(equations)
        return _

    def read_model(self):
        model_path = self.file_model
        try:
            if self.model is not None and self.model.get_path() == model_path and self.model.model is not None:
                pass
            else:
                self.model = self.ebs.open(model_path)
        except AttributeError:  # 有时候会出现model不为空，但model.model为None的情况，这种情况下，model.get_path()会报错
            self.model = self.ebs.open(model_path)
        if self.model.model is None:
            self.ebs = EbsApp()  # 出现这种情况一般是ebs崩了，尝试重新初始化
            self.read_model()
        return self.model

    def get_color(self):
        ...


if __name__ == "__main__":
    # settings = server.read_settings(r"C:\Users\YangKe\Desktop\新建文件夹\15版\settings.xlsx")
    # ebs = EbsApp()
    # ebs.describe()
    # batch_all_conditions(start_from=0)
    run_app(MainWindow)
