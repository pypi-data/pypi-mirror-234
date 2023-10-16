import os.path
import re
import traceback
from typing import Iterable

from yangke.common.QtImporter import QModelIndex, QMimeData, QComboBox, QApplication, QLineEdit, QDrag

from yangke.common.QtImporter import QDir, Qt, QRectF, QSize, QStringListModel, QStandardItemModel, QStandardItem, \
    QIcon, QColor, QBrush, QResizeEvent, QKeyEvent, QFileSystemModel, QListView, QWidget, QGridLayout, QVBoxLayout, \
    QListWidget, QListWidgetItem, QLabel, QLayout, uic, QMainWindow, QColorDialog

from UI.MainWindow_PyQt5 import Ui_MainWindow
from UI.content import Ui_Form as ContentForm
from yangke.base import yield_all_file
from yangke.common.config import logger
from yangke.common.qt import UIWidget, run_app, YkWindow, YkItem, YkFoldableWidget, YkInputPanel, YkEditor, YkConsole, \
    YkVariableWidget
from yangke.ebsilon.constant.constant import default_unit, Unit
from yangke.ebsilon.graphicsview import YkGraphicsScene, YkGraphicsView, YkGraphicsItem, CoordinateItem, SceneGridItem, \
    YkStyledItemDelegate, DisplayPanel, PipeItem, SceneFlagItem, Port
import importlib

from yangke.ebsilon.values import Values


