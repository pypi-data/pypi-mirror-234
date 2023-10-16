import os.path

from PyQt5.QtCore import QDir, Qt, QRectF, QSize, QStringListModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon, QColor, QBrush, QResizeEvent, QKeyEvent
from PyQt5.QtWidgets import QFileSystemModel, QListView, QWidget, QGridLayout

from UI.TPRI_CNNP import Ui_Form
from UI.content import Ui_Form as ContentForm
from yangke.base import yield_all_file
from yangke.common.config import logger
from yangke.common.qt import UIWidget, run_app, YkWindow
from yangke.ebsilon.graphicsview import YkGraphicsScene, YkGraphicsView, YkGraphicsItem, CoordinateItem, SceneGridItem, \
    YkStyledItemDelegate
import importlib


class Content(QWidget):
    def __init__(self, tab_name):
        super(Content, self).__init__()
        self.ui: QWidget = UIWidget(ContentForm)  # 即qt designer设计的ui文件面板
        self.tab_name = tab_name
        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.ui, 0, 0, 1, 1)
        self.scene = YkGraphicsScene()
        self.view = YkGraphicsView(self.scene)  # self.view.setScene(self.scene)
        self.view.setAcceptDrops(True)
        # self.view.setDragMode(ScrollHandDrag)
        self.view.setAlignment(Qt.AlignCenter)
        self.ui.layout().addWidget(self.view)


class MainWindow(YkWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.choose_component = 0
        self.setCentralWidget(UIWidget(Ui_Form))
        self.setWindowTitle("热力性能建模平台")
        self.ui: Ui_Form = self.centralWidget().ui  # TPRI_CNNP.Ui_Form

        # [<PyQt5.QtGui.QStandardItem object at 0x0227C49C11B0>, <PyQt5.QtGui.QStandardItem object at 0x0227C49C1480>]
        self.items = []  # 组件的QStandardItem实例

        # 组件类对象, {'Comp1': <class 'components.Comp1.Item'>, 'Comp2': <class 'components.Comp2.Item'>}
        self.all_comps = self.load_all_comp(os.path.join(os.path.dirname(__file__), "components"))
        self.init_file_view()
        self.init_compo_view()
        self.content_widget = self.init_content_tab()
        self.draw_content_view()
        self.init_scene_nav_view()
        self.init_compo_info()
        self.content_widget.scene.item_changed_signal.connect(self.init_scene_nav_view)

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key_F9:
            self.calculate()
        super(MainWindow, self).keyPressEvent(a0)

    def init_content_tab(self):
        if self.ui.content_tab.count() == 0:
            return self.add_content_tab("新建项目1")
        else:
            return self.ui.content_tab.widget(0).ui

    def add_content_tab(self, tab_name):
        content = Content(tab_name)
        self.ui.content_tab.addTab(content, tab_name)
        self.content_widget = content
        return self.content_widget

    def load_all_comp(self, path):
        """
        从yangke.ebsilon.components文件夹中加载所有的组件

        :param path:
        :return:
        """
        if hasattr(self, "all_comps") and self.all_comps is not None:
            return self.all_comps
        all_comps = {}
        for file in yield_all_file(path, ".py"):
            basename = os.path.basename(file).replace(".py", "")
            _ = importlib.import_module(f"components.{basename}")
            all_comps.update({basename: _.Item})
        return all_comps

    def init_compo_view(self):
        """
        组件导航面板，加载及显示所有组件

        :return:
        """
        list_model = QStandardItemModel()
        self.items = []
        for k, comp_cls in self.all_comps.items():
            comp: YkGraphicsItem = comp_cls()
            item = QStandardItem(QIcon(comp.icon_file), comp.NAME)
            item.setData({"ebs_id": comp.EBS_ID, "ebs_name": comp.EBS_NAME, "ebs_type": comp.EBS_TYPE},
                         Qt.UserRole)  # 给item添加自定义数据
            self.items.append(item)
            list_model.appendRow(item)
        self.ui.lv_com.setItemDelegate(YkStyledItemDelegate())
        self.ui.lv_com.setSpacing(4)

        self.ui.lv_com.setModel(list_model)
        self.ui.lv_com.setViewMode(QListView.ListMode)
        self.ui.lv_com.setDragEnabled(True)

        self.ui.lv_com.clicked.connect(self.click_com)

    def init_compo_info(self):
        """
        组件信息面板，显示组件详细信息

        :return:
        """
        logger.debug(f"{self.all_comps}")

    def init_file_view(self):
        """
        文件目录面板
        :return:
        """
        model = QFileSystemModel()
        model.setRootPath(QDir.currentPath())
        self.ui.tv_file.setModel(model)

    def init_scene_nav_view(self):
        """
        场景导航面板

        :return:
        """
        list_model = QStringListModel()
        scene_items = self.content_widget.scene.items  # {'边界值': [<components.Comp1.Item object at 0x0000024CB50C4D30>]}
        list_ = []
        for k, v in scene_items.items():
            for i in v:
                str_name = f"{i.NAME}_{i.id}"
                list_.append(str_name)
        list_model.setStringList(list_)
        self.ui.lv_scene.setModel(list_model)
        for item in self.content_widget.scene.items:
            ...

    def click_com(self, item):
        """
        组件导航面板的点击响应事件

        :return:
        """
        # name = item.data()
        user_info = item.data(Qt.UserRole)
        self.choose_component = user_info.get("ebs_id")

    def draw_content_view(self):
        if self.content_widget is None:
            return
        self.content_widget.scene.setBackgroundBrush(QBrush(QColor(0, 100, 0, 50)))

    def resizeEvent(self, a0: QResizeEvent) -> None:
        super(MainWindow, self).resizeEvent(a0)
        try:
            rect = self.content_widget.rect()
            self.content_widget.scene.setSceneRect(QRectF(rect.x(), rect.y(), rect.width() - 24, rect.height() - 24))
        except:
            pass

    def calculate(self):
        """
        计算项目

        :return:
        """
        ...


run_app(MainWindow)
