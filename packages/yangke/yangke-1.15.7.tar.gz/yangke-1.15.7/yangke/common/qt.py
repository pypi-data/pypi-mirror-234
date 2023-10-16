import json
import math
import re
import sys
import os
import time
import traceback
import functools

from pyecharts.charts import Grid
from pyecharts.globals import ThemeType

from yangke.common.QtImporter import (QtGui, QMainWindow, QHBoxLayout, QPushButton, QComboBox, QLineEdit,
                                      QTableWidgetItem,
                                      QLabel, QCheckBox, QVBoxLayout, QWidget, QApplication, QAction, QDesktopWidget,
                                      QTableWidget,
                                      QDialog, QInputDialog, QMessageBox, QWebEngineView, QStandardItem,
                                      QStandardItemModel,
                                      QTextEdit, QSplitter, QStatusBar, QTabWidget, QScrollArea, QFileDialog,
                                      QGridLayout,
                                      QMenu, QtCore, Qt, QKeyEvent, QBrush, QColor, QFont, QIcon, pyqtSignal, uic,
                                      pyqtSlot, QTreeView, QSizePolicy,
                                      QPoint, QPointF, QLine, QLineF, QListView, QDockWidget, QToolBar,
                                      QAbstractItemView, QRect, QFileInfo, QUrl,
                                      QMimeData, QKeySequence, QDrag, QTableWidgetSelectionRange, qt_version)

try:
    from yangke.common.QtImporter import QsciScintilla, QsciLexerPython, QsciAPIs
except ImportError:
    QsciScintilla = QTextEdit
    QsciLexerPython = None
    QsciAPIs = None

from pyecharts.charts.chart import Chart
from pyecharts import options as opts
from yangke.common.fileOperate import read_from_pickle, write_as_pickle
from yangke.common.config import logger
import pandas as pd
from gettext import gettext as _

try:
    from qt_material import apply_stylesheet
except:
    pass

from yangke.web.pyecharts.app import is_ready
from yangke.base import get_settings, is_number, start_threads, is_js_str, YkDict
from yangke.web.pyecharts.app import DataPackage
import numpy as np

_app = None


class UIWidget(QWidget):
    def __init__(self, ui_class):
        """
        将Qt designer设计的界面转换为QWidget对象，以便在其他应用中使用。示例：

由Qt Designer生成的Test.py文件，内容如下：
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.calendarWidget = QtWidgets.QCalendarWidget(Form)
        self.calendarWidget.setObjectName("calendarWidget")
        self.gridLayout.addWidget(self.calendarWidget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))

则本类的使用方法如下：
from Test import Ui_Form
widget = UIWidget(Ui_Form)
此时，widget可以添加到任意Qt界面中

        :param ui_class: Qt designer生成的*.py文件中的UI对象类或者*.ui文件的路径
        """
        super(UIWidget, self).__init__()
        if isinstance(ui_class, str):  # 如果直接传入的是*.ui文件
            widget = uic.loadUi(ui_class)
            self.setLayout(QGridLayout())
            self.layout().setContentsMargins(0, 0, 0, 0)
            # noinspection all
            self.layout().addWidget(widget, 0, 0, 1, 1)
            self.ui = widget
        else:  # 如果传入的ui文件转换后的python类
            self.ui = ui_class()
            self.ui.setupUi(self)


class YkToolBar(QToolBar):
    def __init__(self, parent=None, settings=None, from_file=None):
        """
        默认从工作目录下的ui/ui_toolbar.yaml加载工具栏信息。也可以使用字典定义工具栏，字典示例如下：
        toolbar = {
            "name": "工具栏1",  # 同一个软件可以有多个工具栏，但工具栏名称不能相同
            "actions": [
                {
                    "name": "刷新",
                    "shortcut": "F5",
                    "icon": "refresh.png",
                    "connect": "refresh()",
                    "statusTip": "刷新界面"
                },
                {
                    "name": "推出",
                    "shortcut": "Esc",
                    "connect": "close()",
                }
            ]

        }
        说明：toolbar字典中必须有name和actions这两个key，且actions数组中的元素是一个字典，该字典必须有name和connect这两个key


        """
        self.connect_info = {}  # 工具栏工具项的连接事件记录字典

        if settings is None:
            if from_file is None:
                from_file = _get_yaml_file("ui", "ui_toolbar")

            if from_file is not None:
                settings = get_settings(item=None, setting_file=from_file)
                settings = settings.get("toolbar")
            else:
                logger.error(f"找不到工具栏定义文件{os.path.abspath('ui/ui_toolbar.yaml')}")
                self.title = None
                super().__init__()
                return
        self.settings = settings
        self.title = self.settings.get("name")
        super(YkToolBar, self).__init__(self.title, parent)
        # super().__init__(self.title, parent)  # 因为super是c语言定义的方法，这里不能带关键字传参
        for action in self.settings.get("actions"):
            self.addAction(action)

    def get_name(self):
        """
        获取工具栏名称
        """
        return self.title

    def addAction(self, action: QAction | dict) -> None:
        """
        工具栏中添加一个工具，可以直接传入action或者使用字典定义工具。字典定义方法示例：
        action = {
            "name": "刷新",
            "shortcut": "F5",
            "icon": "refresh.png",
            "connect": "refresh()",
            "statusTip": "刷新界面"
        }
        """

        if isinstance(action, QAction):
            super().addAction(action)
        else:
            _action = QAction(_(action.get("name")), self)
            if action.get("shortcut"):
                key_str = action.get("shortcut")
                key = QKeySequence(key_str)
                _action.setShortcut(key)
            icon_path = action.get("icon")
            if icon_path:
                if os.path.exists(icon_path):  # 当前工作目录
                    icon_path = os.path.abspath(icon_path)
                elif os.path.exists(os.path.join("ui", icon_path)):  # 当前工作目录下的ui文件夹下
                    icon_path = os.path.join("ui", icon_path)
                elif os.path.exists(os.path.join(os.path.dirname(__file__), "ui", icon_path)):  # 库路径下
                    icon_path = os.path.join(os.path.dirname(__file__), "ui", icon_path)
                _action.setIcon(QIcon(icon_path))
            # if action.get("statusTip"):
            #     _action.setStatusTip(_(action.get("statusTip")))
            # try:
            #     exit_action.disconnect()  # 防止按钮的绑定事件多次执行
            # except TypeError:  # 当没有绑定事件时，会解绑失败
            #     pass
            connect = action.get("connect")
            if connect is not None:
                self.connect_info.update({_action: {"signal": "triggered", "connect": connect}})
            else:
                logger.warning(f"工具栏工具项({_(action.get('name'))})没有指定触发的事件，请检查！")
            super().addAction(_action)

    def apply_action_connect(self):
        for widget, desc in self.connect_info.items():
            connect_event_by_dict(widget, desc)

        # _action.triggered.connect(self.closeEvent)

    def __getstate__(self):
        """
        使该类可以被pickle序列化与反序列化，pickle会使用该方法返回的字典中的参数重新构造该类的对象
        """
        return {"settings": self.settings}


class YkDialog(QDialog):
    """
    对话框类，用于在其他界面中弹出自定义窗口，且窗口可以与父窗口通信
    """

    # 以下消息的传递参数时object，其包括(type, value)，其中type是消息想要传递的参数类型，value是想传递的值
    signal_close = pyqtSignal(object)  # 用于对话框关闭时发送关闭消息，object=(dict:value)是YkDialog关闭时的对象的值
    signal_button_clicked = pyqtSignal(object)  # object=(QPushButton, 按钮)，YkDialog对象会自动通过sender传递

    def __init__(self, parent, title=_("对话框"), widget=None):
        """
        弹出式对话框

        :param title:
        :param widget:  对话框上显示的QWidget对象
        """
        super().__init__(parent=parent)
        self.setWindowTitle(title)
        self.setWindowModality(Qt.ApplicationModal)
        if widget is None:
            widget = QLabel("对话框")
        self.widget = widget
        layout = QVBoxLayout()
        layout.addWidget(self.widget)
        self.setLayout(layout)
        self.show()

    def set_size(self, width, height):
        """
        设置对话框的尺寸，对话框位置自动置于父窗口的中心
        """
        _ = self.parent().geometry()
        xp, yp, wp, hp = _.x(), _.y(), _.width(), _.height()
        x = xp + int((wp - width) / 2)
        y = yp + int((hp - height) / 2)
        self.setGeometry(x, y, width, height)


# <editor-fold desc="已测试完成的代码">
def html_widget(url="https://www.baidu.com", local_file=None):
    _ = QWebEngineView()
    if local_file is not None:
        qurl = QUrl(QFileInfo(local_file).absoluteFilePath())
        _.load(qurl)
    else:
        _.load(QtCore.QUrl(url))
    return _


def _get_yaml_file(ui_folder, file_base_name):
    """
    查找yaml配置文件
    """
    # 首先查找ui_folder下是否存在指定文件
    file = os.path.join(ui_folder, f"{file_base_name}.yaml")
    if os.path.exists(file):
        return file
    else:
        file = os.path.join(ui_folder, f"{file_base_name}.yml")
        if os.path.exists(file):
            return file

    # 其次查找当前工作目录下是否存在指定文件
    file = os.path.abspath(f"{file_base_name}.yaml")
    if os.path.exists(file):
        return file
    else:
        file = os.path.abspath(f"{file_base_name}.yml")
        if os.path.exists(file):
            return file

    # 最后使用库中的文件

    file = os.path.join(os.path.dirname(__file__), "ui", f"{file_base_name}.yaml")  # 相对于qt.py的路径
    if os.path.exists(file):
        return file
    else:
        file = os.path.join(os.path.dirname(__file__), "ui", f"{file_base_name}.yml")  # 相对于qt.py的路径
        return file


# </editor-fold>

