import os

import torch

from yangke.common.config import logger
from yangke.common.qt import YkWindow, run_app, YkItem, YkInputPanel, YkConsole
from yangke.common.QtImporter import QMessageBox, QFileDialog, QHBoxLayout, QCheckBox, QComboBox, QWidget, \
    QLineEdit, QApplication, QStringListModel
from yangke.common.fileOperate import read_csv_ex
from yangke.pytorch.mytorch import DataSetFitting, DataFitterNet
from yangke.pytorch.ui.PriorLoss_PyQt5 import Ui_Form


class PriorLossWidget(QWidget):
    def __init__(self):
        super(PriorLossWidget, self).__init__()
        self.total_items = 10
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.x_titles = []
        self.y_title = None
        self.rules = []
        # self.ui.btn_ok.clicked.connect(self.save_rules)  btn_ok的点击事件有根组件完成，因为要保存信息至项目级别
        for i in range(1, self.total_items, 1):
            exec(f"self.ui.check{i}.stateChanged.connect(lambda: self.checked_changed({i}))", {"self": self})

    def update_parameters(self, x_titles, y_title):
        self.x_titles = x_titles
        self.y_title = y_title

    def checked_changed(self, idx):
        ui = self.ui
        check: QCheckBox = eval(f"ui.check{idx}")
        condition: QHBoxLayout = eval(f"ui.condition{idx}")
        widget: QWidget = eval(f"ui.widget{idx}")
        layout: QHBoxLayout = widget.layout()
        if check.isChecked():
            combo1: QComboBox = getattr(ui, f"prior{idx}1")
            combo2: QComboBox = getattr(ui, f"prior{idx}2")
            combo3: QComboBox = getattr(ui, f"prior{idx}3")
            combo4: QComboBox = getattr(ui, f"prior{idx}4")
            layout.removeItem(condition)
            layout.removeWidget(combo4)
            condition.deleteLater()
            combo1.deleteLater()
            combo2.deleteLater()
            combo3.deleteLater()
            combo4.deleteLater()
            QApplication.processEvents()
            del combo4
            del condition
            condition = QLineEdit()
            layout.addWidget(condition)
            setattr(ui, f"condition{idx}", condition)
        else:
            layout.removeWidget(condition)
            condition.deleteLater()
            QApplication.processEvents()
            condition = QHBoxLayout()
            combo1 = QComboBox()
            combo2 = QComboBox()
            combo3 = QComboBox()
            combo4 = QComboBox()
            condition.addWidget(combo1)
            condition.addWidget(combo2)
            condition.addWidget(combo3)
            setattr(ui, f"prior{idx}1", combo1)
            setattr(ui, f"prior{idx}2", combo2)
            setattr(ui, f"prior{idx}3", combo3)
            setattr(ui, f"prior{idx}4", combo4)
            setattr(ui, f"condition{idx}", condition)
            combo4.setDisabled(True)
            layout.addLayout(condition)
            layout.addWidget(combo4)
        self.display_rules(idx=idx)

    def display_rules(self, rules: dict | None = None, idx=None):
        """
        将规则显示在PriorLossWidget上
        :param rules:
        :param idx: 设置单个rule时，指定rule的索引，索引从1开始
        :return:
        """
        if rules is None:
            rules = [None] * self.total_items

        exp_list = ["无"]
        if self.x_titles is None:
            return
        for x in self.x_titles:
            exp_list.append(f"[{self.y_title[0]}]随[{x}]单调递增")
            exp_list.append(f"[{self.y_title[0]}]随[{x}]单调递减")
        for i in range(self.total_items):
            if i < len(rules):
                rule = rules[i]
            else:
                rule = None

            check: QCheckBox = getattr(self.ui, f"check{i + 1}")
            if idx is not None:
                if i + 1 != idx:
                    continue
            if rule is None:
                if check.isChecked():
                    ...
                else:
                    combo1: QComboBox = getattr(self.ui, f"prior{i + 1}1")
                    combo2: QComboBox = getattr(self.ui, f"prior{i + 1}2")
                    combo3: QComboBox = getattr(self.ui, f"prior{i + 1}3")
                    combo4: QComboBox = getattr(self.ui, f"prior{i + 1}4")
                    combo2.setModel(QStringListModel(["无", "大于", "等于", "小于", "任何条件"]))
                    combo2.setCurrentIndex(0)
                    combo1.hide()
                    combo3.hide()
                    combo4.setModel(QStringListModel(exp_list))
                    exec(f"combo2.currentTextChanged.connect(lambda: self.condition_changed(combo2, {i + 1}))",
                         {"self": self, f"combo2": combo2})

            else:
                is_checked = rule.get("isChecked")
                if is_checked:
                    check.setChecked(True)
                    condition: QLineEdit = getattr(self.ui, f"condition{i + 1}")
                    condition.setText(rule.get("expression") or "")
                else:
                    check.setChecked(False)
                    var1 = rule.get("var1")
                    op = rule.get("op")
                    var2 = rule.get("var2")
                    expression = rule.get("expression")
                    combo1: QComboBox = getattr(self.ui, f"prior{i + 1}1")
                    combo2: QComboBox = getattr(self.ui, f"prior{i + 1}2")
                    combo3: QComboBox = getattr(self.ui, f"prior{i + 1}3")
                    combo4: QComboBox = getattr(self.ui, f"prior{i + 1}4")
                    exec(f"combo2.currentTextChanged.connect(lambda: self.condition_changed(combo2, {i + 1}))",
                         {"self": self, f"combo2": combo2})

                    combo1.setModel(QStringListModel(self.x_titles))
                    combo2.setModel(QStringListModel(["无", "大于", "等于", "小于", "任何条件"]))
                    combo3.setModel(QStringListModel(self.x_titles))
                    combo4.setModel(QStringListModel(exp_list))
                    combo1.setCurrentText(var1)
                    combo2.setCurrentText(op)
                    combo3.setCurrentText(var2)
                    combo4.setCurrentText(expression)

    def condition_changed(self, combox, idx=None):
        text = combox.currentText()
        combo1: QComboBox = getattr(self.ui, f"prior{idx}1")
        combo2: QComboBox = getattr(self.ui, f"prior{idx}2")
        combo3: QComboBox = getattr(self.ui, f"prior{idx}3")
        combo4: QComboBox = getattr(self.ui, f"prior{idx}4")
        model1 = QStringListModel(self.x_titles)
        model3 = QStringListModel(self.x_titles)
        combo1.setModel(model1)
        combo3.setModel(model3)
        if text in ["大于", "等于", "小于"]:
            combo1.show()
            combo3.show()
            combo4.setDisabled(False)
        elif text == "无":
            combo1.hide()
            combo3.hide()
            combo4.setCurrentText("无")
            combo4.setDisabled(True)
        else:
            combo1.hide()
            combo3.hide()
            combo4.setDisabled(False)

    def parse_prior_loss_rules(self):
        """
        从PriorLossWidget面板上获取并返回PriorLoss的设置信息

        :return:
        """
        self.rules = []
        for i in range(self.total_items):
            check: QCheckBox = getattr(self.ui, f"check{i + 1}")
            if check.isChecked():
                exp_lineedit: QLineEdit = getattr(self.ui, f"condition{i + 1}")
                exp = exp_lineedit.text()
                self.rules.append({"isChecked": True, "expression": exp})
            else:
                combo1: QComboBox = getattr(self.ui, f"prior{i + 1}1")
                combo2: QComboBox = getattr(self.ui, f"prior{i + 1}2")
                combo3: QComboBox = getattr(self.ui, f"prior{i + 1}3")
                combo4: QComboBox = getattr(self.ui, f"prior{i + 1}4")
                var1 = combo1.currentText()
                op = combo2.currentText()
                var2 = combo3.currentText()
                exp = combo4.currentText()

                if op == "无":
                    continue
                else:
                    self.rules.append({"isChecked": False, "var1": var1, "op": op,
                                       "var2": var2, "expression": exp})
        return self.rules