class Content(QWidget):
    def __init__(self, tab_name):
        super(Content, self).__init__()
        self.ui: QWidget = UIWidget(ContentForm)  # 即qt designer设计的ui文件面板
        self.tab_name = tab_name
        self.setLayout(QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        # noinspection all
        self.layout().addWidget(self.ui, 0, 0, 1, 1)
        self.scene = YkGraphicsScene()
        self.view = YkGraphicsView(self.scene)  # self.view.setScene(self.scene)
        self.view.setAcceptDrops(True)
        # self.view.setDragMode(ScrollHandDrag)
        self.view.setAlignment(Qt.AlignCenter)
        self.ui.layout().addWidget(self.view)


class CalResult:
    def __init__(self):
        ...


class MainWindow(YkWindow, QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.choose_component = 0
        self.setWindowTitle("热力性能建模平台")
        self.ui.btn_set_value.clicked.connect(self.set_values_panel2data)
        self.ui.btn_cancel.clicked.connect(self.cancel)
        # # self.ui下有 self.ui.info_tab用于显示组件的详细信息
        self.ui.sfv.setLayout(QVBoxLayout())  # sfv的竖直方向的SizePolicy必须是Fixed
        self.ui.res.setLayout(QVBoxLayout())
        self.ui.mat.setLayout(QVBoxLayout())

        # [<PyQt5.QtGui.QStandardItem object at 0x0227C49C11B0>, <PyQt5.QtGui.QStandardItem object at 0x0227C49C1480>]
        self.items_nav = []  # 组件的QStandardItem实例，是导航面板上的显示对象，长度与self.all_comps相同

        # 组件类对象, {'Comp1': <class 'components.Comp1.Item'>, 'Comp2': <class 'components.Comp2.Item'>}
        self.all_comps = self.load_all_comp(os.path.join(os.path.dirname(__file__), "components"))
        self.init_file_view()
        self.init_compo_view()
        self.content_widget = self.init_content_tab()

        # 设置场景导航面板的数据模型位self.lv_scene_model
        self.lv_scene_model = QStandardItemModel()
        self.update_scene_nav_view(None)

        self.ui.splitter_3.setStretchFactor(0, 2)
        self.ui.splitter_3.setStretchFactor(1, 4)
        self.current_comp_info_tab = "SpecificationValues"  # 表示self.ui.info_tab显示按个数据面板
        self.ui.content_tab.tabCloseRequested.connect(self.close_project)  # 使单个项目可以关闭

        if self.proj.get("DefaultUnit") is not None:  # 项目默认的单位系统不为空，则加载项目默认单位系统
            pass
        elif self.ini_info.get("DefaultUnit") is not None:  # 如果项目单位系统为空，但软件单位系统不为空，则加载软件单位系统
            self.proj["DefaultUnit"] = self.ini_info.get("DefaultUnit")
        else:  # 如果以上二者都为空，则初始化一个默认的单位系统，并保存到项目中
            self.proj["DefaultUnit"] = None
        if self.proj["DefaultUnit"] is not None:
            default_unit.set(self.proj["DefaultUnit"])

        if self.proj_file is not None and os.path.exists(self.proj_file):  # 如果有项目文件，且该文件存在
            try:
                self.open(self.proj_file)
                self.close_project(0)
            except:
                logger.warning(f"打开{self.proj_file}时出错")

        self.exec_scope = {"self": self}  # 终端代码执行时的变量作用域
        self.tv_var = YkVariableWidget()  # 固定面板-> Terminal -> 变量空间
        self.ui.verticalLayout_12.addWidget(self.tv_var)
        self.init_fixed_window()

        self.ui.info_tab.currentChanged.connect(self.info_tab_changed)
        self.status_bar_coor = QLabel('')
        self.status_bar_coor.setFixedWidth(60)
        self.statusBar1.addPermanentWidget(self.status_bar_coor)
        self.calc_result = CalResult()  # 计算结果信息，如计算是否成功，计算失败原因等

    def keyPressEvent(self, a0: QKeyEvent) -> None:
        if a0.key() == Qt.Key_F9:
            self.calculate()
        elif a0.modifiers().value == (Qt.ShiftModifier | Qt.ControlModifier).value and a0.key() == Qt.Key_AsciiTilde:
            if self.ui.dockWidget_ATW.isHidden():
                self.ui.dockWidget_ATW.show()
            else:
                self.ui.dockWidget_ATW.hide()
        else:
            super(MainWindow, self).keyPressEvent(a0)

    def close_project(self, sender=None):
        if isinstance(sender, int):
            self.ui.content_tab.removeTab(sender)
            self.content_widget = self.ui.content_tab.currentWidget()
        else:
            logger.warning("非法索引！")

    def init_content_tab(self):
        if self.ui.content_tab.count() == 0:
            return self.add_content_tab1("新建项目1")
        else:
            self.content_widget = self.ui.content_tab.widget(0).ui
            self.content_widget.scene.item_changed_signal.connect(self.update_scene_nav_view)
            return self.content_widget

    def add_content_tab1(self, tab_name):
        """
        不能使用父类的add_content_tab方法。
        """
        self._content_tab = self.ui.content_tab
        if tab_name in self.get_content_tab_labels():
            self._content_tab.setCurrentIndex(self.get_content_tab_labels().index(tab_name))
            logger.debug(f"已经存在名为{tab_name}的项目")
            self.content_widget = self._content_tab.currentWidget()
        else:
            content = Content(tab_name)
            self.ui.content_tab.addTab(content, tab_name)
            self.content_widget = content
            self.content_widget.scene.setBackgroundBrush(QBrush(QColor(208, 208, 208)))
            self.content_widget.scene.item_changed_signal.connect(self.update_scene_nav_view)
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
        self.items_nav = []
        for k, comp_cls in self.all_comps.items():
            comp: YkGraphicsItem = comp_cls()
            if comp.icon is None:
                comp.generate_icon()

            item = QStandardItem(comp.icon, comp.NAME)
            item.setData({"ebs_id": comp.EBS_ID, "ebs_name": comp.EBS_NAME, "ebs_type": comp.EBS_TYPE},
                         Qt.UserRole)  # 给item添加自定义数据
            self.items_nav.append(item)
            item.setDragEnabled(True)  # 是列表中的项可以被拖动
            list_model.appendRow(item)

        # list_model.mimeData()  # 实现list_model的mimeData()使之可以
        def _mimeData(indexes: list[QModelIndex]):
            if len(indexes) <= 0:
                return 0
            data = QMimeData()
            data.setData("com_data", str(indexes[0].data(Qt.UserRole)).encode("utf8"))
            return data

        list_model.mimeData = _mimeData

        self.ui.lv_com.setItemDelegate(YkStyledItemDelegate())
        self.ui.lv_com.setSpacing(4)

        self.ui.lv_com.setModel(list_model)
        self.ui.lv_com.setViewMode(QListView.ListMode)
        self.ui.lv_com.setDragEnabled(True)

        self.ui.lv_com.clicked.connect(self.click_com_cls)

    def init_file_view(self):
        """
        文件目录面板
        :return:
        """
        model = QFileSystemModel()
        model.setRootPath(QDir.currentPath())
        self.ui.tv_file.setModel(model)

    def update_scene_nav_view(self, idx: str | None = None):
        """
        场景导航面板

        :param idx: 新增设备的场景id，每次新增设备组件时，会触发本方法执行
        :return:
        """
        if idx is None:  # 初始化场景面板组件时，传入的id位scene
            self.ui.lv_scene.setSpacing(4)
            self.ui.lv_scene.setModel(self.lv_scene_model)
            self.ui.lv_scene.setViewMode(QListView.IconMode)
            self.ui.lv_scene.setDragEnabled(True)
            self.ui.lv_scene.clicked.connect(self.click_com_obj)

        elif idx.startswith("del"):
            name = idx.replace("del", "").strip()
            Qt.FindChildrenRecursively = 1
            # item = self.lv_scene_model.findChild(name=name, options=Qt.FindChildrenRecursively)
            row = self.lv_scene_model.findItems(name)[0].row()
            self.lv_scene_model.removeRow(row)
            self.ui.lv_scene.clearFocus()
            self.ui.lv_scene.clearSelection()
        else:
            scene_id = int(idx)
            设备组件: YkGraphicsItem = self.content_widget.scene.items_scene_id.get(scene_id)
            icon = 设备组件.icon if hasattr(设备组件, "icon") else None
            icon = icon or 设备组件.generate_icon()
            name = 设备组件.NAME if hasattr(设备组件, "NAME") else None
            ebs_id = 设备组件.EBS_ID if hasattr(设备组件, "EBS_ID") else None
            ebs_name = 设备组件.EBS_NAME if hasattr(设备组件, "EBS_NAME") else None
            ebs_type = 设备组件.EBS_TYPE if hasattr(设备组件, "EBS_TYPE") else None

            item = QStandardItem(icon, f"{name}_{设备组件.id} / S{scene_id}")
            item.setData({
                "ebs_id": ebs_id, "ebs_name": ebs_name, "ebs_type": ebs_type, "scene_id": scene_id
            }, role=Qt.UserRole)  # 给item添加自定义数据
            self.lv_scene_model.appendRow(item)
        # self.ui.lv_com.setItemDelegate(YkStyledItemDelegate())

    def init_fixed_window(self):
        self.ui.Terminal.setLayout(QVBoxLayout())
        self.ui.Terminal.layout().setContentsMargins(0, 0, 0, 0)
        self.ui.terminal = YkConsole()
        self.ui.Terminal.layout().addWidget(self.ui.terminal)
        self.ui.Log.setLayout(QVBoxLayout())
        self.ui.Log.layout().setContentsMargins(0, 0, 0, 0)
        self.ui.log_editor = YkEditor()
        self.ui.Log.layout().addWidget(self.ui.log_editor)
        self.ui.terminal.deal_cmd = self.deal_cmd
        self.ui.dockWidget_ATW.hide()
        self.update_terminal_var()
        logger.add(self.ui.log_editor)  # 将日志面板加入日志类的sink中

    def update_terminal_var(self):
        """
        更新变量面板上的变量值
        """
        tv = self.tv_var  # 变量的QTreeView实例对象
        try:
            self.exec_scope.update({"items_scene_id": self.content_widget.scene.items_scene_id})
            tv.update_variable(self.exec_scope)
        except:
            self.output_log(traceback.format_exc())

    def deal_cmd(self, cmd):
        """
        处理控制台输入的命令

        :param cmd: 控制台最后一行的文本内容，也就是命令
        :return:
        """
        try:
            if cmd == "refresh" or cmd == "update":  # 更新一下当前数据
                self.update_terminal_var()
                return
            res = eval(cmd, self.exec_scope)  # eval只能执行表达式，不能是语句，如eval("x=1")会报错
            self.exec_scope.update({"_": res})
        except:
            try:
                res = exec(cmd, self.exec_scope)  # exec可以执行语句，但是执行表达式时不返回结果，如exec("2+1")返回None
            except:
                res = traceback.format_exc()
        self.update_terminal_var()
        return res

    def click_com_cls(self, item):
        """
        组件导航面板的点击响应事件

        :return:
        """
        user_info = item.data(Qt.UserRole)
        self.choose_component = user_info.get("ebs_id")

    def insert_components(self, com_name):
        """
        在当前激活的项目中插入组件，一般为text组件
        """
        if com_name == 'text':
            self.choose_component = 'text'

    def click_com_obj(self, item):
        """
        场景导航面板的点击响应事件

        :param item:
        :return:
        """
        user_info = item.data(Qt.UserRole)
        if user_info is None:
            return
        scene_id = user_info.get("scene_id")
        item: YkGraphicsItem = self.content_widget.scene.items_scene_id.get(scene_id)
        item.setFocus(Qt.MouseFocusReason)
        self.display_info(scene_id)

    def draw_content_view(self):
        if self.content_widget is None:
            return
        self.content_widget.scene.setBackgroundBrush(QBrush(QColor(0, 100, 0, 50)))

    def resizeEvent(self, a0: QResizeEvent) -> None:
        super(MainWindow, self).resizeEvent(a0)
        # try:
        #     rect = self.content_widget.rect()
        #     self.content_widget.scene.setSceneRect(QRectF(rect.x(), rect.y(), rect.width() - 24, rect.height() - 24))
        # except:
        #     pass

    def save(self):
        """
        保存项目
        :return:
        """
        self.proj = self.proj or {}
        items = self.content_widget.scene.items_scene_id
        # 将items中无法序列化的Item对象转换为字符串
        items_new = []
        try:
            for scene_id, obj in items.items():
                if scene_id <= 2 or isinstance(obj, CoordinateItem) or isinstance(obj, SceneGridItem):
                    continue  # scene_id=0和1是网格和坐标系组件
                obj: YkGraphicsItem = obj
                bak_info = {}
                if obj.EBS_ID == '-100':
                    obj: PipeItem = obj
                    bak_info.update({
                        "control_points": obj.control_points, "color": obj.color, "connect_items": obj.connect_items,
                    })
                objs_pickable = {"EBS_ID": obj.EBS_ID, "EBS_NAME": obj.EBS_NAME, "id": obj.id, "scene_id": obj.scene_id,
                                 "values": obj.values, "rotation": obj.rotation(),
                                 "scene_pos": obj.scenePos(), "height": obj.height, "width": obj.width,
                                 "ports": obj.ports, "bak_info": bak_info, "z_value": obj.zValue(),
                                 }
                items_new.append(objs_pickable)
        except:
            traceback.print_exc()

        self.proj.update({'items': items_new})
        super(MainWindow, self).save()

        self.statusBar1.showMessage(f"项目保存完成")
        logger.info(f"项目保存至{self.proj_file}")

    def get_projects(self):
        """
        获取当前已经打开的项目名称
        """
        res = [self.ui.content_tab.tabText(i) for i in range(self.ui.content_tab.count())]
        return res

    def new_project(self):
        super().new_project()
        _proj_name = "new"
        _proj_names = self.get_projects()
        if _proj_name in _proj_names:
            i = 1
            while f"new_{i}" in _proj_names:
                i = i + 1
            _proj_name = f"new_{i}"
        _ = self.add_content_tab1(_proj_name)
        self.ui.content_tab.setCurrentWidget(_)
        self._content_tab = self.ui.content_tab

    def open(self, proj=None):
        super(MainWindow, self).open(proj)
        # 添加一个新的content_tab，并切换到新添加的content_tab
        if self.proj_file is None:  # 当新建项目时，打开空项目但proj_file尚未指定
            return
        proj_name = os.path.basename(self.proj_file).split(".")[0]
        self.add_content_tab1(tab_name=proj_name)
        self.ui.content_tab.setCurrentWidget(self.content_widget)
        if self.proj is None:
            return
        # 取出项目中的组件，并逐个绘制到场景中
        proj_items = self.proj.get("items")
        if proj_items is None:
            return
        try:
            for obj in proj_items:
                EBS_ID = obj.get("EBS_ID")
                if EBS_ID == '-100':
                    comp: PipeItem = PipeItem(fluid_type=obj["EBS_NAME"])
                    comp.set_color(obj["bak_info"]["color"])
                    comp.setPos(obj.get("scene_pos"))
                    control_points = obj["bak_info"]["control_points"]
                    comp.update_line(vectors_item=control_points)
                    comp.set_connect_items(obj["bak_info"]["connect_items"])
                    comp.EBS_NAME = obj["EBS_NAME"]
                else:
                    comp: YkGraphicsItem = self.all_comps.get(f"Comp{obj.get('EBS_ID')}")()
                    comp.setPos(obj.get("scene_pos"))
                    comp.values = obj.get("values")
                    comp.ports = obj.get("ports")

                z_value = obj.get("z_value") or 1  # 图层高度
                comp.setZValue(z_value)
                comp.setRotation(obj.get("rotation"))  # 图像的旋转角度
                self.content_widget.scene.addItem(comp, scene_id=obj.get("scene_id"), id=obj.get('id'))  # 添加combobox项时
            logger.debug(f"项目加载完成")
        except:
            traceback.print_exc()

        self.update_scene_nav_view()

    def refresh(self):
        ...

    def get_calc_items(self, sort_by='计算顺序'):
        """
        获取当前激活的项目下需要参与计算的设备组件字典
        """
        components = []
        for scene_id, com in self.content_widget.scene.items_scene_id.items():
            if com.__class__.__name__ in ["SceneGridItem", "SceneFlagItem", "CoordinateItem"]:
                ...
            else:
                components.append(com)
        if sort_by == "计算顺序":
            components.sort(key=lambda x: x.cal_order)
        return components

    def clear_results(self, components=None):
        """
        清空当前激活的项目中的计算结果数据
        """
        components = components or self.get_calc_items()
        for com in components:
            com: YkGraphicsItem = com
            for idx, port in com.ports.items():
                port: Port = port
                port.values = Values(values_steps={0: {}})  # port的初始值为空
            com.values.clear_result()  # 清空端口上初始值以后的迭代步的值
            com.calculated = False  # 重置计算状态为False

    def calculate_real_time(self):
        ...

    def calculate(self):
        """
        计算项目，计算开始时，应确保每个组件的values中的values_steps数组中已经放置了初始的参数设置，即使没有初始参数需要设置，也需要以
        空Values对象占位。

        计算过程中，需要保证时间步0只保存画面上传入的数据，中间计算结果永远不要保存到时间步0。
        计算开始时，所有的Port对象中均没有数据，Port上的数据是在事件步1由边界条件设置组件传递到Port对象上的

        :return:
        """
        cal_type, _info = self.get_calculate_info()
        if cal_type == "real_time":  # 实时计算，每隔指定时间计算一次
            time_interval = float(_info[0])
            from yangke.base import execute_function_by_interval
            execute_function_by_interval(self.calculate_real_time, minute=0, second=time_interval)
        else:
            components = self.get_calc_items()  # 所有参与计算的设备组件字典
            epochs = 100  # 计算迭代总次数
            exit_msg = "计算失败！"
            error_info = {}

            # 正式计算之前，清空所有组件的port中存储的之前的计算结果以及result中保存的计算结果
            self.clear_results(components)

            # 首先计算边界值组件，并将边界值组件的值传递给相应的端口，边界值组件必须可以独立计算，否则会直接退出计算过程
            # 边界值组件上设置的参数也是初始参数，需要传递给port的value_steps第0步
            for com in components:
                if hasattr(com, "EBS_ID") and com.EBS_ID in [1, 46]:
                    msg: str = com.calculate(step=0)
                    if msg != "done":
                        logger.debug(f"{com.scene_id}号组件未设置必要参数！--- {msg}")
                        epochs = 1  # 让整体计算不在进行，直接退出
                        break
                    com.spread_values(step=0)  # 将当前组件设置的边界或起始值扩散到与其端口上

                    com.calculate(step=1)
                    com.spread_values(step=1)  # 将当前组件设置的边界或起始值扩散到与其端口上

            for i in range(1, epochs):
                total_num = len(components)
                calculated = {}
                exit_epochs = False
                self.content_widget.scene.current_step = i  # 设置当前计算步
                for com in components:  # 不加dict，调试经常出现无法解析整形的错误
                    if com.EBS_ID in [1, 46]:  # 边界及初始条件设置组件已经计算完成
                        # 目前来讲，1和46号组件无须重复计算，但是考虑到初始值或参考值或控制值等组件，每个迭代步可能都要计算
                        # 且如果这里不计算，则边界值组件的values.value_steps只有前两步的值
                        com.calculate(step=i)
                        com.spread_values(step=i)  # 将当前组件设置的边界或起始值扩散到与其端口上
                        com.calculated = True
                        calculated.update({com.scene_id: True})
                        continue

                    # if com.calculated:  # 计算过的参数仍需计算，不影响过定义，因为过定义只在第1个时间步判断第0个时间步的值
                    #     calculated.update({scene_id: True})
                    #     continue

                    # 首先将当前面板上的数据读入设备组件的values中
                    com.before_com_calculate(step=i)
                    msg: str = com.calculate(step=i)
                    if msg is None:
                        logger.debug(f"组件{com.scene_id}的calculate方法未返回计算结果信息，请检查组件代码！")
                        return

                    msgs = msg.split("---")
                    _err = None
                    if len(msgs) == 2:
                        msg, _err = msgs[0].strip(), msgs[1].strip()
                    if msg == "done":
                        com.calculated = True
                        calculated.update({com.scene_id: True})
                    elif _err is not None and _err.strip() == "break":  # 引发计算立即退出的错误
                        error_info.update({com.scene_id: msgs})
                        logger.debug(error_info)  # 输出错误原因
                        exit_epochs = True
                        exit_msg = "计算失败！"
                        break
                    else:
                        com.calculated = False
                        if error_info.get(com.scene_id) == msg:  # 当前错误信息与上一次相同，则退出计算
                            logger.debug(error_info)
                            exit_epochs = True
                            exit_msg = "计算失败！"
                            break
                        error_info.update({com.scene_id: msg})  # 更新当前组件的错误信息
                        if len(calculated) >= total_num - 1:  # 其他都已经计算完成，只剩一个未计算，则说明缺少参数，直接退出并报错
                            logger.debug(msg)
                            exit_epochs = True
                            exit_msg = "计算失败！"
                            break
                    com.spread_values(step=i)  # 将当前组件计算出的结果扩散到与其连接的其他组件

                if len(calculated) == total_num:
                    # 如果所有组件都计算完成，则退出计算循环
                    exit_epochs = True
                    exit_msg = "计算成功"
                if exit_epochs:
                    break

            # 获取当前组件信息面板是属于哪个组件的，更新显示结果
            _ = self.ui.detail_tab.tabText(0).split("/ S")
            if len(_) > 1:
                scene_id_current = int(_[1].replace(']', '').strip()) if len(_) > 1 else None
                self.display_info(scene_id=scene_id_current, tab=self.current_comp_info_tab)

            logger.debug(exit_msg)
            self.ui.ActiveToolWindow.setCurrentWidget(self.ui.Log)  # 将FixedToolWindow切换到日志面板
            self.show_active_tool_window()

    def show_active_tool_window(self):
        if self.ui.dockWidget_ATW.isHidden():
            self.ui.dockWidget_ATW.show()

    def display_info(self, scene_id, tab=None, save_data=True):
        """
        当选中组件时，该方法用于显示组件的详细信息

        @param: scene_id : 组件在场景中的id
        @param tab: 需要显示的信息面板标签页
        """
        if save_data:
            self.set_values_panel2data()  # 先保存当前面板的值，后切换到新面板

        if scene_id is None or scene_id < 2:  # 0号组件是场景网格对象，1号组件是场景坐标系对象
            return True
        item = self.content_widget.scene.items_scene_id.get(scene_id)

        if item is None:
            return

        if tab is None:
            self.ui.detail_tab.setTabText(0, f"组件信息[{item.NAME}_{item.id} / S{item.scene_id}]")
            tab = self.ui.info_tab.tabText(self.ui.info_tab.currentIndex())

        self.show_info_tab(tab, item)

        # 更新场景组件导航面板上的组件列表
        # self.update_scene_nav_view()  # 貌似不用更新场景信息面板，否则会导致场景信息面板重加载

        idx = list(self.content_widget.scene.items_scene_id.keys()).index(scene_id) - 3  # 因为场景中有三个组件不显示
        qm_idx = self.ui.lv_scene.model().index(idx, 0)
        self.ui.lv_scene.setCurrentIndex(qm_idx)

    def show_info_tab(self, tab_name: str, device_item: YkGraphicsItem | None = None):
        """
        根据tab_items的值，构建组件信息面板，并将values中的值显示到信息面板上

        :param tab_name: 信息面板的标签页名
        :param device_item: 当面板上的combobox需要链接事件时，需要传入面板所属的设备组件Item对象，以便从Item中加载相应的事件响应方法
        :return:
        """
        if tab_name == "SpecificationValues" or tab_name == "规格值":
            tab_items = device_item.SpecificationValues or {}
            panel_info_tab, connect_slot = self._form_display_panel(tab_items, device_item)
            if len(self.ui.sfv.children()) == 1 and isinstance(self.ui.sfv.children()[0], QLayout):
                self.ui.sfv.layout().addWidget(panel_info_tab)
            else:
                self.ui.sfv.layout().removeWidget(self.ui.sfv.children()[1])
                if len(self.ui.sfv.children()) > 1:
                    # 必须强制删除一次原组件，才能彻底删除干净，replaceWidget方法也存在删除不干净的问题
                    self.ui.sfv.children()[1].deleteLater()
                self.ui.sfv.layout().addWidget(panel_info_tab)

            values = device_item.values
            _values = values.get_initial(need_unit=True)
            panel_info_tab.set_values(_values)  # 此时，combobox连接事件尚未添加，因此设置值不会触发相应事件

            # 数值设置完成后，再添加combox链接事件
            # 如果在值设置之前连接事件，则会导致多个组件切换时，动态响应参数与响应时间源不匹配的问题
            self._add_combo_box_connect(panel_info_tab, connect_slot, device_item)

            return panel_info_tab
        elif tab_name == "Results" or tab_name == "结果":
            tab_items = device_item.Result or {}
            panel_info_tab, connect_slot = self._form_display_panel(tab_items, device_item)

            if len(self.ui.res.children()) == 1 and isinstance(self.ui.res.children()[0], QLayout):
                self.ui.res.layout().addWidget(panel_info_tab)
            else:
                self.ui.res.layout().removeWidget(self.ui.res.children()[1])
                if len(self.ui.res.children()) > 1:
                    # 必须强制删除一次原组件，才能彻底删除干净，replaceWidget方法也存在删除不干净的问题
                    self.ui.res.children()[1].deleteLater()
                self.ui.res.layout().addWidget(panel_info_tab)

            values = device_item.values
            _values = values.get_results(need_unit=True)
            panel_info_tab.set_values(_values)
        elif tab_name == "材料" or tab_name == "Materials":
            pass

    def _add_combo_box_connect(self, panel_info_tab, connect_slot, device_item):
        # 处理信息面板中combobox值改变时的事件响应
        if len(connect_slot) > 0:
            _ = []
            for connect in connect_slot:
                exist = False
                # 首先合并connect_slot中var和connect相同的信号与槽
                for c in _:
                    if c["var"] == connect["var"] and c["connect"] == connect["connect"]:
                        if isinstance(c["object"], list):
                            c["object"].append(connect["object"])
                            c["object_type"].append(connect["object_type"])
                        else:
                            c["object"] = [c["object"], connect["object"]]
                            c["object_type"] = [c["object_type"], connect["object_type"]]
                        exist = True
                        break
                if not exist:
                    _.append(connect)

            for connect in _:
                connect_func = eval(f"device_item.{connect.get('connect')}")
                var = connect.get("var")
                var_item = panel_info_tab.get_child_yk_items(var)
                value_combobox = var_item.value
                if isinstance(value_combobox, QComboBox):
                    # 多个connect_func方法相同时，则连接的函数传入的参数会相同，这会导致相当于信号触发最后一次绑定的事件多次，而不是各种参数
                    # 各调用一次，需要进行处理
                    value_combobox.currentTextChanged.connect(
                        lambda: self.combox_text_changed(connect_func, connect, panel_info_tab))

    def _form_display_panel(self, tab_items, device_item):
        """
        生成详细信息面板

        :param tab_items: 面板需要显示的数据，一般为item.SpecificationValues或item.Result数据对象
        :return:
        """
        panel_sfv = DisplayPanel()
        connect_slot = []  # 信息面板中各项之间可能有combobox等事件联动，记录下来
        for 参数类别, 参数项 in tab_items.items():
            disabled = False
            panel_参数类别 = QWidget()
            panel_参数类别.setLayout(QVBoxLayout())
            panel_参数类别.layout().setContentsMargins(0, 0, 0, 0)
            panel_参数类别.layout().setSpacing(1)
            for 子参数项 in 参数项:
                size = [100, 80, 60]
                name = 子参数项[0]
                symbol = 子参数项[1]
                value = 子参数项[2]
                if len(子参数项) >= 4:
                    unit = 子参数项[3]
                else:
                    unit = None
                if isinstance(unit, dict):
                    func = unit.get("func")
                    _res = re.findall(r"(.+)[(](.*)[)]", func)[0]
                    func_name, var = _res
                    # symbol的unit需要根据func_name(var)的执行结果确定
                    _slot = {"var": var, "connect": func_name, "object": symbol, "object_type": "unit"}
                    connect_slot.append(_slot)
                    try:
                        unit = eval(f"device_item.{func_name}('{var}')")
                        unit = {"value": unit.allowed_values, "selected_val": unit.unit}
                    except:
                        unit = ["初始化时发生错误！"]
                else:
                    pass
                if len(子参数项) >= 5:
                    var4 = 子参数项[4]
                    if isinstance(var4, str):
                        disabled = True if var4 == "disabled" else False
                    elif isinstance(var4, dict):
                        if var4.get("size") is not None:
                            size = var4.get("size")
                item = YkItem(f"{name}[{symbol}]", value, unit, size=size, draggable=True)
                # if isinstance(item.value, QLineEdit):
                #     item.value.setDragEnabled(True)
                if disabled:
                    item.value.setEnabled(False)
                panel_参数类别.layout().addWidget(item)
            panel_fold = YkFoldableWidget(参数类别, panel_参数类别)
            panel_sfv.layout().addWidget(panel_fold)

        return panel_sfv, connect_slot

    def combox_text_changed(self, func, connect_info, panel_sfv):
        """
        组件信息面板上，combobox组件值改变时，触发的事件处理

        :param func:
        :param connect_info:
        :return:
        """
        # noinspection all
        var, func = connect_info.get("var"), func  # 这两个参数在eval语句中使用
        self.set_values_panel2data()  # 先将当前改变后的值写入self.values中，再调用dynamic_unit方法
        res: Unit = eval(f"func(var)")
        object_yk_items = connect_info.get("object")
        object_types = connect_info.get("object_type")
        if not isinstance(object_yk_items, list):
            object_yk_items = [object_yk_items]
            object_types = [object_types]

        for object_item, object_type in zip(object_yk_items, object_types):
            des = panel_sfv.get_child_yk_items(object_item)  # 设置的目标YkItem对象
            if object_type == "unit":
                des.unit.setModel(QStringListModel(res.allowed_values))
                des.set_unit(res.unit)

    def set_values_panel2data(self):
        """
        将面板上的数值赋值给组件的values对象，点击【确定】按钮时会执行该方法
        """
        # 获取到当前正在设置的组件，根据场景id
        _ = self.ui.detail_tab.tabText(0).split("/ S")
        if len(_) == 1:
            return
        scene_id = int(_[1].replace(']', '').strip())
        item = self.content_widget.scene.items_scene_id.get(scene_id)
        if item is None:  # 说明当前的组件已经被删除，因为显示下一个信息面板时会首先保存上一个信息，所以该方法可能在组件已删除的情况下被调用
            return
        # 获取当前设置的面板名
        tab_name = self.ui.info_tab.tabText(self.ui.info_tab.currentIndex())
        if tab_name == "规格值" or tab_name == "SpecificationValues":
            _layout = self.ui.sfv.layout()  # self.ui.sfv.layout()没有子项
            if len(self.ui.sfv.children()) > 1 and isinstance(self.ui.sfv.children()[1], DisplayPanel):
                panel: DisplayPanel = self.ui.sfv.children()[1]  # 当前sfv上显示的面板
                values: dict = panel.get_values()  # 获取面板上的所有值，包括空值
                item.values.set_values(0, values, set_none=True)  # 将面板上的值赋值给设备组件，包括空值，面板上获取的值都是初始状态的值
                item.after_values_updated()  # 值设置完成后进行的操作
        elif tab_name == "结果":
            pass  # 结果不保存至当前设备组件，结果数据只能是计算出来的

    def set_values_data2panel(self):
        """
        将组件中的参数数值显示到面板上
        """
        # 获取到当前正在设置的组件，根据场景id
        scene_id = int(self.ui.detail_tab.tabText(0).split("/ S")[1].replace(']', '').strip())
        item = self.content_widget.scene.items_scene_id.get(scene_id)

        # 获取当前设置的面板名
        tab_name = self.ui.info_tab.tabText(self.ui.info_tab.currentIndex())
        if tab_name == "规格值" or tab_name == "SpecificationValues":
            panel: DisplayPanel = item.SpecificationValuesPanel
            children = self.ui.sfv.children()
            self.ui.sfv.layout().replaceWidget(children[1], panel)
            values = panel.set_values(item.values)

    def cancel(self):
        ...

    def info_tab_changed(self, idx):
        """


        :param idx:
        :return:
        """
        # 获取到当前正在设置的组件，根据场景id
        _ = self.ui.detail_tab.tabText(0).split("/ S")
        if len(_) == 1:
            return
        scene_id = int(_[1].replace(']', '').strip())
        # 获取到当前的信息面板名，如 "规格值"、"结果"
        tab_name = self.ui.info_tab.tabText(idx)
        self.display_info(scene_id=scene_id, tab=tab_name, save_data=False)  # 切换面板触发的显示信息不保存数据

    def get_color(self):
        color = QColorDialog.getColor(Qt.white)
        if color.isValid():
            self.content_widget.scene.setBackgroundBrush(QBrush(color))

    def clear_log_console(self):
        log_editor: YkEditor = self.ui.log_editor
        log_editor.setText("")

    def get_calculate_info(self):
        """
        获取计算设置信息
        """
        settings = self.proj.get('settings')
        if settings is None:
            return None, (None,)
        else:
            cal_type = settings.get('cal_type')
            cal_time_interval = settings.get('cal_time_interval')
        return cal_type, (cal_time_interval,)

    def set_calculate(self):
        """
        计算设置，点击后默认10s计算一次
        {"settings":
            {
                "cal_type": "real_time",
                "cal_time_interval": 10
            }
        }
        """
        settings = self.proj.get('settings')
        if settings is None:
            self.proj.update({"settings": {"cal_type": "real_time", "cal_time_interval": 10}})
        else:
            if settings.get("cal_type") == "real_time":
                self.proj.update({"settings": {"cal_type": "normal"}})
            else:
                self.proj.update({"settings": {"cal_type": "real_time", "cal_time_interval": 10}})


if __name__ == "__main__":
    run_app(MainWindow)