class YkWindow(QMainWindow):
    """
    一个桌面应用类，默认配置了相关设置。

    从settings.yaml中获取软件配置。

    默认从ui/ui_menu.yaml中获取软件菜单配置。
    默认从ui/ui_table.yaml获取软件主界面table的界面配置。
    """
    # button_clicked_signal = QtCore.pyqtSignal(object)
    yk_signal = pyqtSignal(dict)  # 子线程更新UI时，通过self.yk_signal.emit(dict)触发此信号，此信号绑定了更新UI事件

    def __init__(self, setting_file="default"):
        super().__init__()
        self.window_title = "YkMainFrame"  # 窗口的固定标题
        # noinspection all
        self.yk_signal.connect(self.yk_signal_received)
        self.ini_file = os.path.abspath("yk_window.ini")  # 软件默认打开的文件，从中加载软件设置信息，不要使用基于本文件的相对路径
        self.ini_info = {}  # 储存软件本身的设置信息
        if os.path.exists(self.ini_file):
            self.ini_info: dict = read_from_pickle(self.ini_file) or {}
        # 首先加载yk_window.ini文件，查找软件设置及历史项目信息
        # noinspection all
        self.proj_file: str = self.ini_info.get("last_proj")  # 查询最后一个打开的项目
        if self.proj_file is not None:
            if not os.path.exists(os.path.dirname(self.proj_file)):
                os.makedirs(os.path.dirname(self.proj_file))
            os.chdir(os.path.dirname(self.proj_file))  # 将工作目录切换到最后一次保存的文件目录
        self.proj = read_from_pickle(self.proj_file) or {}  # 软件项目信息，打开项目时加载项目文件内容至该字典中
        self.setting_file = setting_file
        self.settings = get_settings(setting_file=setting_file)
        self.info = {}  # 用于传递临时变量的变量

        self._content_tab: YkTabWidget | None = None
        self._table_widget: YkDataTableWidget | None = None  # 只有一个表格时，可以直接引用
        self._html_widget: QWebEngineView | None = None
        self._input_tab: YkTabWidget | None = None
        self._input_panel: YkInputPanel | None = None  # 输入面板，当只有一个输入面板时，可以直接引用该面板及其子方法
        self._root_splitter: QSplitter | None = None
        self._dock = None  # 软件界面上的QDockWidgets
        self.panels = {}  # 界面中所有面板以{名称: 面板对象}的形式存储在该参数中
        self.statusBar1: QStatusBar | None = None
        self.ini_info.update({"digits": 0})
        # self._digits = 0  # 软件界面中显示的小数的小数点默认位数
        # ---------------- 判断有没有ui文件夹，初始化ui_folder -------------------------
        ui_folder = self.settings.get_settings("mainframe.ui.folder") or os.path.abspath("ui")
        if os.path.exists(ui_folder):
            self.ui_folder = ui_folder
        else:
            self.ui_folder = os.getcwd()
        self.table_ui_file = None
        self.menu_ui_file = None
        # --------------------------------------------------------------------------
        self.toolbars = {}  # 可以有多个工具栏，通过工具栏名称获取对应的工具栏
        self.init_ui()
        self.set_window_size()
        self.show()
        logger.debug("就绪")

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.modifiers() == Qt.ShiftModifier | Qt.ControlModifier and a0.key() == Qt.Key_AsciiTilde:
            if self._dock is not None:
                if isinstance(self._dock, list):
                    if len(self._dock) > 0:
                        if self._dock[0].isHidden():
                            for _dk in self._dock:
                                _dk.show()
                        else:
                            for _dk in self._dock:
                                _dk.hide()
                else:
                    if self._dock.isHidden():
                        self._dock.show()
                    else:
                        self._dock.hide()
        elif a0.key() == Qt.Key_Escape:
            self.close()
        super().keyPressEvent(a0)

    def addToolBar(self, area, toolbar=None) -> None:
        if isinstance(area, YkToolBar):
            name = area.get_name()
            if self.toolbars.get(name) is not None:
                logger.debug(f"已存在名为{name}的工具栏，自动忽略添加工具栏操作")
            else:
                super().addToolBar(area)
                self.toolbars.update({name: area})
                area.apply_action_connect()  # 使工具栏中的工具项事件可以正常触发，必须在addToolBar()之后执行

    def refresh(self):
        logger.debug(f"方法未实现：refresh")

    def init_ui(self):
        # ----------------------------- 定义一个退出事件 ----------------------------------
        # exit_action = QAction(_('刷新'), self)
        # exit_action.setShortcut('F5')
        # exit_action.setIcon(QIcon(r"D:\PycharmProjects\lib4python\yangke\common\ui\refresh.png"))
        # exit_action.setStatusTip(_('刷新股票列表'))
        # # try:
        # #     exit_action.disconnect()  # 防止按钮的绑定事件多次执行
        # # except TypeError:  # 当没有绑定事件时，会解绑失败
        # #     pass
        # exit_action.triggered.connect(self.closeEvent)
        # # ----------------------------- 定义一个退出事件 ----------------------------------
        #
        # # 将退出事件添加到工具栏中
        # self.removeToolBar(self.toolbar)  # 防止重复添加工具栏
        # self.toolbar = self.addToolBar(_('工具栏1'))
        # self.toolbar.addAction(exit_action)
        toolbar = YkToolBar()
        self.addToolBar(toolbar)  # 可以有多个工具栏，但工具栏的名称不能相同
        # ----------------------------- 设置软件菜单 -------------------------------------
        menu_ui_file = self.settings.get_settings("mainframe.menu.ui")
        if menu_ui_file is None or len(menu_ui_file) == 0:
            menu_ui_file = _get_yaml_file(self.ui_folder, "ui_menu")
        if menu_ui_file is not None:
            self.menu_ui_file = menu_ui_file
            set_menu_bar(self, from_file=menu_ui_file)
        # ----------------------------- 设置软件菜单 -------------------------------------

        # ----------------------------- 设置软件图标 -------------------------------------
        logo_file = self.settings.get_settings("mainframe").get("logo") or os.path.join(self.ui_folder, "yk.png")
        if not os.path.exists(logo_file):
            logo_file = os.path.join(os.path.dirname(__file__), "yk.png")  # 该文件必然存在
        self.setWindowIcon(QIcon(logo_file))
        # ----------------------------- 设置软件图标 -------------------------------------

        # ----------------------------- 设置软件标题 -------------------------------------
        self.window_title = self.settings.get_settings("mainframe").get("title") or self.window_title
        self.setWindowTitle(_(self.window_title))
        # ----------------------------- 设置软件标题 -------------------------------------
        self.statusBar1: QStatusBar = self.statusBar()
        for _child in self.statusBar1.children():  # 移除PermanentWidget
            if isinstance(_child, QLabel):
                self.statusBar1.removeWidget(_child)
        self.statusBar1.showMessage('就绪')
        self.statusBar1.addPermanentWidget(QLabel("西安热工研究院有限公司                     "
                                                  "        ©2022 TPRI. All Rights Reserved."))
        if self.ini_info.get("table_enabled"):
            self.enable_table()
        else:
            self.destroy_table()
        if self.ini_info.get("input_panel_enabled"):
            self.enable_input_panel()  # 该方法经常异常出错，需要记录出错原因

    def set_status_bar_label(self, label="default"):
        for _child in self.statusBar1.children():  # 移除PermanentWidget
            if isinstance(_child, QLabel):
                self.statusBar1.removeWidget(_child)
        self.statusBar1.addPermanentWidget(QLabel(label))

    def switch_dock_widget(self, idx=None):
        """
        切换DockWidget的显示与隐藏
        """
        if isinstance(self._dock, QDockWidget):
            if self._dock.isVisible():
                self._dock.hide()
            else:
                self._dock.show()
        elif isinstance(self._dock, list):
            if idx is None or str(idx).strip() == "":
                for i in range(len(self._dock)):
                    self.switch_dock_widget(i)
            else:
                try:
                    idx = int(idx)
                    if len(self._dock) < idx:
                        return
                    if isinstance(self._dock[idx], QDockWidget):
                        if self._dock[idx].isVisible():
                            self._dock[idx].hide()
                        else:
                            self._dock[idx].show()
                except ValueError:
                    logger.warning(f"dock widget的索引错误,{idx=}")

    def setWindowTitle(self, title=None):
        """
        设置窗口标题，该窗口标题自带项目文件路径

        :param title:
        :return:
        """
        _title = title
        if title is None:
            proj_str = self.proj_file or "新建项目"
            super(YkWindow, self).setWindowTitle(f"{self.window_title} - {proj_str}")
        elif " - " in title:
            super(YkWindow, self).setWindowTitle(title)
            self.window_title = title.split("-")[0].strip()
        else:
            self.window_title = title
            proj_str = self.proj_file or "新建项目"
            super(YkWindow, self).setWindowTitle(f"{title} - {proj_str}")

    def new_project(self):
        """
        新建项目

        :return:
        """
        # self.proj = None  # 将空项目写入last_proj，并重新初始化软件
        self.ini_info.update({"last_proj": None})

        write_as_pickle(self.ini_file, self.ini_info)
        self.proj_file = None
        self.open(proj={})
        self.setWindowTitle()

    def save_as(self):
        """
        另存当前项目
        :return:
        """
        self.proj_file, _ = QFileDialog.getSaveFileName(self, '保存项目', os.getcwd(),
                                                        "项目文件(*.ykproj);;所有文件(*)")
        if self.proj_file:
            write_as_pickle(file=self.proj_file, obj=self.proj)  # 将项目信息存入硬盘文件
            self.ini_info.update({"last_proj": self.proj_file})  # 将项目文件路径写入软件ini文件，用于下次启动时直接加载项目文件
            self.setWindowTitle()
            _proj_name = os.path.splitext(os.path.basename(self.proj_file))[0]
            if _proj_name in self.get_content_tab_labels():
                logger.warning(f"当前已存在名为{_proj_name}的项目，请重新命名")
            else:
                self._content_tab.tabBar().setTabText(self._content_tab.currentIndex(), _proj_name)
        self.ini_info["size"] = self.geometry()
        write_as_pickle(self.ini_file, self.ini_info)

    def get_content_tab_labels(self):
        _ = [self._content_tab.tabText(i) for i in range(self._content_tab.tabBar().count())]
        return _

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.ini_info.update(
            {"size": (self.geometry().x(), self.geometry().y(), a0.size().width(), a0.size().height(),)})
        super().resizeEvent(a0)

    def open(self, proj=None):
        """
        该方法需要进一步实现才能显示打开的项目。因为每个软件项目的显示细节都不相同，需要具体实现，父类的open方法只加载项目文件至self.proj中。
        打开项目，如果传入了proj_info参数，则直接更新当前YkWindow中的参数为proj_info中保存的信息，本方法不对软件界面上的显示数据做更新。
        菜单项触发该方法时，第二个参数为False，原因未知
        :param proj:
        :return:
        """
        if proj is None or proj is False:
            self.proj_file, _ = QFileDialog.getOpenFileName(self, "打开项目", os.getcwd(),
                                                            "项目文件(*.ykproj);;所有文件(*)")
            if self.proj_file:
                self.proj = read_from_pickle(self.proj_file)
                self.init_ui()
                self.ini_info.update({"last_proj": self.proj_file})  # 将项目文件路径写入软件ini文件，用于下次启动时直接加载项目文件
        else:
            self.proj = read_from_pickle(self.proj_file)  # proj是项目的信息，不是项目文件
            self.ini_info.update({"last_proj": self.proj_file})  # 将项目文件路径写入软件ini文件，用于下次启动时直接加载项目文件
        self.setWindowTitle()
        # self.init_ui()

    def save(self):
        """
        保存self.proj参数到文件，如果当前项目已经存在对应的文件，则自动保存，如果不存在，则弹出选择文件对话框，由用户确定保存到的文件
        """
        if self.proj_file is not None:
            write_as_pickle(file=self.proj_file, obj=self.proj)
        else:
            self.save_as()
        if self.proj_file != "":
            os.chdir(os.path.dirname(self.proj_file))  # 将工作目录切换到最后一次保存的文件目录
            self.ini_info.update({"cwd": os.path.dirname(self.proj_file)})
            self.setWindowTitle(f"{self.window_title} - {self.proj_file}")
            self.statusBar1.showMessage("保存完成")
        self.ini_info["size"] = self.geometry()
        write_as_pickle(self.ini_file, self.ini_info)

    def add_panel(self, name, widget, location=Qt.LeftDockWidgetArea):
        """
        在左侧的停靠面板中添加一个列表视图
        :param name: 面板的名称，以后可以通过名称获取该视图
        :param widget: 面板对象
        :param location: 列表视图的位置，默认添加在左侧停靠面板中
        """
        if location == Qt.LeftDockWidgetArea or location == Qt.BottomDockWidgetArea or location == Qt.RightDockWidgetArea:
            self._dock = QDockWidget(name, self)
            self._dock.setWidget(widget)
            self.addDockWidget(location, self._dock)
            self.panels.update({name: widget})

    def add_dock_widget(self, name, widget, location=Qt.LeftDockWidgetArea):
        if location == "north" or location == "top":
            location = Qt.TopDockWidgetArea
        elif location == "south" or location == "bottom":
            location = Qt.BottomDockWidgetArea
        elif location == "left" or location == "west":
            location = Qt.LeftDockWidgetArea
        elif location == "right" or location == "east":
            location = Qt.RightDockWidgetArea
        self.add_panel(name, widget, location)

    def switch_input_panel(self, idx=None):
        """
        切换输入面板的显示与隐藏

        :param idx: 显示与隐藏的面板id，暂未使用，需要考虑按名称切换还是按索引切换
        """
        _ = idx
        if self._input_panel is not None:
            if self._input_panel.isVisible():
                self._input_panel.hide()
            else:
                self._input_panel.show()
        else:
            self.enable_input_panel()

    def enable_input_panel(self, panel_ui_file=None, domain=None, force=False):
        """
        :param force: 是否强制使用panel_ui_file刷新输入面板，因为窗口初始化是会生成要给输入面板，如果不强制，则默认只是显示初始化的面板
        :param panel_ui_file: 输入面板的定义文件
        :param domain: 面板在定义文件中的域
        """
        if not force:
            if self._input_panel is not None:
                return
        if panel_ui_file is None or panel_ui_file is False:
            panel_ui_file = self.settings.get_settings("mainframe.panel").get("ui")
            if panel_ui_file is None:
                panel_ui_file = _get_yaml_file(self.ui_folder, "ui_panel")
            if panel_ui_file is None:
                logger.warning(f"找不到配置文件：{os.path.abspath('ui_panel.yaml')}")

        self._input_panel = YkInputPanel(from_file=panel_ui_file, domain=domain)
        # self._input_panel.setMinimumSize(300, 400)  # 该语句会导致self.showMaximized()语句无效
        self.display_to_location(self._input_panel, 0)
        self._input_panel.apply_btn_connect()  # 链接input_panel中的按钮事件
        self.ini_info.update({"input_panel_enabled": True})
        self.info.update({"last_action": "enable_input_panel"})

    def add_input_panel(self, panel_ui_file=None, domain=None):
        """
        添加输入面板，panel_ui_file最好为"ui_panel.yaml"，可最大限度减小错误
        """
        if isinstance(panel_ui_file, YkInputPanel):
            self._input_panel = panel_ui_file
        else:
            if self._input_tab is not None:
                if domain in self._input_tab.labels:
                    return  # 如果需要添加的面板在输入面板tab组件中已经存在，则返回
                else:
                    ...
            if panel_ui_file is None or panel_ui_file is False:
                panel_ui_file = self.settings.get_settings("mainframe.panel").get("ui")
                if panel_ui_file is None:
                    panel_ui_file = _get_yaml_file(self.ui_folder, "ui_panel")
                    if panel_ui_file is None:
                        logger.warning(f"找不到配置文件：{os.path.abspath('ui_panel.yaml')}")
            _input_panel = YkInputPanel(from_file=panel_ui_file, domain=domain)
            if self._input_panel is not None and self._input_panel.name == _input_panel.name:
                return
            self._input_panel = _input_panel
        self.panels.update({self._input_panel.name: self._input_panel})
        # self._input_panel.setMinimumSize(300, 400)  # 该语句会导致self.showMaximized()语句无效
        if isinstance(self.centralWidget(), QSplitter):
            left_panel = self._root_splitter.widget(0)
            if isinstance(left_panel, YkTabWidget):
                left_panel.addTab(self._input_panel, self._input_panel.name)
            else:
                left_panel = YkTabWidget()
                left_panel.addTab(self._root_splitter.widget(0),
                                  self._root_splitter.widget(0).name)  # 此处添加时，root_splitter中的widget(0)会消失
                left_panel.addTab(self._input_panel, self._input_panel.name)
                self._root_splitter.insertWidget(0, left_panel)
            left_panel.setCurrentWidget(self._input_panel)
            self._input_tab = left_panel
        elif isinstance(self.centralWidget(), YkInputPanel):  # 如果当前中心组件是一个InputPanel
            central_widget = YkTabWidget()
            central_widget.addTab(self.centralWidget(),
                                  self.centralWidget().name)  # 此处添加时，centralWidget会消失
            central_widget.addTab(self._input_panel, self._input_panel.name)
            self.setCentralWidget(central_widget)
        # self.root_splitter.handle(0).setDisabled(True)
        self._input_panel.apply_btn_connect()  # 链接input_panel中的按钮事件

        self.ini_info.update({"input_panel_enabled": True})
        self.info.update({"last_action": "add_input_panel"})

    def enable_table(self, table_ui_file=None, force=False):
        if not force:
            if self._table_widget is not None:
                self.display_to_location(self._table_widget, 1)
                return
        if table_ui_file is None or not table_ui_file:
            # 首先从settings.yaml中查找table的定义文件
            table_ui_file = self.settings.get_settings("mainframe.table").get("ui")
            if table_ui_file is None:
                table_ui_file = _get_yaml_file(self.ui_folder, "ui_table")

            if table_ui_file is None:  # 如果以上都没有查找到ui_table.yaml文件，则使用库中的默认文件
                logger.warning(f"找不到配置文件：{os.path.abspath('ui_table.yaml')}")

            self._set_table(table_ui_file)
        else:
            self._set_table(table_ui_file)
        self.ini_info.update({"table_enabled": True})
        self.info.update({"last_action": "enable_table"})

    def destroy_table(self):
        ...

    def remove_input_panel(self, name=None):
        """
        从当前窗口中移除指定的input_panel

        :param name: input_panel的名称，如果不指定，则默认移除第一个
        """
        ...

    def replace_table(self, table_ui_file):
        self._set_table(table_ui_file)

    def replace_input_panel(self, panel_ui_file, domain=None):
        """
        直接替换input_panel有概率导致程序崩溃，尽量不要调用该方法
        :param panel_ui_file:
        :param domain:
        :return:
        """

        logger.warning("直接替换input_panel有概率导致程序崩溃，尽量不要调用该方法")
        if panel_ui_file is None or panel_ui_file is False:
            panel_ui_file = self.settings.get_settings("mainframe.panel").get("ui")
            if panel_ui_file is None:
                panel_ui_file = _get_yaml_file(self.ui_folder, "ui_panel")
                if panel_ui_file is None:
                    logger.warning(f"找不到配置文件：{os.path.abspath('ui_panel.yaml')}")
        self._input_panel = YkInputPanel(from_file=panel_ui_file, domain=domain)
        if domain in self._input_tab.labels:
            idx = self._input_tab.indexOf(self._input_tab.get_tab_panel(domain))
            self._input_tab.removeTab(idx)
            self._input_tab.insertTab(idx, self._input_panel, domain)
        else:
            self.display_to_location(self._input_panel, 0)
        self._input_panel.apply_btn_connect()  # 链接input_panel中的按钮事件
        self.ini_info.update({"input_panel_enabled": True, "panel_ui_file": panel_ui_file})

    def _set_table(self, table_ui_file):
        """
        初始化表格

        :param table_ui_file: 表格定义文件
        :return:
        """
        self.table_ui_file = table_ui_file
        self._table_widget: YkDataTableWidget = YkDataTableWidget(from_file=table_ui_file, root_window=self)
        self.display_to_location(self._table_widget, 1)

    def btn_clicked(self, anything=None, anything2=None, **kwargs):
        """
        处理点击事件

        :param anything: 触发该方法的信号传入的数据，可以是任何类型
        :param anything2: 接收点击事件传入的任何参数
        :return:
        """
        sender = self.sender()  # 发送事件的组件，可能是button、YkDialog等任何拥有signal的类
        if isinstance(sender, QPushButton):
            self.statusBar().showMessage(sender.text() + ' was pressed')

    def add_content_tab(self, widget, tab_name, replace=False):
        """
        在内容区域添加一个标签页，该方法不会改变_root_splitter的分割比，但只有central_widget是QSplitter时才有效，如果是使用qt designer
        设计的图形主界面，该方法无效。

        任何情况下，无法添加同名widget组件，因为组件会根据名称进行索引，因此，同名组件不允许存在。

        :param widget:
        :param tab_name:
        :param replace: 存在同名widget时，是否替换，默认不替换，即忽略当前添加操作，否则将已有同名widget替换为传入的widget
        :return:
        """
        if self._content_tab is None:
            sizes = None
            if self._root_splitter is not None:
                sizes = self._root_splitter.sizes()
            central_widget = self.centralWidget()
            if isinstance(central_widget, QSplitter):
                _ = central_widget.widget(1)  # 获得右侧的组件
                self._content_tab = YkTabWidget()
                self._content_tab.setTabPosition(QTabWidget.South)  # 标签放在南方，0-North, 1-South, 2-West, 3-East
                self._content_tab.addTab(_, "sheet 1")
                self._content_tab.addTab(widget, tab_name)
                central_widget.addWidget(self._content_tab)
            if sizes is not None:  # 此时central_widget就是self._root_splitter
                self._root_splitter.setSizes(sizes)
        else:
            if tab_name in self._content_tab.get_tab_names():  # 如果存在同名面板
                if replace:
                    self._content_tab.removeTab(self._content_tab.indexOf(self._content_tab.get_tab_panel(tab_name)))
                    self._content_tab.addTab(widget=widget, a1=tab_name)
                else:
                    ...  # 否则不做任何操作
            else:
                self._content_tab.addTab(widget=widget, a1=tab_name)

    def center(self):
        """
        将窗口移动到屏幕中间

        :return:
        """
        qr = self.frameGeometry()  # 获得窗口
        if qt_version == "pyqt5":
            cp = QDesktopWidget().availableGeometry().center()  # 获得屏幕中心点
        else:
            cp = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        """
        点击关闭按钮时触发的事件

        :param event:
        :return:
        """
        try:
            self.ini_info["size"] = self.geometry()
            reply = QMessageBox.question(self, "项目尚未保存", "是否保存当前项目?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.save()
                write_as_pickle(self.ini_file, self.ini_info)
                self.close()  # 保存后直接退出，此处不能使用event.accept()，因为有时候event不是事件
            else:
                write_as_pickle(self.ini_file, self.ini_info)
                self.close()
                return
        except:
            traceback.print_exc()

        if self.sender() is None:  # 点击右上角×号时，self.sender()为None
            reply = QMessageBox.question(self, "信息", "确认退出?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()
        else:
            self.close()

    def _test_cal_(self):
        a = self._table_widget.get_value("示例计算.苹果单价")
        b = self._table_widget.get_value("示例计算.香蕉单价")
        x = self._table_widget.get_value("示例计算.苹果数量")
        y = self._table_widget.get_value("示例计算.香蕉数量")
        a_t = a * x
        b_t = b * y
        result = a_t + b_t
        self._table_widget.set_value("计算结果.苹果总价", a_t)
        self._table_widget.set_value("计算结果.香蕉总价", b_t)
        self._table_widget.set_value("计算结果.总价", result)

    def set_digits(self):
        digits_str, ok = QInputDialog.getText(self, "设置数据格式", "保留小数位数（最大位数）", QLineEdit.Normal, "2")
        if ok and digits_str.isnumeric():
            self.ini_info.update({"digits": int(digits_str)})

    def set_font(self, font_size=10):
        font_size, ok_pressed = QInputDialog.getText(self, "设置界面字体大小", "字体大小（px）:", QLineEdit.Normal, "")
        if ok_pressed and font_size.isnumeric():
            font_size = int(font_size)
            self.setFont(QFont("Microsoft YaHei", font_size))

    def about(self, tag=None):
        """
        关于菜单的默认动作

        :return:
        """
        # QMessageBox.information(self, "关于", "Powered by open-source software", QMessageBox.Yes)
        dialog = QDialog()
        # 这个btn和上面的btn不是一个
        edit = QTextEdit()
        edit.setHtml(
            "<h1>lib4python</h1>"
            f"<h2>yangke 1.12.4</h2>"

            f'<p style="background-color:rgb(255,255,0)">{self.info=}</p>'
            f'<p style="background-color:rgb(255,255,0)">{self.ui_folder=}</p>'
            f'<p style="background-color:rgb(255,255,0)">{self.menu_ui_file=}</p>'
            f'<p style="background-color:rgb(255,255,0)">{self.table_ui_file=}</p>'
            f'<p style="background-color:rgb(255,255,0)">{self.proj=}</p>'
            f'<p style="background-color:rgb(255,255,0)">{self.settings=}</p>'
            f'<p style="background-color:rgb(255,255,0)">{self.ini_file=}</p>'
            f'<p style="background-color:rgb(255,255,0)">{self.geometry()=}</p>'

            '<p>开发于PyCharm 2020.3.2 (Community Edition)</p>'
            "<p>构建与2021年03月05日</p>"
            "<p>更新于2022年06月27日</p>"

            "Runtime version: 11.0.9.1+11-b1145.63 amd64"
            "VM: OpenJDK 64-Bit Server VM by JetBrains s.r.o."
            "Windows 10 10.0"
            "<p>Powered by open-source software</p>"
        )
        # edit.setReadOnly(True)
        layout = QVBoxLayout(dialog)
        # dialog.setLayout()
        layout.addWidget(edit)

        dialog.setWindowTitle('关于')
        # 让对话框以模式状态显示，即显示时QMainWindow里所有的控件都不可用，除非把dialog关闭
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.resize(900, 300)
        dialog.exec()

    def help(self, tag=None):
        """
        帮助按钮的默认动作

        :return:
        """
        QMessageBox.information(self, "帮助", "暂不支持帮助", QMessageBox.Yes)

    def start_ws_server(self):
        """
        在本机随机的可用端口上启动socket服务，返回服务所在的url地址。

        通过html_widget(local_file)方法可以加载本地静态网页，从而显示Echarts图表，但是，这种方法无法实现图表响应PyQt图形界面上的事件。
        因为PyQt图像界面上的所有鼠标键盘事件产生的数据无法传递给静态的前端页面。为了解决该问题，本函数通过使用websocket实现前端网页与后端
        服务的长连接，使得后台数据发生变化后，可以随时发送给前端网页，由网页端接收数据后动态渲染数据。

        :return:
        """
        server = self.info.get("server")
        if server is None:
            from yangke.web.pyecharts.start_pyecharts_server import start_pyecharts_server
            port = self.settings.get_settings("mainframe.websocket.server").get("port") or 10001  # get_available_port()
            thread = start_threads(start_pyecharts_server, [port, self.callback_func], engine="threading") or port
            html_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "web", "pyecharts", "templates",
                                     "temp_index.html").replace('\\', '/')
            url = f"file:///{html_file}"
            self._html_widget = html_widget(url)
            self.info.update({"server": thread, "port": port, "url_file": url})  # 记录软件开启的服务的pid
        self.display_to_location(self._html_widget, 2)
        return 0

    def stop_ws_server(self):
        server = self.info.get("server")
        if server is None:
            return
        else:
            # if self.info.get("server") is not None and not fake:
            #     stop_ws_serve()
            #     stop_threads(self.info.get("server"))
            #     self.info.update({"server": None, "port": None, "url_file": None})  # 记录软件开启的服务的pid
            self.remove_panel(self._html_widget)

    def set_echarts_option(self, options):
        if self.info.get("server") is None:
            self.start_ws_server()
        else:
            self.display_to_location(self._html_widget, 2)
        if isinstance(options, Chart) or isinstance(options, Grid):
            options1 = options.dump_options_with_quotes()
            DataPackage(cmd="initChart", option=options1).send()  # send方法必须在ws长连接建立后使用

    def remove_panel(self, widget):
        """
        暂不支持
        :param widget:
        :return:
        """
        if isinstance(widget, QWebEngineView):
            if self._content_tab is not None:
                self._content_tab.setCurrentIndex(0)
                self._html_widget.setWindowOpacity(0)

    def echarts_append_data(self, data):
        DataPackage(cmd="appendData", series=data).send()

    def echarts_update_data(self, data):
        """
        更新echarts图标中的数据，需要与echarts_define.js中的数据源对应。
        需要确保传入的data中的元素的数据类型都为数字或字符串。
        本方法会设置echarts_define.js中某个变量为指定的数组。例如：
        示例1：
        data = {"data": [1,2,3,4]}
        self.echarts_update_data(data)
        则相当于将js中的data变量设置为[1, 2, 3, 4]
        示例2：
        data = {"dataset": [["北京", 1], ["上海", 2], ["广州", 3]]}
        self.echarts_update_data(data)
        则相当于将js中的dataset变量设置为[["北京", 1], ["上海", 2], ["广州", 3]]
        示例3：
        # 如果传入的data不是字典，则默认将js中的data变量设置为传入的data
        data = pd.DataFrame(data=[["北京", 1], ["上海", 2], ["广州", 3]])  # DataFrame类型本方法会自动转换为数组
        则相当于将js中的data变量设置为[["北京", 1], ["上海", 2], ["广州", 3]]

        :param data:
        :return:
        """
        if isinstance(data, dict):
            if len(data) == 0:
                return
            key = list(data.keys())[0]
            val = data.get(key)
            data.update({"var": key})
            if isinstance(val, np.ndarray):
                # if val.dtype == "object":  # float64
                data[key] = val.tolist()
            elif isinstance(val, pd.DataFrame):
                data[key] = val.values.tolist()
            elif isinstance(val, pd.Series):
                data[key] = val.tolist()
            elif isinstance(val, list):
                ...
            else:
                logger.error(f"只支持发送数组型数据，如ndarray、Series、DataFrame等，当前发送类型为{type(val)}")
        elif isinstance(data, list):
            data = {"data": data, "var": "data"}
        else:
            logger.error(f"只支持发送数组型数据，如ndarray、Series、DataFrame等，当前发送类型为{type(data)}")

        DataPackage(cmd="updateData", args=data).send()

    def get_echarts_series(self):
        DataPackage(cmd="getSeries").send()
        while not self.info.get("ready"):
            time.sleep(0.1)
        self.info["ready"] = False
        return self.info.get("series")  # 可能返回空值

    def test_figure(self):
        if self.info.get("server") is None:
            self.start_ws_server()
        while not is_ready():
            logger.debug("等待图形渲染服务启动")
            time.sleep(0.01)  # 等待10ms

        from pyecharts.charts import Line
        from pyecharts.charts import Grid

        x_data = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        y_data = [820, 932, 901, 934, 1290, 1330, 1320]
        y_data1 = [y / 2 for y in y_data]

        c = (  # 最外层的小括号只是为了换行方便
            Line()
            .set_global_opts(
                tooltip_opts=opts.TooltipOpts(is_show=False),
                xaxis_opts=opts.AxisOpts(type_="category"),
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
            )
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
                series_name="",
                y_axis=y_data,
                symbol="triangle",
                symbol_size=20,
                is_symbol_show=True,
                label_opts=opts.LabelOpts(is_show=False),
                linestyle_opts=opts.LineStyleOpts(color='blue', width=2, type_="solid"),
                itemstyle_opts=opts.ItemStyleOpts(color='red', border_color='green', border_width=1),
            ).add_yaxis(
                series_name="",
                y_axis=y_data1,
                symbol="emptyCircle",  # emptyCircle无法设置标记点的填充色，因为填充色必然是空
                symbol_size=20,
                is_symbol_show=True,
                label_opts=opts.LabelOpts(is_show=False),
                linestyle_opts=opts.LineStyleOpts(color='red', width=4, type_='dashed'),
                itemstyle_opts=opts.ItemStyleOpts(color='blue', border_color='green', border_width=1),
            )
        )
        grid = Grid(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        grid.add(c, grid_opts=opts.GridOpts(pos_right='3%', pos_left='5%', pos_top='5%', is_show=True))

        self.set_echarts_option(grid)

    def display_to_location(self, widget, location=0):
        """
        将组件显示到软件界面上的某个位置
        :param widget:
        :param location: 0-左侧导航处，1-右侧主内容区
        :return:
        """
        try:
            _ = self.centralWidget()
            if location == 0:
                if _ is None or self.info.get("central_widget") == "input_panel":
                    self.setCentralWidget(widget)
                    self.info["central_widget"] = "input_panel"
                elif isinstance(_, QSplitter):
                    self._root_splitter.replaceWidget(0, widget)
                    self.info["central_widget"] = "splitter"
                elif isinstance(_, QWebEngineView) or isinstance(_, YkDataTableWidget) \
                        or isinstance(_, QTabWidget):
                    self._root_splitter = QSplitter(Qt.Horizontal, self)  # 主面板分为左右两部分
                    self._root_splitter.addWidget(widget)
                    self._root_splitter.addWidget(_)
                    self._root_splitter.setSizes([300, 800])
                    self.setCentralWidget(self._root_splitter)
                    self.info.update({"central_widget": "splitter"})
                else:
                    self.info.update({"central_widget": "input_panel"})
                    self.setCentralWidget(widget)
            elif location == 1:
                if self.info.get("central_widget") == "input_panel":
                    self._root_splitter = QSplitter(Qt.Horizontal, self)  # 主面板分为左右两部分
                    self._root_splitter.addWidget(_)
                    self._root_splitter.addWidget(widget)
                    self._root_splitter.setSizes([300, 800])
                    self.setCentralWidget(self._root_splitter)
                    self.info.update({"central_widget": "root_splitter"})
                elif isinstance(_, QSplitter):
                    splitter_r = _.widget(1)
                    size = _.size()
                    if isinstance(splitter_r, QTabWidget):
                        if isinstance(widget, QTableWidget):
                            self._content_tab.setCurrentIndex(0)
                        else:
                            self._content_tab.setCurrentIndex(1)
                    elif isinstance(splitter_r, QWebEngineView):
                        self._content_tab = QTabWidget(self)
                        self._content_tab.addTab(widget, "表格")
                        self._content_tab.addTab(splitter_r, "图表")  # 将splitter_r添加到tab_widget中时，QT自动从QSplitter中删除该组件
                        self._root_splitter.addWidget(self._content_tab)
                        self._content_tab.setCurrentWidget(widget)
                    elif isinstance(splitter_r, YkDataTableWidget):
                        _.replaceWidget(1, widget)
                elif isinstance(_, QWebEngineView) and isinstance(widget, QTableWidget):
                    self._content_tab = QTabWidget()
                    self._content_tab.addTab(widget, "表格")
                    self._content_tab.addTab(_, "图表")
                    self.setCentralWidget(self._content_tab)
                elif isinstance(widget, QWebEngineView) and isinstance(_, QTableWidget):
                    self._content_tab = QTabWidget()
                    self._content_tab.addTab(_, "表格")
                    self._content_tab.addTab(widget, "图表")
                    self.setCentralWidget(self._content_tab)
                else:
                    self.setCentralWidget(widget)
            elif location == 2:
                if self.info.get("central_widget") == "input_panel":
                    self.display_to_location(widget, 1)
                    return
                elif self.centralWidget() is None:
                    self.setCentralWidget(widget)
                    self.info.update({"central_widget": "some-content"})
                elif isinstance(_, QWebEngineView) and isinstance(widget, QWebEngineView):
                    return
                elif isinstance(_, QWebEngineView) and isinstance(widget, QTableWidget):
                    self._content_tab = QTabWidget()
                    self._content_tab.addTab(widget, "表格")
                    self._content_tab.addTab(_, "图像")
                    self.setCentralWidget(self._content_tab)
                elif isinstance(widget, QWebEngineView) and isinstance(_, QTableWidget):
                    self._content_tab = QTabWidget()
                    self._content_tab.addTab(_, "表格")
                    self._content_tab.addTab(widget, "图像")
                    self.setCentralWidget(self._content_tab)
                elif isinstance(_, QTabWidget):
                    self._content_tab.setCurrentIndex(1)
                elif isinstance(_, QSplitter):
                    splitter_r = _.widget(1)
                    if isinstance(splitter_r, QTabWidget):
                        if isinstance(widget, QTableWidget):
                            self._content_tab.setCurrentIndex(0)
                        else:
                            self._content_tab.setCurrentIndex(1)
                    elif splitter_r is None:  # 虽然是分割区域面板，但面板右侧为空
                        _.addWidget(widget)
                    else:
                        self._content_tab = QTabWidget()
                        if isinstance(splitter_r, QTableWidget) and isinstance(widget, QWebEngineView):
                            self._content_tab.addTab(splitter_r, "表格")
                            self._content_tab.addTab(widget, "图像")
                            self._root_splitter.addWidget(self._content_tab)
                            self._content_tab.setCurrentWidget(self._content_tab)
                        elif isinstance(splitter_r, QWebEngineView) and isinstance(widget, QTableWidget):
                            self._content_tab.addTab(widget, "表格")
                            self._content_tab.addTab(splitter_r, "图像")
                            self._root_splitter.addWidget(self._content_tab)
                            self._content_tab.setCurrentWidget(self._content_tab)
        except RuntimeError:
            logger.debug(f"显示组件{widget}时发生错误，显示失败！")
            pass

    def callback_func(self, info):
        """
        前端向后端发送消息后，都会调用该回调方法，该方法可以是应用程序知道前端请求了什么内容。
        该方法接受到的数据总是为字符串类型。
        该方法的执行由子线程执行，主线程可以等待该方法执行，二者不会相互阻塞。

        :param info:
        :return:
        """
        try:
            info = json.loads(info)
        except json.decoder.JSONDecodeError:
            pass
        if isinstance(info, str):
            self.statusBar1.showMessage(info)
            self.info.update({"ready": True, "msg": info})
        elif isinstance(info, dict) and info.get("series") is not None:
            self.info.update({"series": info.get("series"), "ready": True})
        else:
            ...

    @pyqtSlot(dict)
    def yk_signal_received(self, msg: dict):
        """
        该方法的执行有主线程完成，会阻塞主线程或主线程会阻塞该方法
        :param msg:
        :return:
        """
        ...

    def get_value_of_panel(self, need_unit=True, need_dict=False):
        if self._input_panel is None:
            return None
        if isinstance(self._input_panel, QScrollArea):
            self._input_panel = self._input_panel.widget()
        return self._input_panel.get_values_and_units(need_unit=need_unit, need_dict=need_dict)

    def set_theme(self, theme=None):
        global _app
        if theme is None or isinstance(theme, bool):
            widget = YkInputPanel(from_file=os.path.join(os.path.dirname(__file__), "ui", "ui_panel_set_theme.yaml"))
            if self.ini_info.get("theme") is not None:
                widget.set_value("设置主题", self.ini_info.get("theme"))
            dialog = YkDialog(self, title="设置界面风格", widget=widget)
            widget.apply_btn_connect()
            # 让对话框以模式状态显示，即显示时QMainWindow里所有的控件都不可用，除非把dialog关闭
            dialog.set_size(300, 300)
            self.info.update({"set_theme_dialog": dialog, "set_theme_widget": widget})
        else:
            if theme.endswith(".xml"):
                apply_stylesheet(_app, theme=theme)
                self.ini_info.update({"theme": theme[:-4]})
            else:
                apply_stylesheet(_app, theme=f"{theme}.xml")
                self.ini_info.update({"theme": theme})

    def _set_theme(self):
        sender = self.sender()
        dialog = self.info.get("set_theme_dialog")
        # noinspection all
        _ = sender.text()
        if _ == "确定" or _ == "应用":
            widget: YkInputPanel = self.info.get("set_theme_widget")
            value = widget.get_item("设置主题").get_value()
            if value == "default":
                self.ini_info.update({"theme": None})  # 主题更改后，无法恢复为默认，只能重新加载
                write_as_pickle(self.ini_file, self.ini_info)
                self.statusBar1.showMessage(f"默认主题需要重启软件！")
            else:
                apply_stylesheet(_app, theme=f"{value}.xml")
            self.ini_info.update({"theme": value})
            write_as_pickle(self.ini_file, self.ini_info)
        if _ == "确定" or _ == "取消":
            dialog.close()

    def set_value_of_panel(self, values=None, panel=None):
        """
        设置输入面板各项的值，如果有多个输入面板，最好手动传入面板实例或面板标签名

        :param values:
        :param panel:
        :return:
        """
        if values is None:
            return
        if panel is not None:
            if isinstance(panel, str):
                panel = self._input_tab.get_tab_panel(panel)
        panel = panel or self._input_panel
        panel.set_values(values)

    def set_window_size(self):
        """
        设置窗口的大小及显示位置

        """
        size = self.ini_info.get("size")
        if size is not None:
            if isinstance(size, QRect):
                self.setGeometry(size)
            else:
                # noinspection all
                self.setGeometry(*size)
            return

        need_center = False
        size = get_settings("mainframe.geometry", self.setting_file)
        if len(size) > 0:
            if size == "maximize":
                self.showMaximized()
            elif size == "fullscreen":
                self.showFullScreen()
            else:
                if isinstance(size, list):
                    pass
                else:
                    size = eval(size)
                if len(size) == 2:
                    size.insert(0, 0)
                    size.insert(0, 0)
                    need_center = True
                x, y, w, h = size
                self.setGeometry(x, y, w, h)
        else:
            self.setGeometry(0, 0, 1400, 800)

        if need_center:
            self.center()


def run_app(cls, theme=None):
    """
    运行Qt主窗口类。

    可支持的主题包括：
    default_light.xml
    default_dark.xml
    dark_amber.xml
    dark_blue.xml
    dark_cyan.xml
    dark_lightgreen.xml
    dark_pink.xml
    dark_purple.xml
    dark_red.xml
    dark_teal.xml
    dark_yellow.xml
    light_amber.xml
    light_blue.xml
    light_blue_500.xml
    light_cyan.xml
    light_cyan_500.xml
    ...

    :param theme: 指定界面的主题，可以改变界面的风格，可取值"default_light", "default_dark", "dark_amber"
    """
    global _app
    _app = QApplication(sys.argv)
    # app.setFont(QFont("Microsoft YaHei", 12))
    # app.setStyleSheet("font-size: 20px")
    _: YkWindow = cls()
    if theme is None:
        pass
    else:
        apply_stylesheet(_app, theme=theme, extra={})
    if _.ini_info.get("theme") is not None and _.ini_info.get("theme") != "default":
        _.set_theme(theme=_.ini_info.get("theme"))
    # _.setFont(QFont("Microsoft YaHei", 12))
    sys.exit(_app.exec_())


def deal_connect_func(connect, widget: QWidget | QPushButton):
    """
    根据connect字符串的描述，获取与widget相关的函数对象，以便后续添加事件连接
    """
    _ = connect.split(".")
    base_name = _[1] if len(_) == 2 and isinstance(_, list) else connect  # 处理方法前面的root或self标记
    # ----------------------- 确保temp_connect中包括()代表的参数 ------------------------
    base_name.replace("()", "")  # 如果两个括号相连，说明没有参数
    _res = re.findall("\((.+)\)", base_name)
    _res_ = []
    for _ in _res:
        if _ == 'True':
            _res_.append(True)
        elif _ == "False":
            _res_.append(False)
        else:
            _res_.append(_)
    # ----------------------- 确保temp_connect中包括()代表的参数 ------------------------

    # ----------------------- 查找指定的方法所属的QWidget对象 ----------------------------
    if len(_res_) > 0:
        temp_connect = base_name.split("(")[0]
    else:
        temp_connect = base_name

    parent_widget = widget
    has_func = hasattr(widget, temp_connect)
    while not has_func and parent_widget is not None:
        parent_widget = widget.parentWidget()
        has_func = hasattr(parent_widget, temp_connect)
    if parent_widget is None:
        logger.warning(f"未找到名为{temp_connect}的方法！")
        return
    # ----------------------- 查找指定的方法所属的QWidget对象 ----------------------------

    if len(_res) > 0:  # lambda表达式在这里会报错，window找不到
        _func = functools.partial(parent_widget.__getattribute__(temp_connect), *_res_)
        # _func = eval(f"lambda: window.{temp_connect}")
    else:
        _func = parent_widget.__getattribute__(temp_connect)
    return _func


def connect_event_by_dict(widget: QPushButton | QComboBox | QWidget | QAction, desc):
    """
    根据yaml文件中的button字典将按钮和应用程序的根方法连接起来，使按钮的点击事件可以正常触发。
    也可以触发combox的currentTextChanged事件。
    根据字典中定义的函数方法，将函数方法与widget的指定事件连接起来。

    desc = {"signal": "currentTextChanged", "connect": "loss_changed()"}  # 连接widget.currentTextChanged方法
    desc = {"signal": "clicked", "connect": "loss_changed"}
    desc = "loss_changed"  # 默认连接widget.clicked方法

    :param widget: 按钮所属的QWidget
    :param desc: str/dict,按钮及按钮点击事件的描述，例如"root.choose()"
    :return:
    """
    event = 'clicked'
    if isinstance(desc, str):  # 说明desc是连接的方法的名称
        connect = desc
        # elif isinstance(desc, dict):
    else:
        event = desc.get("signal") or "clicked"  # 获取事件

        if event == "currentTextChanged" or "triggered":
            # 说明widget是QCombobox或者QAction，需要连接的事件是currentTextChanged或者triggered
            connect = desc.get("connect")  # 连接的方法
        else:
            btn = desc.get("button")
            if not btn:
                btn = desc
            connect = btn.get("on_click") or "root.btn_clicked"

    connect = connect[:-2] if connect.endswith("()") else connect  # 处理方法后面的括号

    _ = connect.split(".")
    base_name = _[1] if len(_) == 2 and isinstance(_, list) else connect  # 处理方法前面的root或self标记

    # 至此，base_name是需要连接的方法
    if connect is not None:
        func = None
        parent = widget
        try:
            while not hasattr(parent, base_name):  # 如果父组件不存在当前的方法，则查询更上一级组件
                if parent is not None:
                    parent = parent.parent()
                else:
                    break
            # 至此，parent为查询到带有指定方法的组件
            func = eval(f"parent.{base_name}")
            widget.disconnect()  # 一定要先断开已有的链接，否则可能单次点击导致事件执行多次
        except AttributeError:  # 也有可能一直到最顶层都没有指定的方法，则报错
            # traceback.print_exc()
            if hasattr(widget, "text"):
                logger.error(
                    f"{widget.__class__.__name__}{widget.text()}及其父组件均没有指定的方法（{base_name}），请检查配置文件")
            else:
                logger.error(
                    f"{widget.__class__.__name__}{widget}及其父组件均没有指定的方法（{base_name}），请检查配置文件")
        except SyntaxError:
            # traceback.print_exc()
            logger.error(f"{func}方法名错误，请检查")
        except TypeError:
            # traceback.print_exc()
            logger.error(f"断开组件已有事件链接失败！{base_name}")

        # 至此，func即是需要连接的函数对象
        try:
            # logger.info(f"{widget=}, {widget.clicked=}")
            if func is not None:
                if event == "clicked":
                    # noinspection all
                    widget.clicked.connect(func)
                elif event == "currentTextChanged":
                    # noinspection all
                    widget.currentTextChanged.connect(func)
                elif event == "triggered":  # QAction
                    # noinspection all
                    widget.triggered.connect(func)
        except AttributeError:  # 也有可能一直到最顶层都没有指定的方法，则报错
            logger.error(f"{widget.__class__.__name__}及其父组件均没有指定的方法（{base_name}），请检查配置文件")
        except SyntaxError:
            # traceback.print_exc()
            logger.error(f"{func}方法名错误，请检查")
        except TypeError:
            # traceback.print_exc()
            logger.error(f"断开组件已有事件链接失败！{base_name}")


class YkItem(QWidget):
    def __init__(self, label="Label",
                 value=None,
                 unit=None,
                 size=None,
                 indent=0,
                 draggable=False,
                 struct=10,
                 margins=(10, 10, 10, 10)
                 ):
        """
        一种输入项，可以带下拉列表单位。示例如下：
        YkItem("环境温度1", "10", {value:["℃", "K"], selected_idx: 0}, size=[100, 20, 50])
        YkItem("环境温度2", "10", {value:["℃", "K"], selected_val: "℃"})
        YkItem("城市", {value: ["北京", "上海", "西安", "武汉"], selected_val: "北京"})
        YkItem("数据文件", "请选择文件", '<button on-click="choose">选择文件</button>')  # 需要组件或其父类中存在choose方法
        YkItem("参数", '<input type=checkbox checked="checked" text="参数名1" /><input type=checkbox text="参数名2" />')
        YkItem("参数", '<input type=checkbox checked="unchecked" text="var1" />', '<input type=checkbox text="var2">')

        如果需要给combobox添加值改变事件，则示例如下：
        YkItem("环境温度2", {'value':['MSE', 'CrossEntropy', 'PriorLoss'], 'text_changed': 'loss_changed'})

        :param label:
        :param value:
        :param unit:
        :param size: 三个子组件的宽度
        :param draggable: 是否可以拖拽，默认不可以
        :param margins: QHBoxLayout中子组件与父组件的间距，分别表示(left, top, right, bottom)
        """
        # noinspection PyArgumentList
        super(YkItem, self).__init__()
        self.btn_info = {}
        self.size1 = size or {}
        if isinstance(self.size1, list):
            self.size1 = {"width": self.size1}
        self.label = self.deal_component_definition(label, prefer="label")
        self.value = self.deal_component_definition(value, prefer="value")
        self.unit = self.deal_component_definition(unit, prefer="unit")
        self.indent = indent
        self.struct = struct or 10
        self.margins = margins
        self.init_ui()
        self.scale = 1  # 宽度方向的缩放
        self.draggable = draggable

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        """
        使得宽度方向可以自适应

        :param a0:
        :return:
        """
        width, height = a0.size().width(), a0.size().height()
        width_cur = self.size1.get("width") or [self.label.width(), self.value.width(), self.unit.width()]
        total_width = 0
        for x in width_cur:
            total_width = x + total_width
        self.scale = max(width * 0.95 / total_width, 1)
        new_size = []
        for i in width_cur:
            new_size.append(int(i * self.scale))
        self.set_size({"width": new_size})
        super(YkItem, self).resizeEvent(a0)

    def deal_component_definition(self, code, prefer="label"):
        """
        根据子组件的定义对象，生成子组件，并返回。
        如果code为自定义对象，则code必须包括get_selected_value()和get_values_list()两个方法。
        :return:
        """
        if code is None:
            return QLabel()
        res = None
        if isinstance(code, QWidget):
            return code
        elif isinstance(code, str):
            if is_js_str(code):
                from lxml import etree
                ele = etree.HTML(code)
                _type = "button" if len(ele.xpath("//button")) == 1 else None
                if _type is None:  # 说明不是<button>标签
                    _type = "label" if len(ele.xpath("//label")) == 1 else _type
                if _type is None:  # 说明不是<label>标签
                    _input = ele.xpath("//input")
                    _type = ele.xpath("//input/@type")[0] if len(_input) == 1 else _type
                if _type == "button":
                    on_click = ele.xpath("//button/@on-click")
                    on_click = None if len(on_click) == 0 else on_click[0]
                    text = ele.xpath("//button/text()")
                    text = text[0] if len(text) == 1 else "按钮"
                    res = QPushButton(text)
                    self.btn_info.update({res: on_click.strip()})
                elif _type == "label":
                    ...
                elif _type == "text":
                    text = str(ele.xpath("//input/@value")[0])
                    res = QLineEdit(text)
                elif _type == "checkbox":  # 以下类型均为js中<input>标签的类型
                    ...
                elif _type == "color":
                    ...
                elif _type == "date":
                    ...
                elif _type == "file":
                    ...
                elif _type == "image":
                    ...
                elif _type == "month":
                    ...
                elif _type == "password":
                    ...
                elif _type == "time":
                    ...
            else:
                if prefer == "label":
                    res = QLabel(code)
                    res.setToolTip(code)
                elif prefer == "value":
                    res = QLineEdit(code)
                else:
                    res = QLabel(code)
                    res.setToolTip(code)
        elif isinstance(code, list):
            code = [str(x) for x in code]  # QComboBox只支持添加元素为字符串的类型
            res = QComboBox(self)
            res.addItems(code)
            res.setCurrentIndex(0)

        elif isinstance(code, dict):
            value = code.get("value")
            value = [str(_) for _ in value]
            if isinstance(value, list):
                res = QComboBox()
                res.addItems(value)
                selected_idx = code.get("select_idx")
                selected_val = code.get("selected_val")
                try:
                    if selected_idx is not None:
                        res.setCurrentIndex(selected_idx)
                    elif selected_val is not None:
                        res.setCurrentText(selected_val)
                    else:
                        res.setCurrentIndex(0)
                except:
                    logger.error(f"设置Combobox的当前选择项时发生错误，{value=}, {selected_idx=}, {selected_val=}")

                text_changed = code.get("text_changed")
                if text_changed is not None:
                    self.btn_info.update({res: {"signal": "currentTextChanged", "connect": text_changed}})

        elif is_number(code):
            code = str(code)
            if prefer == "label":
                res = QLabel(code)
            elif prefer == "value":
                res = QLineEdit(code)
            else:
                res = QLabel(code)
        else:
            try:
                val_list = code.get_values_list()
                sel = code.get_selected_value()
                res = self.deal_component_definition(prefer=prefer, code={"value": val_list, "selected_val": sel})
            except:
                res = QLabel(code.__str__())
        return res

    def __str__(self):
        return f"{self.label}={self.label.text()}, {self.value}={self.value.text()}"

    def apply_btn_connect(self):
        """
        延迟连接的按钮事件，因为窗口初始化时，按钮等组件还没有添加到面板中，因此按钮的父组件为空，无法将按钮与按钮的父组件或爷组件等的事件关联起来
        ，因此延迟连接这类按钮时间，该方法在主窗口初始化完成后，有主窗口调用。
        :return:
        """
        for btn, btn_dict in self.btn_info.items():
            connect_event_by_dict(btn, btn_dict)

    def init_ui(self):
        """
        添加标签、数值和单位三个图形项
        :return:
        """
        # self.setPalette(QPalette(QtCore.Qt.red))
        # self.setAutoFillBackground(True)
        self.setMinimumSize(20, 5)

        h_box = QHBoxLayout()
        h_box.setContentsMargins(9, 2, 2, 9)  # 设置每一项上下左右的边距
        h_box.setSpacing(1)
        if self.indent > 0:
            h_box.addStrut(self.indent)
        h_box.addWidget(self.label)
        h_box.addStrut(self.struct)
        h_box.addWidget(self.value)
        if self.unit is not None:
            h_box.addStrut(self.struct)
            h_box.addWidget(self.unit)
        self.setLayout(h_box)
        h_box.setContentsMargins(*self.margins)
        self.set_size(self.size1)
        # self.setStyleSheet("background-color:green;padding:2;")

    def get_value(self):
        value = None
        if isinstance(self.value, QLineEdit):
            value = self.value.text()
        elif isinstance(self.value, QComboBox):
            value = self.value.currentText()
        elif isinstance(self.value, QCheckBox):
            value = []
            for item in self.findChildren(QCheckBox):
                item: QCheckBox = item
                if item.isChecked():
                    value.append(item.text())
        return value

    def get_unit(self):
        unit = None
        if self.unit is not None:
            if isinstance(self.unit, QPushButton):
                unit = self.unit.text()
            elif isinstance(self.unit, QLabel) or isinstance(self.unit, QLineEdit):
                unit = self.unit.text()
            else:
                unit = self.unit.currentText()
        return unit

    def get_value_and_unit(self, need_label=False):
        if need_label:
            return self.label.text(), self.get_value(), self.get_unit()
        else:
            return self.get_value(), self.get_unit()

    def set_value(self, value):
        """
        设置YkItem项的值，如果value=None，则当现有值不为空时，不进行任何操作，如果value=''，如果现有值不为None，则将其置为''。
        即这里的None和空字符串''是不同的含义。

        :param value:
        :return:
        """
        value = str(value)
        if value is None:
            return
        if isinstance(self.value, QLineEdit):
            self.value.setText(value)
        elif isinstance(self.value, QComboBox):
            # 没有判断设置的值是否在可选的列表中
            self.value.setCurrentText(value)
        elif isinstance(self.value, QHBoxLayout):  # 说明是复选框
            for item in self.findChildren(QCheckBox):
                item: QCheckBox = item
                if item.text() in value:
                    item.setChecked(True)

    def set_unit(self, unit):
        if unit is None:
            return
        unit = str(unit)
        if self.unit is not None:
            if isinstance(self.unit, QComboBox):
                available_text = []
                for i in range(self.unit.model().rowCount()):
                    available_text.append(self.unit.itemText(i))
                if unit in available_text:
                    self.unit.setCurrentText(unit)  # 如果设置的值不在unit可选值中，不会报错，但本语句将无效果
                else:
                    logger.debug(f"设置的单位{unit}不在可选单位列表{available_text}中")
            elif isinstance(self.unit, QLabel) or isinstance(self.unit, QLineEdit):
                self.unit.setText(unit)

    def set_size(self, size):
        # ----------------------------设置组件大小--------------------------------
        size1 = size or self.size1  # 不要改变初始的size1的值
        width = size1.get("width")
        if isinstance(width, int):
            width = [width, width, width]
        if isinstance(width, list):
            if len(width) >= 1:
                # self.label.setFixedWidth(int(width[0]))
                self.label.setMinimumWidth(int(width[0]))
            if len(width) >= 2:
                self.value.setMinimumWidth(int(width[1]))
            if len(width) >= 3 and self.unit is not None:
                self.unit.setMinimumWidth(int(width[2]))
        # ----------------------------设置组件大小--------------------------------

    def get_size(self):
        """
        返回三个子组件的真是宽度

        :return:
        """
        width1 = self.label.size().width() if self.label is not None else 0
        width2 = self.value.size().width() if self.value is not None else 0
        width3 = self.unit.size().width() if self.unit is not None else 0

        return [width1, width2, width3]

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        if self.draggable:
            if a0.button() == Qt.LeftButton:
                drag = QDrag(self)
                mime_data = QMimeData()
                unit = None
                if self.unit is None:
                    ...
                elif isinstance(self.unit, QComboBox):
                    unit = self.unit.currentText()
                else:
                    unit = self.unit.text()
                mime_data.setText(str({"cls": "YkItem", 'label': self.label.text(), "value": self.value.text(),
                                       "unit": unit}))
                drag.setMimeData(mime_data)
                drag.exec()  # exec()不会阻塞主函数，exec_()会阻塞主函数
        else:
            super().mousePressEvent(a0)


def layout_to_widget(layout):
    """
    讲PyQt5中的layout转换为Widget。
    用于：
    在QSplitter中添加内容时，只能使用QWidget类对象，如果是用户创建的QVBoxLayout内容，则无法添加，可以使用该方法转换后添加。

    :param layout:
    :return:
    """

    class YKWidget(QWidget):
        def __init__(self):
            super(YKWidget, self).__init__()
            self.setLayout(layout)

    widget = YKWidget()
    return widget


def QYKFigure(x=None, y=None, xlim=None, ylim=None,
              fig_type=None, figsize=None, dpi=None, facecolor=None, edgecolor=None,
              linewidth=0.0,
              frameon=None, subplotpars=None, tight_layout=None, constrained_layout=None,
              title=None, xlabel=None):
    """
    在PyQt5面板中绘制matplotlib图形，该方法返回一个QWidget图形对象

    :param ylim: (bottom: float, top: float)
    :param xlim: (bottom: float, top: float)
    :param xlabel:
    :param x:
    :param y:
    :param fig_type: scatter/bar/hist/curve
    :param figsize:
    :param dpi:
    :param facecolor:
    :param edgecolor:
    :param linewidth:
    :param frameon:
    :param subplotpars:
    :param tight_layout:
    :param constrained_layout:
    :param title:
    :return:
    """
    import matplotlib
    matplotlib.use("Qt5Agg")
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.figure import Figure
    import matplotlib.pyplot as plt
    from matplotlib.axes._subplots import Axes

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False

    class Qt5Figure(FigureCanvas):
        def __init__(self, figsize=None, dpi=None, facecolor=None, edgecolor=None, linewidth=0.0,
                     frameon=None, subplotpars=None, tight_layout=None, constrained_layout=None):
            self.figure = Figure(figsize=figsize, dpi=dpi, facecolor=facecolor, edgecolor=edgecolor,
                                 linewidth=linewidth, frameon=frameon, tight_layout=tight_layout,
                                 subplotpars=subplotpars, constrained_layout=constrained_layout)

            # 在父类中激活Figure窗口，此句必不可少，否则不能显示图形
            super(Qt5Figure, self).__init__(self.figure)
            self.axes: Axes = self.figure.add_subplot(111)
            if title is not None:
                self.figure.suptitle(title)
            self.axes.set_xlabel(xlabel)
            self.axes.set_ylim(auto=True)
            self.axes.set_xlim(auto=True)
            self.axes.grid(axis="both", color="y", linestyle=":", linewidth=1)

            if fig_type is not None:
                if fig_type == "scatter":
                    self.scatter(x, y)
                elif fig_type == "bar":
                    self.bar(x, y)
                elif fig_type == "hist":
                    self.hist(x)
                elif fig_type == "curve":
                    self.curve(x, y)
            else:
                self.curve(x, y)
            # self.figure.tight_layout()

        def add_fig(self, fig_type, x=None, y=None, **kwargs):
            """
            在当前图中添加图。
            一般用于同一个坐标系多条曲线的情况，添加第二条曲线时即可使用该方法。

            :param fig_type: 新图的类型，curve/scatter/bar/hist
            :param x:
            :param y:
            :return:
            """
            if fig_type == "scatter":
                self.scatter(x, y, **kwargs)
            elif fig_type == "bar":
                self.bar(x, y, **kwargs)
            elif fig_type == "hist":
                self.hist(x, **kwargs)
            elif fig_type == "curve":
                self.curve(x, y, **kwargs)
            self.figure.tight_layout()

        def curve(self, x, y, **kwargs):
            if isinstance(x, float) or isinstance(x, int):
                x = [x]
            if isinstance(y, float) or isinstance(y, int):
                y = [y]
            self.axes.plot(x, y, **kwargs)

        def scatter(self, x_, y_, **kwargs):
            """
            散点图
            :param x_:
            :param y_:
            :return:
            """
            if isinstance(x_, float) or isinstance(x_, int):
                x_ = [x_]
            if isinstance(y_, float) or isinstance(y_, int):
                y_ = [y_]
            x_ = np.array(x_)
            y_ = np.array(y_)
            if x_.shape != y_.shape:
                if x_.shape[0] == y_.shape[0]:
                    x_ = np.repeat(x_, y_.shape[1])
                elif x_.shape[0] == y_.shape[1]:
                    x_ = np.tile(x_, y_.shape[0])
                y_ = y_.flatten()
            if x_.shape != y_.shape:
                raise ValueError("散点图的数据列表长度不等，且无法扩展到相同维度")
            self.axes.scatter(x_, y_, **kwargs)

        def bar(self, x_, y_, **kwargs):
            """
            柱状图
            :param x_: 列表或数值
            :param y_: 列表或数值
            :return:
            """
            if isinstance(x_, float) or isinstance(x_, int):
                x_ = [x_]
            if isinstance(y_, float) or isinstance(y_, int):
                y_ = [y_]
            self.axes.bar(x_, y_, **kwargs)

        def hist(self, value, bins=10):
            """
            直方图
            :param value:
            :param bins:
            :return:
            """
            self.axes.hist(value, 10)

        def show_control_panel(self):
            """
            显示图片的控制面板

            :return:
            """
            # todo
            pass

        def hide_control_panel(self):
            """
            隐藏控制面板

            :return:
            """
            # todo
            pass

    return Qt5Figure()


def set_menu_bar(window: QMainWindow, from_file="ui_menu.yaml"):
    """
    根据ui_menu.yaml文件定义的菜单栏菜单项信息设置window窗口的菜单栏

    ui_menu.yaml示例文件
------------------------------------------------------------------------------------
menu:
  - # 第一个菜单ribbon
    name: "文件"
    items:
      - action_name: "设置数据文件"
        short_cut: "Ctrl+Q"
        connect: "self.set_data_file"
  - # 种群图类型
    name: "设置"
    items:
      - action_name: "计算设置"
        connect: "self.set_calculate"
      - action_name: "遗传算法设置"
        connect: "self.set_algorithm"
      - action_name: "图像显示设置"
        connect: "self.set_display"
  -
    name: "帮助"
    items:
      - action_name: "关于"
      - action_name: "帮助"
------------------------------------------------------------------------------------

    :param window:
    :param from_file:
    :return:
    """
    menu_bar = window.menuBar()
    menu_bar.clear()
    menus = get_settings("menu", setting_file=from_file)
    for ribbon in menus:
        temp_ribbon = menu_bar.addMenu(_(ribbon.get("name")))
        actions = ribbon.get("items")
        for item in actions:
            temp_action = QAction(item.get("action_name"), window)
            if item.get("short_cut") is not None:
                temp_action.setShortcut(item.get("short_cut"))
            temp_connect: str = item.get("connect")
            if temp_connect is not None:
                if temp_connect.startswith("self."):
                    temp_connect = temp_connect.replace("self.", "")

                # ----------------------- 确保temp_connect中包括()代表的参数 ------------------------
                temp_connect.replace("()", "")  # 如果两个括号相连，说明没有参数
                _res = re.findall("\((.+)\)", temp_connect)
                # if "(" not in temp_connect:
                #     temp_connect = f"{temp_connect}()"
                # ----------------------- 确保temp_connect中包括()代表的参数 ------------------------

                try:
                    if len(_res) > 0:  # lambda表达式在这里会报错，window找不到
                        temp_connect = temp_connect.split("(")[0]
                        _res = _res[0]
                        _func = functools.partial(eval(f"window.{temp_connect}"), _res)
                        # _func = eval(f"lambda: window.{temp_connect}")
                    else:
                        _func = eval(f"window.{temp_connect}")
                    # noinspection all
                    temp_action.triggered.connect(_func)
                except AttributeError as e:
                    logger.error(f"应用程序类{window.__class__.__name__}中不存在方法：{e}")
            temp_ribbon.addAction(temp_action)

    # logger.debug("加载YkDataTableWidget")


class YkDataTableWidget(QTableWidget):

    def __init__(self, from_file="table_data.yaml", root_window=None, **kwargs):
        """

        数据表格组件，配置的table_data.yaml文件参见ui/table_data1.yaml;ui/table_data2.yaml;table_data_single_calculate.yaml

        以下yaml文件内容向表格中添加一个按钮，按钮链接表格组件的self.single_calculate方法
        ---------------------- table.yaml ----------------------
        button:
          - name: "计算"
            range: "(2,4)"  # 按钮位于表格的第三列四行
            connect: "self.single_calculate"
        --------------------------------------------------------
            self.single_calculate方法必须先传入，然后初始化，例如：
        ---------------------- example.py ----------------------
        def calculate:
            # calculate中需要完成的操作
            pass

        YkDataTableWidget.single_calculate = calculate
        table_widget = YkDataTableWidget(from_file = "table.yaml")
        --------------------------------------------------------

        :param from_file: 构建本实例的yaml文件
        :param root_window: 本表格所属的应用程序对象，为QMainWindow类实例
        :param kwargs:
        """
        self.root_window = root_window
        super(YkDataTableWidget, self).__init__()
        if from_file is None:
            settings = YkDict({})
        elif not os.path.exists(from_file):
            logger.debug(f"YkDataTableWidget的数据设置文件<{from_file}>未找到，使用空文件代替！")
            settings = YkDict({})
        else:
            settings = get_settings(setting_file=from_file)
        data = settings.get("data") or {}
        buttons = settings.get("button") or {}
        width1 = settings.get("width")

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # noinspection all
        self.customContextMenuRequested.connect(self.pop_custom_menu)

        self.columns = 20
        self.rows = 100
        self.setRowCount(self.rows)
        self.setColumnCount(self.columns)
        # 初始化var_loc用于存储表格中记录的数值的索引位置，格式为：
        # {"title_1": {"label_1": (x_left_top, y_left_top), "label_2": (x1, y1)}, "title_2": {}, ...}
        # 对应table_data.yaml的格式
        self.var_loc = {}
        self.buttons = {}

        # noinspection all
        self.cellPressed.connect(self.cellPressedEvent)

        for domain in data:
            title = domain.get("title")
            # -------------------- 处理range参数，生成可以直接使用的x0,y_left_top,width,rows-------------------------------
            domain_range = eval(domain.get("range")) or (0, 0)
            x_left_top, y_left_top, width, height = (0, 0, 3, 0)
            if len(domain_range) == 2:
                x_left_top, y_left_top = domain_range
            elif len(domain_range) == 3:
                x_left_top, y_left_top, width = domain_range
            elif len(domain_range) == 4:
                x_left_top, y_left_top, width, height = domain_range
            # -------------------- 处理range参数，生成可以直接使用的x0,y_left_top,width,rows-------------------------------
            # -------------------- 处理background/foreground/align参数 -------------------------------
            background = domain.get("background") or "#ffffff"
            foreground = domain.get("foreground") or "#000000"
            if background.startswith("QBrush"):
                background = eval(background)
            else:
                background = QBrush(QColor(background))
            if foreground.startswith("QBrush"):
                foreground = eval(foreground)
            else:
                foreground = QBrush(QColor(foreground))
            row_index, col_index = y_left_top, x_left_top
            if title is not None:  # 表格中的小分区
                items = domain.get("items") or []
                height = len(items)
                if height == 0:
                    height = len(items)
                self._set_row_column_count(x_left_top, y_left_top, width, height)
                align = self._get_align(item_dict=domain, default="AlignCenter")
                label_align = domain.get("items_text_align")
                label_align = Qt.AlignCenter if label_align == "center" else label_align
                label_align = Qt.AlignRight if label_align == "right" else label_align
                label_align = Qt.AlignLeft if label_align == "left" else label_align
                label_align = label_align or Qt.AlignLeft
                unit_align = domain.get("items_unit_align")
                unit_align = Qt.AlignCenter if unit_align == "center" else unit_align
                unit_align = Qt.AlignRight if unit_align == "right" else unit_align
                unit_align = Qt.AlignLeft if unit_align == "left" else label_align
                unit_align = unit_align or Qt.AlignLeft
                # -------------将表格第一行单元格合并，并将标题内容填入第一行，且设置第一行style----------------
                self.setSpan(row_index, col_index, 1, width)
                self.setItem(row_index, col_index, QTableWidgetItem(title))
                self.item(row_index, col_index).setBackground(
                    background)  # 这里itemAt()用来设置颜色只有第一条设置语句有效，后续无效，测试发现item()函数可用
                self.item(row_index, col_index).setForeground(foreground)
                self.item(row_index, col_index).setTextAlignment(align)
                self.var_loc[title] = {}
                # -------------将表格第一行单元格合并，并将标题内容填入第一行，且设置第一行style----------------

                # --------------------------填充数据行内容------------------------------
                for i, item in enumerate(items):
                    label = item.get("label") or ""
                    value = item.get("value") or ""
                    unit = item.get("unit") or ""
                    x = row_index + i + 1
                    merge_label = item.get("merge_label_row_col")
                    if merge_label is not None:
                        merge_row, merge_col = eval(merge_label)
                        self.setSpan(x, col_index, merge_row, merge_col)
                    merge_value = item.get("merge_value_row_col")
                    if merge_value is not None:
                        merge_row, merge_col = eval(merge_value)
                        self.setSpan(x, col_index + 1, merge_row, merge_col)
                    self.setItem(x, col_index, QTableWidgetItem(label))
                    self.setItem(x, col_index + 1, QTableWidgetItem(value))
                    if isinstance(unit, str):
                        self.setItem(x, col_index + 2, QTableWidgetItem(unit))
                    elif isinstance(unit, list):
                        box = QComboBox()
                        box.addItems(unit)
                        self.setCellWidget(x, col_index + 2, box)
                    self.var_loc[title].update({label: (x, col_index + 1)})
                    self.item(x, col_index).setTextAlignment(label_align)
                    if isinstance(unit, str):
                        self.item(x, col_index + 2).setTextAlignment(unit_align)
                # --------------------------填充数据行内容------------------------------
                # --------------------------设置数据行格式------------------------------
                for i in range(1, height + 1):
                    x = row_index + i
                    self.item(x, col_index).setBackground(background)
                    self.item(x, col_index).setForeground(foreground)
                    self.item(x, col_index + 1).setBackground(background)
                    self.item(x, col_index + 1).setForeground(foreground)
                    if isinstance(unit, str):
                        self.item(x, col_index + 2).setBackground(background)
                        self.item(x, col_index + 2).setForeground(foreground)
                # --------------------------设置数据行格式------------------------------
            else:
                label = domain.get("label")
                value = domain.get("value")
                unit = domain.get("unit")
                if height == 0:
                    height = 1
                self._set_row_column_count(x_left_top, y_left_top, width, height)
                merge_label = domain.get("merge_label_row_col")
                merge_row_label, merge_col_label = 1, 1
                if merge_label is not None:
                    merge_row_label, merge_col_label = eval(merge_label)
                    self.setSpan(row_index, col_index, merge_row_label, merge_col_label)
                merge_value = domain.get("merge_value_row_col")
                merge_row_value, merge_col_value = 1, 1
                if merge_value is not None:
                    merge_row_value, merge_col_value = eval(merge_value)
                    self.setSpan(row_index, col_index + 1, merge_row_value, merge_col_value)

                align = self._get_align(domain, "AlignLeft")

                # --------------------------------- 按照参数类型添加不同组件 ---------------------------------
                if isinstance(value, bool):  # 如果参数取值为bool类型，则使用QCheckBox组件就可以很好的满足要求
                    check_box = QCheckBox(label)
                    check_box.setChecked(value)
                    self.setSpan(row_index, col_index, merge_row_label, merge_col_label)
                    self.setCellWidget(row_index, col_index, check_box)
                else:
                    self.setItem(row_index, col_index, QTableWidgetItem(label))
                    self.setItem(row_index, col_index + merge_col_label, QTableWidgetItem(value))
                    self.setItem(row_index, col_index + merge_col_label + merge_col_value, QTableWidgetItem(unit))
                # --------------------------------- 按照参数类型添加不同组件 ---------------------------------

                # --------------------------------- 按照参数类型更新参数所在的位置 ---------------------------------
                if isinstance(value, bool):  # 布尔型设置项的取值就是布尔型组件本身的坐标
                    self.var_loc.update({label: (row_index, col_index)})
                else:
                    self.item(row_index, col_index).setTextAlignment(align)
                    self.item(row_index, col_index).setBackground(background)
                    self.item(row_index, col_index).setForeground(foreground)
                    self.item(row_index, col_index + merge_col_label).setBackground(background)
                    self.item(row_index, col_index + merge_col_label).setForeground(foreground)
                    self.item(row_index, col_index + merge_col_label + merge_col_value).setBackground(background)
                    self.item(row_index, col_index + merge_col_label + merge_col_value).setForeground(foreground)
                    self.var_loc.update({label: (row_index, col_index + merge_col_label)})
                # --------------------------------- 按照参数类型更新参数所在的位置 ---------------------------------

        if width1 is not None:
            width1 = eval(width1)
            for i, w in enumerate(width1):
                self.setColumnWidth(i, w)

        self.apply_button_connect(buttons)

    def apply_button_connect(self, buttons):
        for button in buttons:
            name = button.get("name")
            q_btn = QPushButton(name)
            col_index, row_index = eval(button.get("range"))
            self.setCellWidget(row_index, col_index, q_btn)
            connect: str = button.get("connect")

            func = deal_connect_func(connect, self.root_window)

            if connect is not None and func is not None:
                try:
                    # noinspection all
                    q_btn.clicked.connect(func)
                except AttributeError as e:
                    traceback.print_exc()
                    logger.error(f"{self.__class__.__name__}没有指定的方法，请检查配合文件")
            self.buttons.update({name: q_btn})

    def read_data_in_range(self, start_row, end_row, start_col, end_col, with_column=True):
        """
        将表格指定区域的数据读入dataframe中

        :param start_row: 开始行的行号，以左上角为（1，1）单元格开始计算
        :param end_row: 结束行的行号，以左上角为（1，1）单元格开始计算
        :param with_column: 是否将第一行作为标题行
        """
        data = []
        for r in range(start_row - 1, end_row):
            row = []
            for c in range(start_col - 1, end_col):
                if self.item(r, c) is not None:
                    row.append(self.item(r, c).text())
                else:
                    row.append(None)
            data.append(row)

        data_frame = pd.DataFrame(data=data)

        data_frame.dropna(inplace=True)
        if with_column:
            data_frame.columns = data_frame.iloc[0]  # 将第一行作为标题行
            data_frame.drop([0], inplace=True)  # 删除第0行
        return data_frame

    def _set_row_column_count(self, x, y, width, height):
        """
        根据小区域的大小和位置设置表格宽高，保证表格可以容纳整个小区域

        :param x:
        :param y:
        :param height:
        :param width:
        :return:
        """
        # 设置表格长宽
        if width + x > self.columns:
            self.columns = width + x
            self.setColumnCount(self.columns)
        if height + y > self.rows:
            self.rows = height + y
            self.setRowCount(self.rows)

    @staticmethod
    def _get_align(item_dict, default="AlignCenter"):
        """
        从当前字典中获取align值，如果不存在，则生成default对应的align值，返回QtCore.Qt.AlginCenter等对象

        :param item_dict:
        :param default:
        :return:
        """
        align = item_dict.get("align") or "AlignCenter"
        if align.startswith("Qt"):
            align = eval(f"QtCore.{align}")
        elif align.startswith("QtCore"):
            align = eval(align)
        else:
            align = eval(f"QtCore.Qt.{align}")
        return align

    def get_var_location(self, var_name: str):
        """
        获取某个变量在表格中的位置
        :param var_name: 参数名称，如果表格时按照小区域分割的，则参数名称以 domain.label 的格式传入
        :return: tuple(x,y)
        """
        var_name = var_name.split(".")
        temp = self.var_loc
        for lvl in var_name:
            temp = temp.get(lvl)
            if isinstance(temp, tuple):
                return temp
        logger.warning(f"所查找的变量不存在{var_name}")
        return -1, -1

    def set_cell_value(self, row, col, value):
        if self.item(row, col) is None:
            self.setItem(row, col, QTableWidgetItem(str(value)))
        else:
            self.item(row, col).setText(str(value))

        self.viewport().update()  # 外部设置值时，Table中的视图数据不更新，其实内部数据已经改变，使用该语句刷新视图

    def set_value(self, var_name: str, value: str | float | int = ""):
        """
        设置表格中某个参数的值
        :param var_name: 参数名称，如果表格时按照小区域分割的，则参数名称以 domain.label 的格式传入
        :param value: 需要设置的值
        :return:
        """
        x, y = self.get_var_location(var_name)
        if x != -1:  # 说明存在制定字符串对应的变量
            if type(value) == bool:  # 布尔型变量设置checked状态
                # noinspection all
                self.cellWidget(x, y).setChecked(value)
            else:
                value = str(value)
                self.item(x, y).setText(value)  # 不能使用setItem()方法，否则会改变单元格样式
        else:
            logger.debug(f"{var_name}未找到")

    def get_value(self, var_name: str):
        """
        获取表格中某个参数的值
        :param var_name: 参数名称，如果表格时按照小区域分割的，则参数名称以 domain.label 的格式传入
        :return:
        """
        x, y = self.get_var_location(var_name)
        try:
            # 常规的文本类型直接返回text即可
            result: str | float = self.item(x, y).text()
        except AttributeError:  # 可能是QCheckBox类型，需要返回是否选中的bool值
            result: QCheckBox | QWidget = self.cellWidget(x, y)
            result = result.isChecked()

        try:
            result = float(result)
        except ValueError:
            pass
        return result

    def get_button(self, name):
        """
        根据按钮的文字获取按钮对象
        :param name:
        :return:
        """
        q_btn = self.buttons.get(name)
        return q_btn

    def display_dataframe(self, df: pd.DataFrame, row_index: int = 0, col_index: int = 0,
                          index: int | None = "", header: str | None = "", digits=None):
        """
        将pandas的DataFrame数据显示到YkDataTableWidget上，本方法不会清理YkDataTableWidget上的原来存在的数据

        :param df:
        :param df: dataframe数据
        :param row_index: 显示区域左上角的行索引
        :param col_index: 显示区域左上角的列索引
        :param index: 是否写入df的行标题，默认是写入的。如果是None，则不写入。
        :param header: 是否写入df的列标题，默认是写入原标题的。如果是None，则不写入。
        :param digits: 数据类型的最大小数点后显示位数
        :return:
        """
        if df is None:
            return
        if index is not None:
            df1 = df.reset_index()
        else:
            df1 = df
        if self.rowCount() < row_index + df1.shape[0] + 1:
            self.setRowCount(row_index + df1.shape[0] + 2)
        if self.columnCount() < col_index + df1.shape[1] + 1:
            self.setColumnCount(col_index + df1.shape[1] + 2)
        values = df1.values

        if header is not None:
            for j, col_name in enumerate(df1.columns):
                # setItem(row_index, col_index, QTableWidgetItem(label))
                self.setItem(row_index, col_index + j, QTableWidgetItem(str(col_name)))
            row_index = row_index + 1
        for i, row in enumerate(values):
            for j, cell in enumerate(row):
                cell = str(cell).strip()
                x = row_index + i
                y = col_index + j
                if is_number(cell) and digits is not None:
                    cell = str(round(float(cell), digits))
                self.setItem(x, y, QTableWidgetItem(cell))

    def mouseReleaseEvent(self, e: QtGui.QMouseEvent) -> None:
        """
        表格中的点击事件
        :param e:
        :return:
        """
        if e.button() == Qt.RightButton:
            logger.debug("右键点击了单元格")

    def pop_custom_menu(self, pos):
        """
        弹出自定义菜单

        :param pos: 鼠标点击的位置
        :return:
        """
        menu = QMenu()
        item1 = menu.addAction('粘贴')

        # 单击一个菜单项就返回，使之被阻塞
        action = menu.exec(self.mapToGlobal(pos))
        row = self.selectionModel().selection().indexes()[0].row()
        col = self.selectionModel().selection().indexes()[0].column()
        if action == item1:
            self.paste_data(row, col)

    def paste_data(self, row=0, col=0, rows=None, cols=None):
        """
        将剪切板中的数据粘贴到表格中

        :param row: 粘贴位置的行号
        :param col: 粘贴位置的列号
        :param rows: 粘贴的总行数
        :param cols: 粘贴的总列数
        :return:
        """
        from yangke.base import clipboard_to_dataframe
        try:
            content = clipboard_to_dataframe()
            self.display_dataframe(content, row, col, index=None, header=None)
        except:
            logger.error("粘贴剪切板数据至表格失败！")

    def cellPressedEvent(self, row: int, column: int) -> None:
        self.clearSelection()
        # self.setCurrentCell(row, column)
        self.setRangeSelected(QTableWidgetSelectionRange(row, column, row, column), True)

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        """ Ctrl + C复制表格内容 """
        if e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_C:
            # 获取表格的选中行
            selected_ranges = self.selectedRanges()[0]  # 只取第一个数据块,其他的如果需要要做遍历,简单功能就不写得那么复杂了
            text_str = ""  # 最后总的内容
            # 行（选中的行信息读取）
            for row in range(selected_ranges.topRow(), selected_ranges.bottomRow() + 1):
                row_str = ""
                # 列（选中的列信息读取）
                for col in range(selected_ranges.leftColumn(), selected_ranges.rightColumn() + 1):
                    item = self.item(row, col)
                    if item is not None:
                        row_str += item.text() + '\t'  # 制表符间隔数据
                    else:
                        row_str += '\t'
                text_str += row_str + '\n'  # 换行
            clipboard = QApplication.clipboard()  # 获取剪贴板
            clipboard.setText(text_str)  # 内容写入剪贴板

        elif e.modifiers() == Qt.ControlModifier and e.key() == Qt.Key_V:
            row = self.selectedRanges()[0].topRow()
            col = self.selectedRanges()[0].leftColumn()
            self.paste_data(row, col)
        else:
            if len(self.selectedRanges()) > 0:
                row = self.selectedRanges()[0].topRow()
                col = self.selectedRanges()[0].leftColumn()
                # self.setItem(row, col, QTableWidgetItem(cell))
        super().keyPressEvent(e)


class YkScrollArea(QScrollArea):
    def __init__(self):
        super(YkScrollArea, self).__init__()
        self.setWidgetResizable(True)
        self.setFixedWidth(350)

    def resize(self, a0: QtCore.QSize) -> None:
        super().resize(a0)
        logger.debug(self.geometry())

    def repaint(self) -> None:
        super(YkScrollArea, self).repaint()
        logger.debug(self.geometry())


class YkTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super(YkTabWidget, self).__init__(parent)
        self.labels = []  # 每一个标签页的名称，标签顺序和标签页顺序相同

    def get_tab_names(self):
        return self.labels  # 标签不允许重复

    def insertTab(self, index: int, widget: QWidget, a2: str) -> int:
        res = super(YkTabWidget, self).insertTab(index, widget, a2)
        self.labels.insert(index, a2)
        return res

    def addTab(self, widget: QWidget, a1: str) -> int:
        res = super(YkTabWidget, self).addTab(widget, a1)
        self.labels.append(a1)
        return res

    def removeTab(self, index: int) -> None:
        super(YkTabWidget, self).removeTab(index)
        self.labels.pop(index)

    def remove_tab(self, name: str):
        idx = self.indexOf(self.get_tab_panel(name))
        self.removeTab(idx)

    def activate_tab(self, tab_name):
        if tab_name in self.labels:
            idx = self.labels.index(tab_name)
            self.setCurrentIndex(idx)
            return self.currentWidget()

    def get_tab_panel(self, tab_name) -> 'YkInputPanel | YkDataTableWidget | QWidget | None':
        if tab_name in self.labels:
            idx = self.labels.index(tab_name)
            return self.widget(idx)
        else:
            logger.debug(f"YkTabWidget中不包含名为{tab_name}的标签页面板")
            return None


class YkInputPanel(QWidget):  # 高度自定，宽度随外部定
    def __init__(self, from_file="ui_data.yaml", domain=None,
                 values: list = None, fix_height=38, parent=None):
        """
        输入面板。可以为空面板
        本面板会根据需要自动包含拖动条。
        可以使用self.apply_btn_connect()方法链接面板中的按钮至所有父组件中的方法。



    输入框面板

    # 输入界面类型一般如下：
    --------------------------------------
    |  <label1>  <textField1> <unit1>    |
    |  <label2>  <textField2> <unit2>    |
    |  <label3>  <textField3> <unit3>    |
    |                                    |
    |          <btn_apply>   <btn_ok>    |
    --------------------------------------

    实例ui_data.yaml文件
    ----------------------------------------------------------------
    size:
      width:
        - 160  # <label>的宽度
        - 140  # <textField>的宽度
        - 80  # <unit>的宽度
    algorithm:
      inputArea:
        - # 第一个设置项
          label: "种群大小"
          value: 50
        - # 第二个设置项
          label: "遗传代数"
          value: 200
      buttons:
        - # 第一个按钮
          text: "应用"
          on_click: "btn_clicked"  # 按钮点击触发的事件
        - text: "确定"
          on_click: "btn_clicked"  # 按钮点击触发的事件
    ----------------------------------------------------------------

    :param values: 输入框的显示值，如果不设置，则为默认的初始值，设置的话必须一一对应每一个值，不能省略，也可以是qt_designer生成的ui文件
    :param domain: ui定义文件中的选项，一个ui文件中中可以定义多个输入面板，该值表示选用哪个
    :param from_file: ui定义文件
    :return:

        """
        super(YkInputPanel, self).__init__(parent)
        self.fix_height = fix_height
        self.size1 = {"width": [100, 50, 50]}
        self.name = None  # 面板的名称可能是from_file的文件名，也可能是from_file中的domain名，具体取哪个根据不同情况而有差异
        if from_file is not None and from_file.endswith(".ui"):
            widget = uic.loadUi(from_file)
            self.setLayout(QGridLayout())
            self.layout().setContentsMargins(0, 0, 0, 0)
            # noinspection all
            self.layout().addWidget(widget, 0, 0, 1, 1)
            self.name = os.path.basename(from_file).split(".")[0]
            self.yk_items = []
            self.connect_info = {}
        else:
            if domain is None:  # 则将domain设置为第一个有inputArea的组件面板
                settings = get_settings(setting_file=from_file)
                for k, v in settings.items():
                    if v.get("inputArea") is not None:
                        domain = k
                        break
            self.yk_items = []

            if domain is None:
                logger.debug("空面板")
                self.settings = {}
            else:
                self.settings = get_settings(domain, setting_file=from_file)
                input_area = self.settings.get('inputArea')
                self.size1 = get_settings("size", setting_file=from_file)  # self.size()是QWidget的内置方法
                for i, item in enumerate(input_area):
                    if values is not None:
                        item["value"] = values[i]  # 用调用方法传入的默认值替换ui文件中的默认值

                    _label = item.get("label")
                    _value = item.get("value")
                    _unit = item.get("unit")
                    _indent = item.get("indent") or 0
                    _size = item.get("size") or self.size1

                    if isinstance(_value, list):
                        _value = {"value": _value}
                    if isinstance(_unit, list):
                        _unit = {"value": _unit}

                    if item.get("value_text_changed"):
                        _value.update({"text_changed": item.get("value_text_changed")})
                    if item.get("unit_text_changed"):
                        _unit.update({"text_changed": item.get("unit_text_changed")})

                    if item.get("unit_selected"):
                        _unit.update({"selected_val": item.get("unit_selected")})
                    if item.get("value_selected"):
                        _value.update({"selected_val": item.get("value_selected")})

                    self.yk_items.append(YkItem(size=_size, label=_label, value=_value, unit=_unit, indent=_indent))

            self.name = domain
            self.values = []
            self.units = []
            self.connect_info = {}  # 需要链接的点击事件信息
            self.box: QVBoxLayout | None = None
            self.buttons = []
            self.update_ui()

    def get_items_count(self):
        """
        返回当前输入面板中YkItem的数量
        """
        return len(self.yk_items)

    def get_button(self, button_text) -> QPushButton | None:
        """
        获取指定的按钮
        """
        for button in self.buttons:
            if button.text() == button_text:
                return button
        return None

    def update_ui(self):
        btn_box = QHBoxLayout()
        btn_box.addStretch()
        self.connect_info = {}
        self.buttons = []
        item_box = QVBoxLayout()  # 各个设置项组成的面板
        item_box.setContentsMargins(9, 9, 9, 9)
        for btn in self.settings.get('buttons') or []:
            btn1 = QPushButton(btn.get('text'))
            connected: str = btn.get('on_click') or btn.get("connect")
            self.connect_info.update({btn1: connected})
            btn_box.addWidget(btn1)
            self.buttons.append(btn1)
        v_box = QVBoxLayout()
        for item in self.yk_items:
            item_box.addWidget(item)
        scroll = QScrollArea()
        widget = QWidget()
        widget.setLayout(item_box)

        size_policy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(1)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(widget.sizePolicy().hasHeightForWidth())
        widget.setSizePolicy(size_policy)

        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)  # 如果设置可以resize，则内部组件尺寸会按照layout排列。

        v_box.addWidget(scroll)
        v_box.addItem(btn_box)
        self.setLayout(v_box)
        self.box = item_box

    def apply_btn_connect(self):
        """
        延迟连接的按钮事件，因为窗口初始化时，按钮等组件还没有添加到面板中，因此按钮的父组件为空，无法将按钮与按钮的父组件或爷组件等的事件关联起来
        ，因此延迟连接这类按钮时间，该方法在主窗口初始化完成后，有主窗口调用。
        :return:
        """
        for it in self.yk_items:
            it.apply_btn_connect()
        for k1, v1 in self.connect_info.items():
            k1: QWidget = k1
            connect_event_by_dict(k1, v1)

    def insert_item(self, index, items):
        """
        在面板中插入新的YkItem组件

        :param index:
        :param items: YkItem 组件或组件列表
        :return:
        """
        if isinstance(items, YkItem):
            if items.size1 is None or len(items.size1) == 0:
                items.set_size(self.size1)
            self.yk_items.insert(index, items)
            self.box.insertWidget(index, items)
            items.apply_btn_connect()
            # height = self.box.parentWidget().size().height()
            # self.box.parentWidget().setFixedHeight(height + self.fix_height)
        else:
            for item in items:
                if item.size1 is None or len(item.size1) == 0:
                    item.set_size(self.size1)
                self.yk_items.insert(index, item)
                self.box.insertWidget(index, item)  # 倒数第二个是stretch，倒数第一个是btn_box
                item.apply_btn_connect()
                # height = self.box.parentWidget().size().height()
                # self.box.parentWidget().setFixedHeight(height + self.fix_height)

    def append_item(self, items):
        """
        在面板末尾添加YkItem组件
        :param items:
        :return:
        """
        if isinstance(items, YkItem):
            if items.size1 is None or len(items.size1) == 0:
                items.set_size(self.size1)
            self.yk_items.append(items)
            self.box.addWidget(items)
            items.apply_btn_connect()
            # height = self.box.parentWidget().size().height()
            # self.box.parentWidget().setFixedHeight(height + self.fix_height)
        else:
            for item in items:
                if item.size1 is None or len(item.size1) == 0:
                    item.set_size(self.size1)
                # self.yk_items.extend(items)
                count = self.box.count()
                self.box.insertWidget(count, item)  # 在倒数第三个的位置插入新组件，即【..., stretch, btn_box】的stretch之前
                item.apply_btn_connect()
                # height = self.box.parentWidget().size().height()
                # self.box.parentWidget().setFixedHeight(height + self.fix_height)
            self.yk_items.extend(items)

    def remove_item(self, name=None, index=None):
        """
        从当前
        :param name: 需要移除的YkItem中label的名
        :param index: 需要移除的YkItem的索引
        :return:
        """
        if index is None:
            for idx, item in enumerate(self.yk_items):
                if item.label.text() == name:
                    self.box.removeWidget(item)
                    self.yk_items.pop(idx)
                    # height = self.box.parentWidget().size().height()
                    # self.box.parentWidget().setFixedHeight(height - self.fix_height)
                    return
        else:
            if isinstance(index, int):
                self.box.removeWidget(self.yk_items[index])
                self.yk_items.pop(index)
            elif isinstance(index, list):
                index.sort(reverse=True)  # 只能先删除索引大的项，在删除索引小的项，因为删除前面项时，后面的项的索引会改变
                for i in index:
                    self.remove_item(index=i)

    def get_item(self, label_text):
        """
        根据标签的文字，获取对应的YkItem对象

        :param label_text:
        :return:
        """
        for item in self.yk_items:
            if isinstance(item.label, QLabel):
                if item.label.text() == label_text:
                    return item

    def get_values_and_units(self, need_unit=True, need_dict=False, need_label=False):
        """
        获取YkInputPanel对象的数值和单位

        :param need_unit: 是否需要单位，不需要则只返回数值
        :param need_dict: 是否需要返回dict类型的数据，默认返回列表类型数据，需要注意的是，如果返回字典类型，则同标签名的数据会覆盖
        :param need_label: 是否需要返回标签名列表
        :return:
        """
        if not need_dict:
            self.labels = []
            self.values = []
            self.units = []
            for it in self.yk_items:
                self.labels.append(it.label.text())
                self.values.append(it.get_value())
                self.units.append(it.get_unit())
            if need_unit and not need_label:
                return self.values, self.units
            if need_label and not need_unit:
                return self.labels, self.values
            elif need_label and need_unit:
                return self.labels, self.values, self.units
            else:
                return self.values
        else:
            value_dict = {}
            unit_dict = {}
            for it in self.yk_items:
                value_dict.update({it.label.text(): it.get_value()})
                if need_unit:
                    unit_dict.update({it.label.text(): it.get_unit()})
            if need_unit:
                return {"value": value_dict, "unit": unit_dict}
            else:
                return value_dict

    def set_values(self, values=None, units=None):
        """
        设置输入面板中各项的值（按顺序），也可以设置单位

        :param values: 值的列表，或｛label:value｝的字典
        :param units: 单位
        :return:
        """
        if values is None:
            return
        if isinstance(values, dict):
            for it in self.yk_items:
                label = it.label.text()
                if label in values.keys():
                    try:
                        it.set_value(values[it.label.text()])
                    except:
                        traceback.print_exc()
        elif isinstance(values, list):
            for i, it in enumerate(self.yk_items):
                it: YkItem
                unit = units[i] if units is not None else None
                try:
                    it.set_value(values[i])
                    it.set_unit(unit)
                except:
                    pass

    def set_value(self, label, value, unit=None):
        if value is None:
            return
        for it in self.yk_items:
            if isinstance(it.label, QLabel):
                if it.label.text() == label:
                    try:
                        it.set_value(value)
                        if unit is not None:
                            it.set_unit(unit)
                        return
                    except:
                        traceback.print_exc()