class MainWindow(YkWindow):
    def __init__(self):
        super(MainWindow, self).__init__()  # 完成了通用变量的加载
        self.setWindowTitle("数据分析")
        self.df = None  # 声明变量
        self.file = None  # 声明变量
        self.dataset = None  # 声明变量
        self.net = None
        self.display_project(self.proj)  # 展示本应用的数据至画面
        self.model = None
        self.console = YkConsole()
        self.add_dock_widget('终端', self.console, "bottom")
        logger.add(self.console)

    def open(self, proj=None):
        super(MainWindow, self).open(proj)  # 父类加载项目信息至self.proj中
        if isinstance(self.proj, dict):
            self.display_project(self.proj)  # 子类显示self.proj信息

    def new_project(self):
        super(MainWindow, self).new_project()
        self.display_project(self.proj)

    def set_predict_method(self, method):
        if method == "svm":
            self.proj.update({"predict_method": "svm"})
        else:
            self.proj.update({"predict_method": "nn"})
        self.display_project()

    def display_project(self, proj=None):
        """
        展示数据至画面

        :param proj:
        :return:
        """
        self.enable_table("ui/ui_panel.yaml")
        self.enable_input_panel("ui/ui_panel.yaml", domain="panel")
        _predict_method = self.proj.get("predict_method")
        if _predict_method is None or _predict_method == "nn":
            if self._input_tab is None or "set_nn" not in self._input_tab.labels:
                self.add_input_panel("ui/ui_panel.yaml", domain="set_nn")
            if "set_svm" in self._input_tab.labels:
                self._input_tab.remove_tab("set_svm")
        else:
            if self._input_tab is None or "set_svm" not in self._input_tab.labels:
                self.add_input_panel("ui/ui_panel.yaml", domain="set_svm")
            if "set_nn" in self._input_tab.labels:
                self._input_tab.remove_tab("set_nn")
        self.add_input_panel("ui/ui_panel.yaml", domain="set_var")
        self.add_input_panel(domain="set_predict")
        # 添加计算结果面板后，会导致self._table_widget面板不显示dataframe数据，原因未知
        # self.add_content_tab(YkDataTableWidget(from_file=None), "计算结果", replace=False)
        if self.proj == {}:
            # 清空软件界面上现有的数据
            self.replace_table("ui/ui_table.yaml")
            self.replace_input_panel("ui/ui_panel.yaml", domain="panel")
        elif self.proj is not None and self.proj is not False:
            self.file = self.proj.get("datafile")
            if self.file is None:
                return
            self.df = self.proj.get("dataframe")
            self._input_tab.activate_tab("panel")
            self.set_value_of_panel({"数据文件": self.file}, panel="panel")
            if os.path.exists(self.file):
                self.df = read_csv_ex(self.file)
            if self.df is None:
                return
            self._table_widget.display_dataframe(self.df[:1000], index=None)
            # 清空所有已添加的输入参数
            self._input_panel = self._input_tab.get_tab_panel("panel")
            while len(self._input_panel.get_values_and_units(need_unit=False)) > 1:
                self._input_panel.remove_item(index=1)
            #
            title = list(self.df.columns)
            items = [
                YkItem(label="选择神经网络输入参数：", size=[200, 50, 50]),
                YkItem(label="input 1", value=title, size=[50, 150, 100]),
                YkItem(label="", value='<button on-click="remove_input_item()">删除输入参数</button>',
                       unit='<button on-click="insert_input_item()">添加输入参数</button>', size=[50, 100, 100]),

                YkItem(label="选择神经网络输出参数：", size=[200, 50, 50]),
                YkItem(label="output 1", value=title, size=[50, 150, 100]),
                YkItem(label="", value='<button on-click="remove_output_item()">删除输出参数</button>',
                       unit='<button on-click="insert_output_item()">添加输出参数</button>', size=[50, 100, 100]),
            ]
            self._input_panel = self._input_tab.get_tab_panel("panel")
            self._input_panel.append_item(items)
            if self.proj.get("x_titles") is not None:
                x_titles = self.proj.get("x_titles")
                if len(x_titles) > 0:
                    self._input_panel.set_value("input 1", x_titles[0])
                for i in range(1, len(x_titles)):
                    self.insert_input_item()
                    self._input_panel.set_value(f"input {i + 1}", x_titles[i])
            if self.proj.get("y_titles") is not None:
                y_titles = self.proj.get("y_titles")
                if len(y_titles) > 0:
                    self._input_panel.set_value("output 1", y_titles[0])
                for i in range(1, len(y_titles)):
                    self.insert_output_item()
                    self._input_panel.set_value(f"output {i + 1}", y_titles[i])
            self.proj.update({"dataframe": self.df})

            # 更新set_nn输入面板
            if _predict_method == "nn":
                self._input_panel = self._input_tab.get_tab_panel("set_nn")
                self._input_panel.set_value("损失函数类型", self.proj.get("loss_func"))
                self._input_panel.set_value("优化器", self.proj.get("optimizer"))
                self._input_panel.set_value("学习率", self.proj.get("learn_rate"))
                self._input_panel.set_value(label="训练轮次数", value=self.proj.get("epochs"))
                self._input_panel.set_value(label="批大小", value=self.proj.get("batch_size"))
                self._input_panel.set_value("神经网络保存路径", self.proj.get("save_path"))
                self._input_panel.set_value("训练集比例", self.proj.get("data_training_proportion"))
                self._input_panel.set_value("测试集比例", self.proj.get("data_test_proportion"))

                self.change_normal_method(self.proj.get("normalization_method"))

                self._input_panel.set_value("数据归一化方法", self.proj.get("normalization_method"))
            else:
                self._input_panel = self._input_tab.get_tab_panel("set_svm")
                self._input_panel.set_value("核", self.proj.get("svm_kernel"))

            combo_box = self._input_tab.get_tab_panel("set_var").get_item("数据归一化方法").value
            combo_box.currentTextChanged.connect(self.change_normal_method)

        self._input_tab.activate_tab("panel")

    def change_normal_method(self, sender):
        self._input_panel: YkInputPanel = self._input_tab.get_tab_panel("set_var")
        if self.proj.get("x_titles") is None:
            return
        titles = self.proj.get("x_titles").copy()
        titles.extend(self.proj.get("y_titles"))
        labels, _ = self._input_panel.get_values_and_units(need_label=True, need_dict=False, need_unit=False)

        _vars = self.proj.get("v_range") or {}

        for label in labels:  # 移除面板上已有的数据
            if label.startswith("参数:"):
                self._input_panel.remove_item(name=label)
        if sender == "min-max":
            items = []
            for title in titles:
                up, bot = _vars.get(title) or (0, 0)
                items.append(
                    YkItem(f"参数:{title}", up, f"<input type='text' value='{bot}'>", size=[100, 100, 100], indent=10))
            self._input_panel.append_item(items)
        else:
            pass

    def start_train(self):
        """
        开始神经网络训练

        :return:
        """
        if self.proj.get("x_titles") is None:
            msg = "error: no dataset!"
            QMessageBox.information(self, "提示信息", "数据集未设置！！")
            return msg
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.proj.update({"device": device})
        if self.proj.get("epochs") is None:
            QMessageBox.information(self, "提示信息", "神经网络未设置，切换到神经网络设置面板！")
            self._input_tab.activate_tab("set_nn")
            return

        # 构建神经网络数据集
        classify = True if self.proj.get('loss_func') == "CrossEntropy" else False
        self.dataset = DataSetFitting(self.df, x_title=self.proj.get("x_titles"), y_title=self.proj.get("y_titles"),
                                      proportion_train=float(self.proj.get("data_training_proportion")),
                                      proportion_test=float(self.proj.get("data_test_proportion")),
                                      classify=True)
        if classify:
            y_class_num = self.df[self.proj.get('y_titles')].drop_duplicates()  # 分类的类别数量
            y_class_num = list(y_class_num.to_numpy().squeeze())
            y_class_num = [int(_) for _ in y_class_num]
            if 0 not in y_class_num:
                logger.warning(f"当前为分类问题，分类问题中，类别编号必须以0开始，但当前类别标签中未发现类别为0的数据项")
            y_class_num = len(y_class_num)
            bak_info = y_class_num
        else:
            bak_info = self.proj.get("loss_func_bak_info")
        if self.proj.get("normalization_method") == "min-max":
            v_range = self.proj.get("v_range")
            x_range = [v_range[x] for x in self.proj.get("x_titles")]
            y_range = [v_range[y] for y in self.proj.get("y_titles")]
            self.dataset.set_standard(normal_method=self.proj.get("normalization_method"),
                                      x_range=x_range, y_range=y_range)
        else:
            self.dataset.set_standard(normal_method="z-score")

        settings = {
            "input": self.proj.get("x_titles"),
            "output": self.proj.get("y_titles"),
            "classify": classify,
            "networks": {
                "train": {
                    "epochs": self.proj.get("epochs"),
                    "batch_size": self.proj.get("batch_size"),
                    "learning_rate": self.proj.get("learn_rate"),
                },
                "loss_fn": {
                    "type": self.proj.get("loss_func"),
                    "bak_info": bak_info
                },
                "optimizer": {
                    "type": self.proj.get("optimizer")
                },
                "layers": self.proj.get("layers"),
            },
            "save_path": self.proj.get("save_path"),
            "normalization_method": self.proj.get("normalization_method")
        }

        # 构建神经网络对象
        self.net = DataFitterNet(settings1=settings)
        model = self.net.to(device)  # 将神经网络迁移到cpu或gpu上
        model.start_train(self.dataset)
        model.save_yk(self.proj.get("save_path"))
        self.model = model

    def update_proj(self):
        """
        更新项目信息

        :return:
        """
        # noinspection all
        self._input_panel: YkInputPanel = self._input_tab.currentWidget()
        _l, _v, _u = self._input_panel.get_values_and_units(need_unit=True, need_dict=False,
                                                            need_label=True)  # 不能使用dict，因为有重名
        x_titles = []
        y_titles = []
        layers = []
        v_range = {}
        for k, v, u in zip(_l, _v, _u):
            if k.startswith('input '):
                x_titles.append(v)
            elif k.startswith('output '):
                y_titles.append(v)
            elif k.startswith("损失函数"):
                self.proj["loss_func"] = v
            elif k.startswith("数据归一化方法"):
                self.proj["normalization_method"] = v
            elif k == "优化器":
                self.proj["optimizer"] = v
            elif k == "学习率":
                self.proj["learn_rate"] = float(v)
            elif k == "训练轮次数":
                self.proj["epochs"] = int(v)
            elif k == "批大小":
                self.proj["batch_size"] = int(v)
            elif k == "神经网络保存路径":
                self.proj["save_path"] = v
            elif k == "训练集比例":
                self.proj["data_training_proportion"] = float(v)
            elif k == "测试集比例":
                self.proj["data_test_proportion"] = float(v)
            elif k == "输入层":
                layers.append({"type": "input", "cell_num": "auto"})
            elif k.startswith("隐藏层"):
                _temp = k
                layers.append({})
            elif k == "类型":
                layers[-1].update({"type": v})
            elif k == "神经元数量":
                # noinspection all
                layers[-1].update({"cell_num": int(v)})
            elif k == "偏置":
                bias = True if v == "是" else False
                # noinspection all
                layers[-1].update({"bias": bias})
            elif k == "输出层":
                layers.append({"type": "output", "cell_num": "auto"})
            elif k.startswith("参数:"):
                k = k.replace("参数:", "")
                v_range.update({k: [float(v), float(u)]})
            elif k == "核":
                self.proj.update({"svm_kernel": v})
            elif k == "gamma":
                self.proj.update({"svm_gamma": v})
            elif k == "阶数":
                self.proj.update({"svm_degree": v})

        if len(x_titles) > 0:
            self.proj.update({"x_titles": x_titles, "y_titles": y_titles})
        if len(layers) > 0:
            self.proj.update({"layers": layers})
        if len(v_range) > 0:
            self.proj.update({"v_range": v_range})

    def choose_predict_file(self):
        files, _ = QFileDialog.getOpenFileName(self, '选择数据文件', os.getcwd(), "All Files(*)")
        if files is None or files == "":
            return
        if not files.endswith(".csv"):
            logger.warning(f"选择的文件{files}不是正确的数据文件，请检查!")
            return
        self._input_panel = self._input_tab.get_tab_panel("set_predict")
        self.set_value_of_panel({"数据文件": files})

    def predict(self):
        """
        加载模型并预测
        :return:
        """
        table_widget = self._content_tab.get_tab_panel("计算结果")
        self._input_panel = self._input_tab.get_tab_panel("set_predict")
        file = self._input_panel.get_item("数据文件").get_value()
        out_file = self._input_panel.get_item("预测结果输出文件").get_value()
        if not os.path.exists(file):
            QMessageBox.information(self, "提示信息", "数据文件不存在！")
            return
        df = read_csv_ex(file)
        if self.model is None:
            self.model = DataFitterNet.load_yk(self.proj.get("save_path"))
        y = self.model.prediction(df)
        y = y.flatten()
        df["predict"] = y
        if not os.path.exists(os.path.dirname(os.path.abspath(out_file))):
            os.makedirs(os.path.dirname(os.path.abspath(out_file)))

        df.to_excel(out_file, index=False)
        logger.debug(f"预测结果输出值{os.path.abspath(out_file)}")

    def choose_file(self):
        files, _ = QFileDialog.getOpenFileName(self, '选择数据文件', os.getcwd(), "All Files(*)")
        if files is None or files == "":
            return
        if not files.endswith(".csv"):
            logger.warning(f"选择的文件{files}不是正确的数据文件，请检查!")
            return
        self._input_panel = self._input_tab.get_tab_panel("panel")
        self.set_value_of_panel({"数据文件": files})
        value = self.get_value_of_panel(need_unit=False, need_dict=True)
        self.statusBar1.showMessage(str(value))
        self.file = files
        self.proj.update({"datafile": files})
        self.display_project(self.proj)

    def read_data(self):
        files = self.get_value_of_panel(need_unit=False, need_dict=True)['数据文件']
        if isinstance(files, list):
            for file in files:
                if os.path.exists(file):
                    self.df = read_csv_ex(file)
        else:
            if os.path.exists(files):
                self.df = read_csv_ex(files)
        self.enable_table()
        if self.df is None:
            return
        self._table_widget.display_dataframe(self.df)
        title = list(self.df.columns)
        items = [
            YkItem(label="选择神经网络输入参数：", size=[200, 50, 50]),
            YkItem(label="input 1", value=title, size=[50, 150, 100]),
            YkItem(label="", value='<button on-click="remove_input_item()">删除输入参数</button>',
                   unit='<button on-click="insert_input_item()">添加输入参数</button>', size=[50, 100, 100]),

            YkItem(label="选择神经网络输出参数：", size=[200, 50, 50]),
            YkItem(label="output 1", value=title, size=[50, 150, 100]),
            YkItem(label="", value='<button on-click="remove_output_item()">删除输出参数</button>',
                   unit='<button on-click="insert_output_item()">添加输出参数</button>', size=[50, 100, 100]),
        ]
        self._input_panel.append_item(items)
        self.proj.update({"dataframe": self.df})

    def insert_input_item(self, value=None):
        self._input_panel = self._input_tab.get_tab_panel("panel")
        values = self.get_value_of_panel(need_dict=True, need_unit=False)
        input_values = [e for e in values if e.startswith("input")]
        title = list(self.df.columns)
        item = YkItem(label=f"input {len(input_values) + 1}", value=title, size=[50, 150, 100])
        self._input_panel.insert_item(len(input_values) + 2, item)

    def remove_input_item(self):
        self._input_panel = self._input_tab.get_tab_panel("panel")
        values = self.get_value_of_panel(need_dict=True, need_unit=False)
        input_values = [e for e in values if e.startswith("input")]
        if len(input_values) <= 1:
            logger.warning(f"输入变量至少应有1个，无法继续删除")
            return
        self._input_panel.remove_item(name=input_values[-1])

    def insert_output_item(self):
        self._input_panel = self._input_tab.get_tab_panel("panel")
        values: dict = self.get_value_of_panel(need_dict=True, need_unit=False)
        output_values = [k for k, v in values.items() if k is not None and k.startswith("output")]
        title = list(self.df.columns)
        item = YkItem(label=f"output {len(output_values) + 1}", value=title, size=[50, 150, 100])
        idx = list(values.keys()).index(output_values[-1]) + 1
        self._input_panel.insert_item(idx, item)

    def remove_output_item(self):
        self._input_panel = self._input_tab.get_tab_panel("panel")
        values = self.get_value_of_panel(need_dict=True, need_unit=False)
        output_names = [e for e in values if e.startswith("output")]
        self._input_panel.remove_item(name=output_names[-1])

    def loss_changed(self):
        """
        修改损失函数

        :return:
        """
        current_input_panel_name = self._input_panel.name
        self._input_panel = self._input_tab.get_tab_panel("set_nn")
        loss_type = self._input_panel.get_item("损失函数类型").get_value()
        if loss_type == "PriorLoss":
            widget = PriorLossWidget()
            widget.update_parameters(x_titles=self.proj.get("x_titles"), y_title=self.proj.get("y_titles"))
            widget.display_rules(self.proj.get("loss_func_bak_info"))
            if self._content_tab is None:
                self.add_content_tab(widget=widget, tab_name="设置PriorLoss函数", replace=False)
            a0 = self._content_tab.widget(0).geometry()
            widget.setGeometry(a0)
            self.add_content_tab(widget=widget, tab_name="设置PriorLoss函数", replace=False)
            self._content_tab.activate_tab('设置PriorLoss函数')
            widget.ui.btn_ok.clicked.connect(self.save_prior_loss_info)
        else:
            if loss_type == "CrossEntropy":
                self.statusBar1.showMessage("CrossEntropy为多分类问题的损失函数！")
                logger.debug(
                    f"CrossEntropy为多分类问题的损失函数，分类问题中，输出参数必须为[0, 1, 2, ..., n]等代表类别的整数")
                logger.debug(f"选择该损失函数，模型将自动切换为分类预测神经网络！")
            else:
                ...
            if self._content_tab is None:
                return
            widget = self._content_tab.get_tab_panel("设置PriorLoss函数")
            if widget is not None:
                self._content_tab.removeTab(self._content_tab.indexOf(widget))

        self._input_panel = self._input_tab.get_tab_panel(current_input_panel_name)

    def save_prior_loss_info(self):
        # noinspection all
        widget: PriorLossWidget = self._content_tab.get_tab_panel("设置PriorLoss函数")
        if widget is None:
            return
        rules = widget.parse_prior_loss_rules()
        self.proj.update({"loss_func_bak_info": rules})  # 更新损失函数的备注信息
        self._content_tab.activate_tab('sheet 1')


if __name__ == "__main__":
    run_app(MainWindow)