class YkFoldableWidget(QWidget):
    def __init__(self, title: str, content: QWidget):
        super(YkFoldableWidget, self).__init__()
        self.title = title
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(1)
        label = QLabel(title)
        self.layout().addWidget(label)
        self.widget = content
        self.layout().addWidget(self.widget)
        self.widget.setVisible(True)


class YkTabButton(QPushButton):
    # 按钮作为开关
    def __init__(self, item, name, parent=None):
        super(YkTabButton, self).__init__(parent)
        self.item = item
        self.setCheckable(True)  # 设置可选中
        self.setText(name)

    def resizeEvent(self, event):
        # 解决item的高度问题
        super(YkTabButton, self).resizeEvent(event)
        self.item.setSizeHint(QtCore.QSize(self.minimumWidth(), self.height()))


class YkEditor(QsciScintilla):
    def __init__(self, language: str | None = 'python'):
        """
        编辑器窗口
        """
        if not hasattr(QsciScintilla, "setLexer"):
            logger.debug(f"QsciScintilla未安装！pip install QScintilla/PyQt6-QScintilla安装")
            exit(0)
        super(YkEditor, self).__init__()
        self.__lexer = self.lexer()
        if language is None:
            self.__lexer = None
        elif language == "python":
            self.__lexer = QsciLexerPython()
        self.setLexer(self.__lexer)
        self.setUtf8(True)  # Set encoding to UTF-8
        self.__myFont = QFont("Consolas", 14)
        self.setFont(self.__myFont)  # Will be overridden by lexer!
        self.setWrapMode(QsciScintilla.WrapCharacter)
        self.setWrapVisualFlags(QsciScintilla.WrapFlagByText)
        # self.setIndentationsUseTabs(False)  # 使用'\t'还是' '进行缩进
        self.setIndentationWidth(4)
        self.setIndentationGuides(True)
        self.setTabIndents(True)  # 是否对齐缩进
        self.setAutoIndent(True)  # 下一行是否自动缩进
        self.setCaretForegroundColor(QColor(255, 0, 0))
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#1fff0000"))
        self.setAutoCompletionSource(QsciScintilla.AcsAll)  # 自动补全代码的参考源，包括API和文档
        self.setAutoCompletionThreshold(1)  # 输入一个字符时即触发自动补全
        self.setAutoCompletionCaseSensitivity(False)  # 自动补全触发条件忽略大小写
        self.setAutoCompletionReplaceWord(True)  # 自动补全时直接替换当前单词
        self.setAutoCompletionUseSingle(QsciScintilla.AcusExplicit)
        if self.__lexer is not None:
            self.__api = QsciAPIs(self.__lexer)
            self.__api.prepare()

        self.setMarginType(1, QsciScintilla.NumberMargin)
        self.setMarginWidth(1, "000")
        self.setMarginsForegroundColor(Qt.black)

    def add_auto_completions(self, strings):
        """
        在self.__api.prepare()之后在加入的词是无效的，需要重新生成QsciAPIs
        """
        for ac in strings:
            self.__api.add(ac)

    def append(self, msg):
        super().append(msg)
        if self.lines() > 9999:
            self.setMarginWidth(1, "00000")
        elif self.lines() > 999:
            self.setMarginWidth(1, "0000")

    def write(self, msg: str):
        """
        该方法是面板作为logger的sink时必须实现的方法，logger.debug(msg)等方法会调用该方法将日志写到面板上
        """
        self.append(msg)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())  # 滚动到最后
        QApplication.processEvents()  # 每次输出，就更新Qt图形界面，使得某些长耗时子进程不方便调用图形界面时，可以调用日志方法


class YkConsole(YkEditor):
    def __init__(self):
        """
        控制台只能在最后一行输入命令，前面不可编辑
        """
        super(YkConsole, self).__init__()
        self.cursorPositionChanged.connect(self.onCursorPositionChanged)

    def onCursorPositionChanged(self):
        """
        只能在最后一行输入命令，前面不可编辑
        """
        line, index = self.getCursorPosition()
        if self.lines() > line + 1:  # 当前行号小于总行数
            self.setReadOnly(True)  # 如果在之前行上输入任何字符，忽略并将光标移动到最后
        else:
            self.setReadOnly(False)

    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        line, index = self.getCursorPosition()
        if self.lines() > line + 1:  # 当前行号小于总行数
            # 如果在之前行上输入任何字符，忽略并将光标移动到最后
            self.setCursorPosition(self.lines() - 1, self.lineLength(self.lines() - 1))
        else:  # 如果是最后一行点击Enter键，则执行最后一行的命令
            if e.key() == Qt.Key_Enter or e.key() == Qt.Key_Return:
                cmd = self.get_last_line_text()
                self.last_cmd = cmd
                if cmd == "clear":
                    self.setText("")
                elif cmd == "exit()":
                    sys.exit(0)
                elif cmd.strip() == '':
                    pass
                else:
                    res = self.deal_cmd(cmd)  # 执行命令返回结果
                    self.append("\n")
                    self.append(str(res or ''))
                    self.setCursorPosition(self.lines() - 1, self.lineLength(self.lines() - 1))

        if e.key() == Qt.Key_Up:  # 向上翻页时，不移动光标
            self.append(self.last_cmd)
        else:
            super(YkConsole, self).keyPressEvent(e)

    def get_last_line_text(self):
        """
        获取最后一个非空行的内容
        """
        text = self.text()
        lines = text.split("\n")
        return lines[-1]

    def deal_cmd(self, cmd):
        return "succeed: " + cmd


class YkStandardItemModel(QStandardItemModel):
    def __init__(self, item_list: list):
        """
        列表试图等使用的QStandardModel类对象，构造方法：
        model = [str1, str2, ... , str100]
        model = [{"name": str1, "自定义参数1": 自定义参数1, "自定义参数n": 自定义参数n}
        """
        if isinstance(item_list, list):
            super().__init__()
            for obj in item_list:
                if isinstance(obj, str):
                    item = QStandardItem(obj)
                elif isinstance(obj, dict):
                    item = QStandardItem(obj.get("name"))
                    item.setData(obj, role=Qt.UserRole)  # 给item添加自定义数据
                else:
                    return
                self.appendRow(item)

    def update_item(self, item_list: list):
        self.clear()
        for obj in item_list:
            if isinstance(obj, str):
                item = QStandardItem(obj)
            elif isinstance(obj, dict):
                item = QStandardItem(obj.get("name"))
                item.setData(obj, role=Qt.UserRole)  # 给item添加自定义数据
            else:
                return
            self.appendRow(item)


class YkListViewWidget(QListView):
    def __init__(self, model=None, parent=None):
        """
        初始化一个ListViewWidget，可以传入需要显示的列表，列表中的对象可以是字符串，也可以是字典，如果是字符串，则ListView的
        每一个视图项为该字符串。如果是字典，则字典中必须包含key="name"的项，例如：
        obj_list = [{"name": "北京"}, {"name": "上海"}, {"name": "西安"}]
        """
        super().__init__(parent=parent)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 屏蔽双击编辑操作，很多时候listview并不需要编辑
        self.setModel(model)

    def setModel(self, model: QtCore.QAbstractItemModel) -> None:
        if isinstance(model, QtCore.QAbstractItemModel):
            super().setModel(model)
        else:
            if isinstance(model, list):
                list_model = QStandardItemModel()
                for obj in model:
                    if isinstance(obj, str):
                        item = QStandardItem(obj)
                    elif isinstance(obj, dict):
                        item = QStandardItem(obj.get("name"))
                        item.setData(obj, role=Qt.UserRole)  # 给item添加自定义数据
                    else:
                        return
                    list_model.appendRow(item)
                self.setModel(list_model)

    def update_model(self, model):
        ...

    def add_item_clicked_listener(self, func):
        """
        添加鼠标点击事件，func方法会接收到点击项的索引QModelIndex对象
        """
        # noinspection all
        self.clicked.connect(func)

    def add_item_pressed_listener(self, func):
        """
        添加按下鼠标事件，func方法会接收到点击项的索引QModelIndex对象
        """
        # noinspection all
        self.pressed.connect(func)


class YkVariableWidget(QTreeView):
    def __init__(self, parent=None):
        """
        用于显示程序内变量数据信息的面板，仿Pycharm、Python Console右侧的变量面板或调试时的变量面板
        """
        super(YkVariableWidget, self).__init__(parent)
        self.value: dict | None = None
        self.model: QStandardItemModel = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["变量", "类型", "值"])
        self.setModel(self.model)
        self.setColumnWidth(0, 300)
        self.setColumnWidth(1, 150)
        # self.model.dataChanged.connect(self.on_data_changed)
        # self.clicked.connect(self.onclick)  # clicked事件只有点击在QTreeView的item上时才会触发，点击展开图标时无法触发
        self.base_type = ['int', 'float', 'float32', 'int', 'bool', 'NoneType']
        self.qt_inner_type = ["GraphicsItemFlag", "GraphicsItemChange", "CacheMode", "builtin_function_or_method"]

    def update_variable(self, variable_scope=None):
        if variable_scope is None:
            variable_scope = {}
        self.value = variable_scope
        self.model.removeRows(0, self.model.rowCount())
        self.dict_to_QStandardModel()  # 根据变量命名空间生成QStandardModel

    def dict_to_QStandardModel(self):
        """
        将任意对象转换为QStandardItemModel对象
        """
        value = self.value
        r = 0
        for k, v in value.items():
            if k.startswith("__builtins__"):
                continue
            self.model.appendRow(QStandardItem(str(k)))  # 字典中每一个键都是一个变量，占一行
            self.model.setItem(r, 1, QStandardItem(type(v).__name__))  # 第一列为变量的类型
            self.model.setItem(r, 2, QStandardItem(str(v)))  # 第二列为变量的值
            self.model.item(r, 0).setData(v)  # 将值赋给第一列的QStandardItem，以便当点击第一列时，展开该值的详细信息
            if not type(v).__name__ in self.base_type:  # 如果变量是复杂类型，则添加折叠按钮
                self.object_to_QStandardItem(v, self.model.item(r, 0))  # 如果变量是复杂类型还需要继续处理，如果不是复杂类型，该函数不做操作
            r += 1

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            index = self.indexAt(event.pos())
            if index.isValid():
                data = index.data()
                standard_item: QStandardItem = index.model().itemFromIndex(index)
                v = standard_item.data()
                self.object_to_QStandardItem(v, standard_item, expand=True)  # 设置展开
        super(YkVariableWidget, self).mousePressEvent(event)

    def onclick(self, index):
        logger.debug('...')

    def on_data_changed(self, left, bottom, roles):
        logger.debug('...')

    def object_to_QStandardItem(self, value, parent_item, expand=False):
        """
        将任意对象转换为QStandardItem对象时，如果任意对象是类或字典等具有进一步详细可展开属性时，该方法自动将子属性添加到父对象之下，使得可以进一步
        查看更详细的信息，如果没有子属性，该方法不做任何操作。

        :param value: 父对象的值
        :param parent_item: 父对象的QStandardItem
        :param expand: 是否展开当前模型
        :return:
        """
        if isinstance(value, int) or isinstance(value, str) or isinstance(value, float) or isinstance(value, bool):
            return
        else:
            if expand:
                parent_item.removeRows(0, parent_item.rowCount())
                if isinstance(value, list):
                    for _r, v in enumerate(value):
                        if str(v).strip() == '':
                            continue
                        parent_item.appendRow(QStandardItem(str(_r)))  # 列表中的每一个元素的索引是tableView中的第一列，使用appendRow添加
                        parent_item.setChild(_r, 1, QStandardItem(type(v).__name__))
                        parent_item.setChild(_r, 2, QStandardItem(str(v)))
                        if not type(v).__name__ in self.base_type:  # 如果变量是复杂类型，则添加折叠按钮
                            self.object_to_QStandardItem(v, parent_item.child(_r, 0))
                elif isinstance(value, dict):
                    _r = 0
                    for k, v in value.items():
                        _this_item = QStandardItem(str(k))
                        _this_item.setData(v)
                        parent_item.appendRow(_this_item)
                        parent_item.setChild(_r, 1, QStandardItem(type(v).__name__))
                        parent_item.setChild(_r, 2, QStandardItem(str(v)))
                        if not type(v).__name__ in self.base_type:  # 如果变量是复杂类型，则添加折叠按钮
                            self.object_to_QStandardItem(v, parent_item.child(_r, 0))
                        _r += 1  # 必须位于最后一行
                else:
                    attrs = dir(value)
                    attrs = [i for i in attrs if not i.startswith("_")]
                    # attrs_super = dir(value.__class__.__bases__[0])
                    # super1 = value.__class__.__bases__[0]()
                    _r = 0
                    for _r2, k2 in enumerate(attrs):  # 为了调试方便，改变一下迭代变量名称
                        try:
                            v2 = getattr(value, k2)
                        except:
                            continue
                        if type(v2).__name__ in self.qt_inner_type:
                            continue
                        if parent_item is None:
                            return
                        _this_item = QStandardItem(str(k2))
                        _this_item.setData(v2)
                        parent_item.appendRow(_this_item)
                        parent_item.setChild(_r, 1, QStandardItem(type(v2).__name__))
                        parent_item.setChild(_r, 2, QStandardItem(str(v2)))
                        if not type(v2).__name__ in self.base_type:  # 如果变量是复杂类型，则添加折叠按钮
                            self.object_to_QStandardItem(v2, parent_item.child(_r, 0))
                        _r += 1
            else:
                parent_item.appendRow(QStandardItem("加载中..."))


def distance(obj1, obj2):
    """
    计算两个对象的距离

    :param obj1:
    :param obj2:
    :return:
    """
    type1 = type2 = None
    # 不能使用type(obj1).__class__.__name__的方法判断，因为PyQt5、PyQt6、PySide6的实现会导致class name为wrapper类型
    if isinstance(obj1, QPoint) or isinstance(obj1, QPointF):
        type1 = "point"
    elif isinstance(obj1, QLine) or isinstance(obj1, QLineF):
        type1 = "line"
    if isinstance(obj2, QPoint) or isinstance(obj2, QPointF):
        type2 = "point"
    elif isinstance(obj2, QLine) or isinstance(obj2, QLineF):
        type2 = "line"

    if type1 == "point" and type2 == "point":
        x1, y1 = obj1.x(), obj1.y()
        x2, y2 = obj2.x(), obj2.y()
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    elif type1 == "point" and type2 == "line":
        logger.debug("暂不支持点和线的距离计算")
    elif type2 == "line" and type1 == "point":
        logger.debug("暂不支持点和线的距离计算")
    else:
        logger.debug("暂不支持线和线的距离计算")


if __name__ == "__main__":
    ...
