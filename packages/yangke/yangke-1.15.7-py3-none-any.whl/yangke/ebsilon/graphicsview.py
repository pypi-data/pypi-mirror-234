import copy
import math
import os.path
import re
import traceback
import typing

from yangke.common.QtImporter import QPixmap, QGraphicsSceneDragDropEvent, QGraphicsTextItem

from yangke.common.config import logger
from yangke.common.qt import YkWindow, YkFoldableWidget, YkItem, distance
from yangke.ebsilon.constant.constant import 管线图层id, Pressure, Temperature, Enthalpy, MassFlow, Power, Unit, 背景图层id
from yangke.base import Line

# 同时支持PyQt5、PyQt6和PySide6，建议使用PyQt6
from yangke.common.QtImporter import QtGui, QDir, QStringListModel, Qt, QModelIndex, QRectF, QPointF, QRect, QSize, \
    QLineF, QPoint, pyqtSignal, QStandardItemModel, QStandardItem, QIcon, QPainter, QPainterPath, QPen, QColor, QFont, \
    QImage, QBrush, QTransform, QFileSystemModel, QTreeView, QMessageBox, QStyledItemDelegate, QStyleOptionViewItem, \
    QListView, QStyle, QWidget, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsItem, QGridLayout, \
    QVBoxLayout, QGraphicsSceneMouseEvent, QStyleOptionGraphicsItem, QGraphicsSceneHoverEvent, \
    QGraphicsSceneContextMenuEvent, QMenu, QAction, QApplication, QGraphicsLineItem, QLabel, QFrame
from yangke.ebsilon.values import Values, Value
from yangke.performance.iapws97 import get_h_by_pt, get_t_by_hp, get_p_by_th, validate_water_parameters

吸附距离 = 10


class ConnectItem:
    def __init__(self, item_sid, des_port_id=None, point_id=None, des_point_id=None):
        """
        只有管线有连接项属性，设备组件没有连接项属性，设备组件的连接信息记录在组件的ports对象中
        管线上的连接项，用于记录与管线连接的设备组件以及端口的信息。
        如果管线上的连接点连接的是另一条管线，则该连接项没有port_id，对应的应该是另一条管线的点的索引

        :param des_port_id: 连接项连接的目标端口id
        :param point_id: 连接项在当前组件中的点的id，PipeItem类型的点id
        :param des_point_id:
        """
        # [{"item": YkGraphicsItem().scene_id, "port_id": 1, "point_id": 0}]
        if des_point_id is not None:
            self.des_type = "pipe"
        else:
            self.des_type = "device"
        self.item_sid = item_sid
        self.port_id = des_port_id
        self.point_id = point_id
        self.des_point_id = des_point_id

    def equal_item(self, connect_item: "ConnectItem"):
        """
        判断两个连接项是否相同，如果管线上某个点连接的组件及组件上的端口id都相同，说明是同一个连接项
        """
        if self.item_sid == connect_item.item_sid and self.port_id == connect_item.port_id:
            return True
        else:
            return False

    def __str__(self):
        if self.port_id is not None:
            return f"当前管线的第{self.point_id}个点连接至{self.item_sid}号组件第{self.port_id}个端口"
        else:
            return f"当前管线的第{self.point_id}个点连接至{self.item_sid}号组件第{self.des_point_id}个点"

    def get_port_type(self, scene: 'YkGraphicsScene'):
        """
        获取连接点所连接端口的类型
        """
        item = scene.items_scene_id.get(self.item_sid)
        if self.port_id is not None:
            port: Port = item.ports[self.port_id]
            type1 = port.type1
        else:
            type1 = None
        return type1


class ConnectItems(list):
    def __init__(self):
        """
        管线上所有的连接项数组
        """
        super().__init__()

    def has_this_item(self, connect_item: ConnectItem):
        """
        判断当前连接项数组中，是否包含给定的连接项，如果包含，则返回指定连接项在连接项数组中的索引，如果不包含，则返回的索引为-1
        """
        if connect_item is None:
            return None
        item_idx = -1
        for idx, _ci in enumerate(self):
            _ci: ConnectItem
            if _ci.equal_item(connect_item):
                # 如果连接项的场景id和端口号相同，则是同一个连接点，记录下连接项在连接项数组中的索引
                item_idx = idx
                break
        return item_idx

    def append(self, connect_item: ConnectItem) -> None:
        """
        添加连接项，如果已存在相同连接项，则更新连接项的连接点
        """
        if connect_item is None:
            return
        idx = self.has_this_item(connect_item)
        if idx == -1:  # 说明不存在指定项，则直接添加
            super().append(connect_item)
        else:
            self[idx].point_id = connect_item.point_id


class AdsorbInfo:
    def __init__(self, scene, des_sid=None, des_port=None, des_point=None, des_lid=None, des_pid=None, src_port=None,
                 src_sid=None, src_point=None, src_pid=None):
        """
        用于记录鼠标拖动事件中，组件端口的吸附状态的信息，包括吸附对象，对象中的点，对象中的线，拖动组件对象等

        :param des_sid: 吸附目标组件的场景id
        :param des_port: 如果吸附到的是某个组件的端口，则记录该端口id
        :param des_point: QPointF, 如果是吸附到管线上的点，则记录点的坐标
        :param des_lid: int, 如果是吸附到管线上的点，则记录吸附到的线段在管线中的索引
        :param des_pid: 如果是吸附到管线上的控制点，则记录控制点的索引
        :param src_port: 当前发生吸附的端口在当前图元中的索引
        :param src_sid: 当前发生吸附的图元场景id
        """
        self.scene = scene
        self.des_sid = des_sid
        self.des_point: QPointF | None = des_point
        self.des_port = des_port
        self.des_pid = des_pid
        self.des_lid = des_lid
        self.src_port = src_port
        self.src_sid = src_sid
        self.src_point = src_point
        self.src_pid = src_pid

    def clear_adsorb_item(self):
        self.des_sid = None

    def update_info(self, des_sid=None, des_port=None, des_point=None, des_lid=None, des_pid=None, src_port=None,
                    src_sid=None, src_point=None, src_pid=None):
        """
        :param des_sid: 吸附目标组件的场景id
        :param des_port: 如果吸附到的是某个组件的端口，则记录该端口id，如管线吸附到组件端口
        :param des_point: QPointF, 如果是吸附到管线上的点，则记录点的坐标
        :param des_lid: int, 如果是吸附到管线上的点，则记录吸附到的线段在管线中的索引，如信号线吸附到管线
        :param des_pid: 如果是吸附到管线上的控制点，则记录控制点的索引
        :param src_port: 当前发生吸附的端口在当前图元中的索引，如组件端口吸附到管线
        :param src_sid: 当前发生吸附的图元场景id
        :param src_point: 如果是绘制管线时发生吸附，则记录吸附源点的位置，如信号线吸附到管线/管线吸附到组件端口
        :param src_pid: 如果是绘制管线时发生吸附，则记录吸附源点在管线中的索引，如信号线吸附到管线
        """
        self.des_sid = des_sid
        self.des_point: QPointF | None = des_point
        self.des_port = des_port
        self.des_pid = des_pid
        self.des_lid = des_lid
        self.src_port = src_port
        self.src_sid = src_sid
        self.src_point = src_point
        self.src_pid = src_pid

    def adsorbed(self):
        """
        是否发生吸附
        """
        if self.des_sid is None:
            return False
        else:
            return True

    def get_adsorbed_item(self, des=True):
        if des:
            return self.scene.items_scene_id.get(self.des_sid)
        else:
            return self.scene.items_scene_id.get(self.src_sid)

    def get_adsorbed_port(self, des=True) -> 'Port':
        """
        获取吸附发生的端口

        :param des: 如果为True，则返回吸附目标的端口，如果为False，则返回吸附源的端口
        """
        if des:
            item: 'YkGraphicsItem' = self.scene.items_scene_id.get(self.des_sid)
            if hasattr(item, 'ports'):
                return item.ports[self.des_port]
            else:
                return None
        else:
            item: 'YkGraphicsItem' = self.scene.items_scene_id.get(self.src_sid)
            if hasattr(item, 'ports'):
                return item.ports[self.src_port]
            else:
                return None


def points_contains(points, point, tolerance=6):
    """
    判断点击的位置point是否位于points列表里的某个点上，如果位于某个点上，则返回点的索引，未找到返回-1

    :param points: 点的列表，一般为图元上的控制点列表
    :param point: 点对象，图元坐标，一般为点击事件发生的鼠标的坐标
    :param tolerance: 允许的偏差
    :return:
    """
    for idx, p in enumerate(points):
        dx = p.x() - point.x()
        dy = p.y() - point.y()
        distance = math.sqrt(dx * dx + dy * dy)
        if distance <= tolerance:
            return idx
    return -1


class PopUp(QFrame):
    def __init__(self, parent, item, pos: QPointF):
        """
        :param parent: view对象
        :param pos: 场景坐标
        """
        pos = QPoint(int(pos.x()), int(pos.y()))
        super().__init__(parent)
        self.setLayout(QVBoxLayout())
        self.move(pos)  # 将弹出窗口移动到特定位置
        self.setWindowFlag(Qt.FramelessWindowHint)  # 将Form设置为无边框
        # self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.layout().addWidget(QLabel(f"{item.NAME}:{item.scene_id}"))

    def append_para(self, var, val, unit):
        if isinstance(unit, Unit):
            unit = unit.unit
        self.layout().addWidget(QLabel(f"{var:10}{val:10.3} {unit:10}"))


class Port:
    """
    图元上连接点的信息
    """

    def __init__(self, idx=1, point=QPointF(0, 0), type1="Inlet", description=""):
        super(Port, self).__init__()
        self.is_connect = False  # 该端口是否连接了管道
        self.edit_stream_item_scene_id = None  # 连接的管道对象实例的场景id，不能直接使用管线实例对象，否则无法pickle
        self.edit_stream_item_pid = None  # 连接的管道对象上的点在管道对象控制点中的编号
        self.parent_scene_id = None  # 端口所属的组件对象的场景id，不能直接使用组件实例对象，否则无法pickle

        self.idx = idx  # 端口在组件中的端口编号，一个组件可以有多个连接端口
        self.point = point  # 端口在组件中的图元坐标
        self.type1 = type1  # 入口，端口的类型，有入口，出口等类型
        self.description = description
        self.values = Values()

    def get_edit_stream_scene_id(self):
        """
        获取端口所连接管线的场景id
        :return:
        """
        return self.edit_stream_item_scene_id

    def get_edit_stream_info(self) -> "item_sid, pid":
        """
        获取port上连接的管线的信息
        :return: 返回连接管线的场景id和连接点的索引
        """
        return self.edit_stream_item_scene_id, self.edit_stream_item_pid

    def set_edit_stream(self, stream_item, pid=None):
        """
        设置端口连接的管线

        :param stream_item: PipeItem对象或PipeItem对象的场景id
        :param pid: 连接点在管线控制点中的编号，通过管线的control_points[pid]可以拿到连接点的图元坐标
        :return:
        """
        if stream_item is None:
            self.is_connect = False
        else:
            self.is_connect = True
        if isinstance(stream_item, PipeItem):
            self.edit_stream_item_scene_id = stream_item.scene_id
        else:
            self.edit_stream_item_scene_id = stream_item
        if pid is not None:
            self.edit_stream_item_pid = pid

    def set_info(self, parent_scene_id, is_connect, edit_stream=None, edit_stream_pid=None):
        """
        设置端口信息，生成具体的端口时，需要确定这些信息
        :param parent_scene_id: 端口所属的具体图元对象的场景id
        :param is_connect: 端口是否连接了edit stream管线对象
        :param edit_stream: 端口上连接的edit stream管线对象，如果端口尚未连接管线，则该值为空
        :return:
        """
        self.is_connect = is_connect
        self.set_edit_stream(edit_stream)
        self.parent_scene_id = parent_scene_id
        self.edit_stream_item_pid = edit_stream_pid

    def __str__(self):
        return f"{self.type1}:{self.idx}:{self.is_connect}:{self.point}"


class YkGraphicsLineItem(QGraphicsLineItem):
    def __init__(self):
        super(YkGraphicsLineItem, self).__init__()
        self.setPen(QPen(Qt.green, 4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        self.setPos(50, 50)
        self.setLine(0, 0, 500, 500)

    def set_scene_id(self, scene_id):
        self.scene_id = scene_id
        # for k, p in self.ports.items():
        #     p.parent_scene_id = scene_id

    def hoverEnterEvent(self, event):
        logger.debug("hover enter")
        self.setPen(QPen(QColor.red))

    def hoverLeaveEvent(self, event):
        self.setPen(QPen(QColor.black))
        logger.debug("hover leave")


class YkGraphicsItem(QGraphicsItem):
    def __init__(self):
        self.brush_color = QColor(50, 50, 255, 250)
        self.pen_width = 2  # 不能删除，因为管线处于强调状态时，会修改self.pen[0]的宽，如果不记录原始宽，则无法回复管线为非强调状态
        self.pen = [
            QPen(Qt.black, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin),
            QPen(Qt.black, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin),
            QPen(Qt.black, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin),
            QPen(Qt.black, self.pen_width, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin),
            QPen(Qt.blue, self.pen_width, Qt.DashLine, Qt.RoundCap, Qt.RoundJoin)  # 绘制选择边框的画笔
        ]  # 不能使用[QPen()]*5，因为这样会导致生成的5个QPen实际上是同一个对象
        self.brush = [QBrush(Qt.SolidPattern), QBrush(Qt.SolidPattern), QBrush(Qt.SolidPattern),
                      QBrush(Qt.SolidPattern), QBrush(Qt.SolidPattern)]
        super(YkGraphicsItem, self).__init__()
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.height = 40
        self.width = 40
        self.bounding = QRectF(-self.width / 2 - self.pen_width / 2, -self.height / 2 - self.pen_width / 2,
                               self.width + self.pen_width,
                               self.height + self.pen_width)
        self.EBS_ID = 0  # Ebsilon中的组件id
        self.scene_id = 0  # 场景中的组件编号
        self.id = 1  # 场景中的同类组件的编号
        self.icon = None
        self.NAME = ""  # 组件名
        self.EBS_NAME = ""  # Ebsilon中的组件名
        self.EBS_TYPE = ""  # Ebsilon中的组件类名
        self.SELECTION_HANDLE_SIZE = 6  # 图元上锚点的大小，即端口连接点的大小
        self.move_start_pos = None  # 拖动事件记录拖动起始点坐标
        self.move_start_ports = None  # 拖动事件记录起始管线信息
        self.SpecificationValues = None  #
        self.Result = None
        self.values = Values()  # 储存组件所有的参数的值
        self.ports: {int: Port} = {}  # 组件上与其他组件连接的端口的信息 {1: Port(idx=1, point=QPointF(0, 18), type1="Outlet")}
        self.calculated = False  # 用于标记当前组件是否计算完成
        self._temp = {}
        self.cal_order = 1

    def __str__(self):
        return f"{self.NAME} {self.scene_id}"

    def connect_point_region(self, point: QPointF):
        """
        获取图元坐标所属的连接点编号，不位于连接点则返回0

        :param point:
        :return:
        """
        w = self.SELECTION_HANDLE_SIZE / 2
        res = 0
        for k, v in self.ports.items():
            if isinstance(v, Port):
                p = v.point
                x, y = p.x(), p.y()
                x_min, x_max = x - w, x + w
                y_min, y_max = y - w, y + w
                if x_min < point.x() < x_max and y_min < point.y() < y_max:
                    res = k
        return res

    def before_com_calculate(self, step=0):
        """
        在单个组件开始计算之前，初始化组件当前时间步的值
        """
        if self.values.values_steps.get(step) is None:  # 无论计算是否成功，组件上当前时间步的值都要初始化
            # values_step[0]里存储着用户设置的参数，这些参数在任何时间步都是起效的
            self.values.values_steps[step] = self.values.values_steps[0].copy()
            self.values.values = self.values.values_steps[0]

    def make_equal(self, symbol_des, from_symbols: list, step):
        """
        使参数symbol_des的值从from_symbols中给出的值中获得，例如：
        self.make_equal("P", ["P1", "P2", "P3"])
        则当"P1", "P2", "P3"任何一个数值非空时，P将获得其值
        """
        for s in from_symbols:
            _ = self.get(s, need_unit=True)
            if _ is not None and _.value is not None and str(_.value).strip() != "":
                self.values.update({symbol_des: _}, step=step, set_none=False)

    def connect_point_region_ex(self, point_scene: QPointF):
        """
        获取图元坐标所属的连接点编号，不位于连接点则返回0，与connect_point_region的区别是图元以外距离图元端口接近的位置也会判定为
        连接点，且需要传入的参数是场景坐标

        :param point:
        :return:
        """
        w = self.SELECTION_HANDLE_SIZE / 2
        res = 0
        for k, v in self.ports.items():
            if isinstance(v, Port):
                p = self.mapToScene(v.point)
                x, y = p.x(), p.y()
                x_min, x_max = x - w, x + w
                y_min, y_max = y - w, y + w
                if x_min < point_scene.x() < x_max and y_min < point_scene.y() < y_max:
                    res = k
        return res

    def paint(self, painter: QtGui.QPainter, option: QStyleOptionGraphicsItem,
              widget: typing.Optional[QWidget] = ...) -> None:
        """
        组件Item的绘制必须在self.bounding以内，否则会出现移动拖影以及不刷新等各种问题

        :param painter:
        :param option:
        :param widget:
        :return:
        """
        # 绘制组件的边框，新插入的组件只有焦点，但未被选择
        if self.isSelected() or self.hasFocus():  # 可以同时选中多个组件，但不能同时focus多个组件
            painter.setPen(self.pen[4])
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.boundingRect())  # //绘制边框

        painter.setBrush(Qt.black)  # 连接点的绘制有YkGraphicsItem负责
        pen = QPen(Qt.black)
        pen.setWidth(self.SELECTION_HANDLE_SIZE)
        for k, v in self.ports.items():
            if v.type1 == "Inlet":
                pen.setColor(Qt.gray)
            elif v.type1 == "Outlet":
                pen.setColor(Qt.black)
            elif v.type1 == "Signal Inlet" or v.type1 == "Signal Outlet":
                pen.setColor(Qt.black)
            else:  # Set Value
                pen.setColor(Qt.green)
            painter.setPen(pen)
            painter.drawPoint(v.point)

    def get_prev_components(self):
        """
        获取与当前组件连接的上一个组件
        :return: 如果当前组件有多个入口，则上一个组件可能有多个，则返回列表
        """
        result = []
        for idx, port in self.ports.items():
            port: Port
            if port.type1 == "Inlet":
                pipe_sid, point_id = port.get_edit_stream_info()
                pipe: PipeItem = self.scene().items_scene_id.get(pipe_sid)
                comps = pipe.get_connect_components()  # 一条管线最多连接两个组件，中间连接的组件不考虑
                comp: YkGraphicsItem = None
                for _comp in comps:
                    if _comp != self:
                        comp = _comp
                if comp is not None:
                    result.append(comp)
        if len(result) == 0:
            result = None
        elif len(result) == 1:
            result = result[0]

        return result

    def get_next_components(self):
        result = []
        for idx, port in self.ports.items():
            port: Port
            if port.type1 == "Outlet":
                pipe_sid, point_id = port.get_edit_stream_info()
                pipe: PipeItem = self.scene().items_scene_id.get(pipe_sid)
                comps = pipe.get_connect_components()  # 一条管线最多连接两个组件，中间连接的组件不考虑
                comp: YkGraphicsItem = None
                for _comp in comps:
                    if _comp != self:
                        comp = _comp
                if comp is not None:
                    result.append(comp)
        if len(result) == 0:
            result = None
        elif len(result) == 1:
            result = result[0]

        return result

    def mouseDoubleClickEvent(self, QGraphicsSceneMouseEvent):
        print("double click")

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        print("mouse press from YkGraphicsItem")
        self.setFocus()
        self.setSelected(True)
        if event.button() == Qt.LeftButton:
            coor_item = self.mapFromScene(event.scenePos())  # 图元坐标
            connect_point_id = self.connect_point_region(coor_item)
            if self.scene().state == "常规":  # 3种情况，点击连接点开始绘制管线，点击选中组件，拖动组件
                if connect_point_id != 0:  # 如果点击了图元上的连接点，说明是绘制管线的情况，由场景事件处理，不会进入这里来
                    ...
                else:
                    # 2种情况，点击选中组件，拖动组件，此处无法区分这两种情况
                    self.move_start_pos = event.scenePos()  # 拖动事件中，单击意味着开始拖动，记录开始拖动时的场景坐标
                    self.move_start_ports = []
                    for idx, port in self.ports.items():  # 拖动组件时，同时移动组件上连接的管线的连接点坐标
                        stream_line = self.scene().items_scene_id.get(port.get_edit_stream_scene_id())
                        if stream_line is not None:
                            control_points = stream_line.control_points
                            self.move_start_ports.append({idx: control_points})
                    self.show_info()
            elif self.scene().state == "绘制管道":  # 如果点击到端口时，已经处于绘制管道状态，则连接管道并退出绘制管道状态
                ...  # 由场景事件负责
        elif event.button() == Qt.RightButton:
            if self.scene().state == "绘制管道":
                self.scene().views()[0].viewport().setCursor(Qt.ArrowCursor)
                self.scene().state = "常规"
                self.scene().removeItem(self.scene().last_line)
        # event.accept()  # 貌似没啥用
        # super().mousePressEvent(event)  # 如果不执行父类方法，则管线无法删除

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        # -------------------------释放鼠标时，取消所有拖动相关的特效显示---------------------------------------
        self.move_start_pos = None  # 拖动时间时，单击意味着开始拖动，记录开始拖动时的场景坐标
        self.move_start_ports = None
        # -------------------------释放鼠标时，取消所有拖动相关的特效显示---------------------------------------

        # -------------------------释放鼠标时，取消所有吸附相关的特效显示---------------------------------------
        _flag_item = self.scene().items_scene_id.get(-1)
        if _flag_item is not None:
            _flag_item.draw_ui(None)
            if hasattr(_flag_item, "emphasize_pipe"):
                _flag_item.emphasize_pipe.emphasize = False
        # -------------------------释放鼠标时，取消所有吸附相关的特效显示---------------------------------------

        # -------------------------释放鼠标时，如果有吸附发生---------------------------------------
        if self.scene().adsorb_info.adsorbed() and self._temp.get("moved"):
            # self.scene().adsorb_info.do()
            # 如果鼠标释放时，发生吸附，则移动组件的位置
            adsorb_info = self.scene().adsorb_info
            port: Port = adsorb_info.get_adsorbed_port(des=False)
            p = self.mapToScene(port.point)  # 吸附源点的当前位置
            _ = adsorb_info.des_point - p
            self.moveBy(_.x(), _.y())

            if port.type1 == "Inlet" or port.type1 == "Outlet":
                # 如果吸附端口是Inlet或者Outlet类型的端口
                # 更新吸附点所属的端口的信息，该端口更改为已连接，且记录连接的管线ID
                edit_stream_sid = self.scene().adsorb_info.des_sid
                port.set_edit_stream(edit_stream_sid, self.scene().adsorb_info.des_pid)
                # 更新吸附点所属的管线的信息
                pipe: PipeItem = self.scene().items_scene_id.get(edit_stream_sid)
                connect_item = ConnectItem(self.scene_id, des_port_id=port.idx,
                                           point_id=self.scene().adsorb_info.des_pid)
                pipe.connect_items.append(connect_item)  # 该语句不会添加重复的组件链接对象

            elif port.type1 == "Set Value":
                # 设置管线中的connect_items对象，增加值的设置
                edit_stream_sid = self.scene().adsorb_info.des_sid

                # 更新吸附点所属的管线的信息
                pipe: PipeItem = self.scene().items_scene_id.get(edit_stream_sid)

                # 判断当前吸附的项是否已经设置，即重复吸附
                _has_this_item = pipe.connect_items.has_this_item(ConnectItem(self.scene_id, port.idx, 0))
                if _has_this_item == -1:  # 如果吸附项不存在，则更新吸附点的坐标以及顺序
                    control_points = [pipe.mapToScene(p) for p in pipe.control_points]
                    lid = self.scene().adsorb_info.des_lid  # 如果吸附点位于第一条线段，则将点插入control_points中的第二个位置
                    control_points.insert(lid + 1, self.scene().adsorb_info.des_point)
                    pipe.update_line(vectors_scene=control_points)

                    # 更新吸附点所属的端口的信息，该端口更改为已连接，且记录连接的管线ID
                    port.set_edit_stream(self.scene().adsorb_info.des_sid, lid + 1)  # 通过port可以拿到连接的管线及管线上的点

                    # 更新管线上连接图元的信息
                    connect_item = ConnectItem(self.scene_id, port.idx, lid + 1)
                    pipe.connect_items.append(connect_item)

            self._temp["moved"] = False
            self.scene().adsorb_info.clear_adsorb_item()
        elif self._temp.get("moved") and not self.scene().adsorb_info.adsorbed():  # 如果没有吸附
            for port_id, port in self.ports.items():
                # 只有类型为Inlet或Outlet的端口，连接的管线点才会随设备图元移动而移动
                # 如果端口类型是Set Value，则管线上的点不移动，只是断开管线上的连接
                type1 = port.type1
                if type1 == "Set Value":
                    # ------------------------ 断开管线链接 -------------------------------------
                    stream_sid, stream_pid = port.get_edit_stream_info()
                    stream: PipeItem = self.scene().items_scene_id.get(stream_sid)
                    if stream is not None:
                        for ci in stream.connect_items:
                            ci: ConnectItem
                            if ci.equal_item(ConnectItem(self.scene_id, port.idx, 0)):
                                stream.connect_items.remove(ci)  # 管线连接项中删除当前端口
                                break
                        stream.remove_control_point(idx=stream_pid)  # 管线控制点中，删除当前连接点
                    port.set_edit_stream(None)  # 图元项端口中断开与管线的连接
                    # ------------------------ 断开管线链接 -------------------------------------
            self._temp["moved"] = False

        super(YkGraphicsItem, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        图元的鼠标移动事件，只有在鼠标按钮按下时才能触发，因此无法触发hover类的事件。
        管线图元的移动事件在PipeItem中重写，有PipeItem类的mouseMoveEvent实现

        :param event:
        :return:
        """
        print("mouse move event from YkGraphicsItem")
        # 检查图元是否有管线连接，如果有，则需要同时更新管线的位置，如果图元端口与某个管线端口接近则吸附

        QGraphicsItem.mouseMoveEvent(self, event)  # 调用父类的方法，完成图元位置的UI更新

        flag_item: SceneFlagItem = self.scene().items_scene_id.get(-1)  # 场景中的SceneFlagItem
        self._temp["moved"] = True  # 表示发生了鼠标拖动事件，在mouseReleaseEvent中，将moved置为False
        self.scene().adsorb_info.clear_adsorb_item()  # 先初始化吸附状态为未吸附
        for k, port in self.ports.items():
            if port.type1 in ["Inlet", "Outlet", "Signal Inlet", "Signal Outlet"]:
                if port.is_connect:  # 如果该端口与管线有连接，则该端口不用判断是否会吸附其他端口
                    pipe_scene_id, pipe_pid = port.get_edit_stream_info()
                    streamline: PipeItem = self.scene().items_scene_id.get(pipe_scene_id)  # 获取连接点处连接的管线对象
                    streamline.move_point(pipe_pid, self.mapToScene(port.point))
                else:  # 如果当前端口没有管线连接，则需要判断端口附近是否有其他管线的端点，有则吸附，移动过程中有一个端口吸附，则其他端口不再判断
                    # 如果图元组件的某一个端口已经发生吸附，则不再判断其他端口
                    if not self.scene().adsorb_info.adsorbed():
                        if port.type1 in ["Inlet", "Outlet"]:  # 进出口类型的端口吸附与逻辑类型的端口吸附行为不同
                            item_port_point = self.mapToScene(port.point)  # 获取当前端口的场景坐标
                            type_ = port.type1  # 当前端口的类型
                            need_type = self.scene().get_matched_port_type(type_)
                            pipes = self.scene().items.get("流") or []  # 获取场景中所有的管线，端口只可能与管线连接
                            for pipe in pipes:  # 遍历管线
                                pipe: PipeItem = pipe
                                # todo 此处获取的管线类型增加了Signal Inlet和Signal Outlet，因此需要修改以匹配新类型
                                pipe_inlet_outlet = pipe.get_input_output_type()  # 获取管线的类型
                                if pipe_inlet_outlet is None or pipe_inlet_outlet in need_type:
                                    pass
                                else:
                                    continue
                                points, _idx_list = pipe.get_unconnected_points()  # 获取管线上未连接的点
                                if points is None:
                                    continue
                                points_scene = [pipe.mapToScene(p) for p in points]  # 将点坐标映射到场景坐标
                                if points_scene is not None:  # 如果有未连接的点
                                    for p1, p_idx in zip(points_scene, _idx_list):  # 遍历未连接的点
                                        if isinstance(p1, tuple):
                                            logger.debug(f"奇怪的tuple{p1=}")  # 有时候会模型奇妙出现p1为tuple的情况
                                            return
                                        _ = (p1.x() - item_port_point.x()) ** 2 + (p1.y() - item_port_point.y()) ** 2
                                        _ = math.sqrt(_)  # 计算未连接点与当前端口的距离
                                        if _ < 吸附距离:
                                            self.scene().adsorb_info.update_info(des_sid=pipe.scene_id,
                                                                                 des_point=p1,
                                                                                 des_pid=p_idx,
                                                                                 des_port=None,
                                                                                 src_port=port.idx,
                                                                                 src_sid=self.scene_id)
                                            break
                                if self.scene().adsorb_info.adsorbed():
                                    break
                        elif port.type1 in ["Signal Inlet", "Signal Outlet"]:  # 吸附至现有管线或其他逻辑类型
                            self._adsorb_logic_port()  # 这是拖动组件时发生的事件，不是拖动管线时的事件
            elif port.type1 == "Set Value":
                # 如果是设置数据的端口，则需要吸附到管线
                item_port_point = self.mapToScene(port.point)  # 获取当前端口的场景坐标
                pipes = self.scene().items.get("流") or []  # 获取场景中所有的管线，端口只可能与管线连接
                for pipe in pipes:  # 遍历管线
                    # 判断port与管线的距离
                    distance, _p, _l = pipe.distance_to_point(item_port_point)
                    if distance <= 吸附距离:
                        self.scene().adsorb_info.update_info(des_sid=pipe.scene_id,
                                                             des_point=_p,
                                                             des_lid=_l,
                                                             des_port=None,
                                                             src_port=port.idx,
                                                             src_sid=self.scene_id)
                        break

        if self.scene().adsorb_info.adsorbed():  # 如果遍历管线后，存在发生吸附的管线
            adsorbed_port = self.scene().adsorb_info.get_adsorbed_port(des=False)  # 获取吸附源的端口
            adsorbed_p = self.scene().adsorb_info.des_point  # 吸附的目标点
            adsorbed_pipe_sid = self.scene().adsorb_info.des_sid  # 吸附的目标管线
            if adsorbed_port.type1 == "Inlet" or adsorbed_port.type1 == "Outlet":  # 如果是端口吸附，则在目标端口绘制FlagItem
                flag_item.draw_ui(adsorbed_p)
            elif adsorbed_port.type1 == "Set Value":  # 如果是管线吸附
                flag_item.draw_ui(adsorbed_p)
                pipe: PipeItem = self.scene().items_scene_id.get(adsorbed_pipe_sid)
                flag_item.emphasize_pipe = pipe
                pipe.emphasize = True
        else:
            flag_item.draw_ui(None)
            if hasattr(flag_item, 'emphasize_pipe') and flag_item.emphasize_pipe is not None:
                flag_item.emphasize_pipe.emphasize = False

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """
        item的键盘响应函数

        :param event:
        :return:
        """
        if event.key() == Qt.Key_Down:
            self.moveBy(0, 10)
        elif event.key() == Qt.Key_Up:
            self.moveBy(0, -10)
        elif event.key() == Qt.Key_Left:
            self.moveBy(-10, 0)
        elif event.key() == Qt.Key_Right:
            self.moveBy(10, 0)
        elif event.key() == Qt.Key_Escape:
            self.clearFocus()
        elif event.key() == Qt.Key_Delete:
            self.scene().removeItem(self)
        elif event.key() == Qt.Key_T:
            self.test()
        elif event.key() == Qt.Key_R:
            if not isinstance(self, PipeItem) and self.scene_id >= 2:  # 排除管线、坐标和网格图元
                self.setRotation(self.rotation() + 90)
                for idx, port in self.ports.items():
                    port: Port = port
                    sid, pid = port.get_edit_stream_info()
                    stream_line: PipeItem = self.scene().items_scene_id.get(sid)
                    if stream_line is not None:
                        stream_line.move_point(pid, self.mapToScene(port.point))  # 将端口位置也相应移动

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        # self.scene().popup = PopUp(None, self, event.screenPos())
        # symbols = ["P", "T", "H", "M"]
        # for s in symbols:
        #     val = self.get(s, need_unit=True)
        #     if val is not None:
        #         self.scene().popup.append_para(s, val.value, val.unit)
        #
        # self.scene().popup.show()
        if not isinstance(self, PipeItem):
            self.setToolTip(self.NAME + " (Shift查看)")

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.scene().views()[0].viewport().setCursor(Qt.ArrowCursor)
        try:
            self.scene().popup.hide()
        except:
            pass

    def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent) -> None:
        menu = QMenu()
        move_action = QAction("move back")
        act_action = QAction("test")
        menu.addAction(move_action)
        menu.addAction(act_action)
        selected_action = menu.exec(event.screenPos())
        if selected_action == move_action:
            self.setPos(0, 0)

    def scene(self) -> 'YkGraphicsScene':
        return super(YkGraphicsItem, self).scene()

    def show_info(self):
        """
        在主界面中显示组件的详细信息

        :return:
        """
        mainwindow = self.scene().get_main_window()
        # noinspection all
        mainwindow.display_info(scene_id=self.scene_id)

    def get(self, symbol, need_unit=False):
        """
        获取组件属性的值，如果值的value为None或空字符串，则都返回None

        :param symbol: 参数的符号
        :param need_unit: 是否需要返回单位
        :return:
        """
        symbol = str(symbol).strip()
        try:
            # 查询values中是否存在名称为symbol的变量
            value: Value = self.values.get(symbol, need_unit=need_unit)
            if isinstance(value, Value):
                _val = value.value
                _unit = value.unit
                if str(_val).strip() in ["None", ""]:
                    return None
                else:
                    if need_unit:
                        return value
                    else:
                        return _val
            elif type(value).__name__ in ["float", "int", "bool", "str"]:
                if need_unit:
                    return Value(value, None)
                else:
                    return value
            else:  # 如果value是None，则说明不存在名为symbol的变量，进一步判断symbol是否是类似P1这种类型的变量，如果是则查询编号为1的端口的P值
                port_id = re.findall(r"(\d+)$", symbol)  # 匹配字符串末尾的数字
                if len(port_id) == 0 or port_id is None:
                    return None
                else:
                    port_id = int(port_id[0])
                    symbol_ = symbol.strip(str(port_id))
                    port: Port = self.ports.get(port_id)
                    if port is None:
                        traceback.print_exc()
                    res = port.values.get(symbol_, need_unit=need_unit)
                    if res is not None:
                        return res
                    else:
                        # logger.debug(f"组件{self.scene_id}中不存在名为{symbol}的变量！")
                        return None
        except:  # 如果字符串末尾是数字，则从组件上id为该数字的端口上查询该值
            traceback.print_exc()

    # def set(self, symbol, value, unit=None):
    #     """
    #     设置参数的值，这里只设置了参数的字符串单位，如果有同名字符串单位，需要额外处理单位类型.且值只会设置到self.values.values属性中
    #     如果是计算结果的更新，请使用self.values.update()方法
    #
    #     :param symbol:
    #     :param value:
    #     :param unit:
    #     :return:
    #     """
    #     v_cur = self.values.get(symbol, need_unit=True)  # need_unit参数，返回的是Value类型，带参数的单位
    #     if v_cur is not None and str(v_cur.value).strip() != "":
    #         logger.debug(f"设置{self.scene_id}号组件的{symbol}值时发生冲突，当前值为{v_cur.value}，待赋值为{value}")
    #     if isinstance(value, Value):
    #         self.values.update({symbol: value})
    #         return
    #     else:
    #         self.values.update({symbol: Value(value, unit)})

    def calculate(self, step=None):
        self.values.set_values(step=step, values={})
        pass

    def spread_values(self, step=None, symbols=None):
        """
        将计算结果扩散到与该组件连接的其他组件上，需要手动调用，这是父类的方法
        """
        if symbols is None:
            symbols = ["P", "T", "H", "M"]

        values = {}
        for s in symbols:
            values.update({s: copy.deepcopy(self.get(s, need_unit=True))})

        if hasattr(self, "connect_items"):  # 说明是管道组件，管道组件自己处理自己的传值方法
            ...
        else:
            # 获取组件的端口
            for pid, p in self.ports.items():
                # 端口上的值初始与组件相同，但不同端口可能不同，以端口的id为后缀进行区分，如P1、P2分别表示组件上端口1和端口2的压力
                p_values = values.copy()
                p: Port = p
                # 这里不能使用p.values.set_values方法，因为set_values方法会从self.values中删除values中没有的参数，而这些参数可能是从其他组件
                # 传递过来的，不应该被删除，set_none设置为False，表示不清空已有值，所有的清空数据操作应在计算开始前有主线程统一删除
                for s in symbols:
                    _val = copy.deepcopy(self.values.get(f"{s}{pid}", need_unit=True))
                    if values.get(s) is None and _val is not None:
                        p_values.update({s: _val})
                p.values.update(step=step, values=p_values, set_none=False)

    def after_values_updated(self):
        pass

    def test(self):
        self.setPos(self.pos() + QPointF(10, 0))

    def init_default_values(self):
        """
        当用户将组件拖入面板时，组件初始化时可以具有一些默认参数的值，需要更新到self.values中，如果组件的values中已经有值，该方法不会初始化
        具有数据的参数项。
        :return:
        """
        if self.SpecificationValues is None:
            return
        if self.values.values is not None and len(self.values.values) > 0:  # 如果values有值，说明已经初始化过，不应在初始化
            return
        for cls, yk_items in self.SpecificationValues.items():
            for value_item in yk_items:
                tag = value_item[1]
                value = value_item[2]
                value = value[0] if isinstance(value, list) else value
                if isinstance(value, dict):
                    # YkItem("环境温度1", "10", {value:["℃", "K"], selected_idx: 0}, size=[100, 20, 50])
                    # YkItem("环境温度2", "10", {value:["℃", "K"], selected_val: "℃"})
                    if value.get("selected_val") is not None:
                        value = value.get("selected_val")
                    elif value.get("value") is not None and value.get("selected_idx") is not None:
                        value = value.get("value")[value.get("selected_idx")]
                if len(value_item) >= 4:
                    unit = value_item[3]
                else:
                    unit = None
                if value is not None and str(value).strip() != '':  # 取
                    self.values.update({tag: Value(value, unit)})

    def _adsorb_logic_port(self):
        """
        鼠标移动事件中，发生logic端口吸附时，吸附端口至特定组件位置
        """
        pass

    def generate_icon(self):
        """
        绘制组件的图标，如果组件类存在icon_file，则直接使用指定的图标文件，否则根绝self.paint方法绘制相应的组件图标
        """
        if self.icon is None:
            self.icon = QIcon(pixmap_from_item(self, keep_ratio=True))
        return self.icon

    def boundingRect(self) -> QRectF:
        """
        定义了组件item在视图场景中的范围，该范围会响应鼠标点击、碰撞检测等方法
        :return:
        """
        # super(YkGraphicsItem, self).boundingRect()
        pen_width = self.pen[0].width()
        self.bounding = QRectF(-self.width / 2 - pen_width / 2, -self.height / 2 - pen_width / 2,
                               self.width + pen_width,
                               self.height + pen_width)
        return self.bounding

    def set_scene_id(self, scene_id):
        self.scene_id = scene_id
        for k, p in self.ports.items():
            p.parent_scene_id = scene_id

    def dynamic_unit(self, symbol: str):
        """
        根据某个参数(symbol)的值，确定返回的单位

        :param symbol:
        :return:
        """
        参数类型 = self.values.get_initial(symbol)
        if 参数类型 is None:
            return None
        elif not isinstance(参数类型, str):
            logger.debug(f"{参数类型=}")
        elif 参数类型.startswith("1:"):
            return Pressure()  # 返回默认的压力单位，这里的压力单位是软件或项目中设置的默认值
        elif 参数类型.startswith("2:"):
            return Temperature()
        elif 参数类型.startswith("3:"):
            return Enthalpy()
        elif 参数类型.startswith("4:"):
            return MassFlow()
        else:
            return Power()


class YkGraphicsScene(QGraphicsScene):
    """
    视图窗口中的场景类
    """
    item_changed_signal = pyqtSignal(str)

    def __init__(self):
        from yangke.ebsilon.ALPHA import MainWindow

        super(YkGraphicsScene, self).__init__()
        self.main_window: MainWindow | None = None
        self.scene_rect = QRectF(0, 0, 1500, 800)
        self.grid_item = None
        self.coor_item = None
        self.flag_item: SceneFlagItem | None = None
        self.items = {}  # 以组件类型索引的场景组件列表，例如：{'边界值': [<components.Comp1.Item object at 0x000001A0D93BEB00>]}
        self.items_scene_id: {int: YkGraphicsItem} = {}  # 以场景id索引的场景组件列表
        self.ids_total = 0  # 组件在场景中的编号
        self.add_flag_item()
        self.show_grid()
        self.show_coor()
        self.state = "常规"  # "绘制管道"
        self.vectors = []
        self.adsorb_info = AdsorbInfo(self)
        self.dragging_pipe = None
        self.popup: PopUp | None = None
        self.current_step = 0  # 当前的计算步
        self.addItem(YkGraphicsLineItem())

    def itemAt(self, pos, deviceTransform):
        super(YkGraphicsScene, self).itemAt(pos)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """
        场景事件先触发，然后场景调用图元事件。键盘响应函数

        :param event:
        :return:
        """
        if event.key() == Qt.Key_Delete:  # 如果是删除图元，则不再执行图元的按键事件
            items = self.selectedItems()  # 获取到当前激活的图元
            if items is None:  # 当不选择任何图元按delete键时，item为None
                return
            for item in items:
                if isinstance(item, PipeItem):
                    connect_items = item.get_connect_items()  # [{"item": YkGraphicsItem(), "port_id": 1}]
                    for it in connect_items:
                        it: ConnectItem
                        item1: YkGraphicsItem | QGraphicsItem = self.items_scene_id.get(it.item_sid)
                        port_idx = it.port_id
                        port = item1.ports[port_idx]  # {1: ConnectPoint(0,20)}
                        port.set_edit_stream(None)
                    item.control_points = None
                elif isinstance(item, YkGraphicsItem):  # 删除图元组件时，需要删除与其连接的组件的连接信息
                    for idx, port in item.ports.items():
                        stream_line: PipeItem = self.items_scene_id.get(port.edit_stream_item_scene_id)
                        if stream_line is not None:
                            _cis = []
                            for _item in stream_line.connect_items:
                                _item: ConnectItem
                                if _item.item_sid != item.scene_id:
                                    _cis.append(_item)
                            stream_line.connect_items = _cis

                self.removeItem(item)
                self.update_ids_total()
        elif event.key() == Qt.Key_F9:
            self.get_main_window().keyPressEvent(event)
        elif event.modifiers() == Qt.ShiftModifier | Qt.ControlModifier and event.key() == Qt.Key_AsciiTilde:
            self.get_main_window().keyPressEvent(event)
        elif event.key() == Qt.Key_Escape:
            if self.state == "绘制管道":
                # 如果是停止绘制管线，则更新最后的管线坐标
                if hasattr(self, "last_line") and self.last_line.control_points is not None:
                    self.last_line.update_line(vectors_item=self.last_line.control_points)
                self.state = "常规"
            else:
                QGraphicsScene.keyPressEvent(self, event)
        else:  # 除了delete键以外的其他按键事件，均进一步调用图元的按键事件
            QGraphicsScene.keyPressEvent(self, event)  # 执行后，图元事件才会触发

    def update_ids_total(self):
        _id = 2
        for idx, com in self.items_scene_id.items():
            if idx >= _id:
                _id = idx + 1

        self.ids_total = _id

    def start_draw_pipe(self, port, item_):
        """
        开始绘制管道，port为开始绘制管道的端口对象，item_为开始绘制管道的组件图元对象
        :param port:
        :param item_:
        :return:
        """
        self.views()[0].viewport().setCursor(Qt.CrossCursor)  # 将场景视图的鼠标设置为十字星
        self.state = "绘制管道"  # 设置场景状态为正在画线
        fluid_type = "Steam"
        fluid_type = "Logic" if port.type1 in ["Signal Inlet", "Signal Outlet"] else fluid_type
        self.last_line = PipeItem(fluid_type=fluid_type)
        self.last_line.setPos(item_.mapToScene(port.point))
        self.last_line.control_points = [QPointF()] * 2  # 新建的管线起点坐标是(0,0)，第二个坐标未定
        self.last_line.connect_items.append(ConnectItem(item_.scene_id, port.idx, 0))
        self.addItem(self.last_line)
        port.set_info(parent_scene_id=item_.scene_id, is_connect=True,
                      edit_stream=self.last_line,
                      edit_stream_pid=0)

    def mouseReleaseEvent(self, event):
        self.dragging_pipe = None
        super().mouseReleaseEvent(event)  # 必须调用super的方法，否则PipeItem的release方法不会执行

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        场景鼠标事件响应，绘制管线，添加组件等

        :param event:
        :return:
        """
        logger.debug("mouse press from Scene")
        main_window = self.get_main_window(event.widget())  # 主界面
        item_: YkGraphicsItem | QGraphicsItem = self.itemAt(event.scenePos(), QTransform())
        if event.button() == Qt.LeftButton:
            if isinstance(item_, SceneGridItem) or isinstance(item_, CoordinateItem):  # 点击的位置没有其他组件
                if self.state == "常规":
                    # 判断是否选中组件导航面板的组件，如果是，则添加组件到场景中
                    idx = main_window.choose_component
                    if idx != 0:  # 如果组件列表中选中任何组件，则添加组件到场景中
                        if idx == 'text':
                            item: TextItem = TextItem('###')
                            item.setPos(event.scenePos())
                            self.addItem(item)
                            item.setFocus(Qt.MouseFocusReason)
                        else:
                            try:
                                item: YkGraphicsItem = self.get_main_window().all_comps[f"Comp{idx}"]()
                                item.setPos(event.scenePos())
                                self.addItem(item)
                                item.setFocus(Qt.MouseFocusReason)
                            except NameError:
                                logger.warning(f"没有选定的组件,ebs_id={idx}")
                    else:  # 没有选中图元组件，且不是添加组件时，无需做任何操作
                        ...
                elif self.state == "绘制管道":  # 绘制管道时
                    item_des_sid, port_des_id = self.get_item_port_of_pos(event.scenePos())  # 获取鼠标位置是否处于某个端口附近
                    if port_des_id is None:  # 说明鼠标位置不在任何一个端口的邻域内，则添加新点到绘制的管线中
                        # 判断正在绘制的管道类型，如果是Signal，则需要判断是否吸附到管线
                        if self.adsorb_info.des_sid is not None:
                            self.adsorb_line_to_point(self.adsorb_info)
                        else:
                            self.add_new_point_to_pipeline(event, self.last_line)
                    else:  # 鼠标单击位置位于某个端口的邻域内，则吸附到该端口，并结束绘制管道
                        # 至此，距离已经接近，但类型不知道是否匹配，且端口连接状态未知
                        # self.state = "常规"  # 不能在此设置state为"常规"，吸附方法中指定端口可能已经连接，则继续绘制
                        self.adsorb_line_to_port(item_des_sid, port_des_id, self.last_line, event)
                return  # 此处直接返回，不要再调用组件的鼠标事件
            elif not isinstance(item_, YkGraphicsItem):  # 点击的位置不是系统组件
                self.clearFocus()
                self.clearSelection()
                pass
            else:  # 如果点击到了组件，则有4种情况，1即将绘制管线，2连接正在绘制的管线，3拖动组件，4显示组件信息
                if item_ is None:  # 有时候会点击到外部空间
                    return
                main_window.choose_component = 0  # 点击到其他组件上时，则取消插入新组件的命令
                main_window.ui.lv_com.clearSelection()
                self.clearFocus()
                coor_item = item_.mapFromScene(event.scenePos())  # 将场景坐标转换为点击处图元中的图元坐标
                connect_port_id = item_.connect_point_region(coor_item)  # 获得点击位置是否位于图元中的port上，有则拿到端口id
                if self.state == "常规":
                    if connect_port_id != 0:
                        port: Port = item_.ports[connect_port_id]  # 点击位置的图元的端口
                        if port.type1 in ["Inlet", "Outlet", "Signal Inlet", "Signal Outlet"]:  # 只响应特定类型的端口
                            if not port.is_connect:
                                self.start_draw_pipe(port, item_)
                            else:
                                QMessageBox.warning(self.main_window, "提示", "一个端口只能连接一条管线！",
                                                    QMessageBox.Ok, QMessageBox.Ok)
                        return  # 此处直接返回，不要再调用组件的鼠标事件
                    else:
                        # 只是点击到图元上，但未点击到端口上，一般来说，这是要3拖动组件，4显示组件信息，这两种情况交给图元的鼠标点击事件处理
                        # 无须任何操作
                        ...
                elif self.state == "绘制管道":
                    if connect_port_id != 0:
                        port: Port = item_.ports[connect_port_id]  # 点击位置的图元的端口
                        # 点击到了某个图元的端口，且当前处于绘制管道状态中，则判断是否连接管道，并退出绘制状态
                        # 至此，距离已经接近，但类型不知道是否匹配，且端口连接状态未知
                        self.adsorb_line_to_port(item_.scene_id, port.idx, self.last_line, event)
                    else:  # 添加新点至正在绘制的管道，因为可能点击到管线图元上，而管线图元很大，
                        self.add_new_point_to_pipeline(event, self.last_line)
                    return  # 此处直接返回，不要再调用组件的鼠标事件

        elif event.button() == Qt.RightButton:
            main_window.choose_component = 0
            main_window.ui.lv_com.clearSelection()
            # 如果是停止绘制管线，则更新最后的管线坐标
            if self.state == "绘制管道":
                self.last_line.update_line(vectors_item=self.last_line.control_points)
                self.state = "常规"
        QGraphicsScene.mousePressEvent(self, event)  # 触发图元事件

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        鼠标移动事件
        :param event:
        :return:
        """
        # print("mouse move event from YkGraphicsScene")

        # 调用父类的方法完成图元UI位置更新，必须与YkGraphicsItem的mouseMoveEvent事件结合才可以移动
        super(YkGraphicsScene, self).mouseMoveEvent(event)

        if self.state == "绘制管道":  # 如果是绘制管道模式，则随着鼠标移动，动态更新管道路线
            point = event.scenePos()
            # 先判断鼠标位置是否可以吸附某个组件的端口
            ci_src: ConnectItem = self.last_line.connect_items[0]
            item_src: YkGraphicsItem = self.items_scene_id.get(ci_src.item_sid)
            port_src: Port = item_src.ports[ci_src.port_id]
            type_src = port_src.type1  # 正在绘制的管线的类型
            _des = self.get_matched_port_type(type_src)
            # 遍历所有组件，查询未连接的端口
            item, port = self.get_item_port_of_pos(event.scenePos())
            if port is None:  # 说明鼠标点击位置不位于任何组件端口的邻域内
                if type_src in ["Signal Inlet", "Signal Outlet"]:
                    # 需要进一步判断是否接近任何管线，如果是，则需要吸附
                    pipe_sid, dis, p, line_idx = self.get_nearest_pipeitem_point(event.scenePos())
                    if pipe_sid is None:
                        ...
                    else:
                        if dis < 吸附距离:
                            self.last_line.control_points[-1] = self.last_line.mapFromScene(point)  # 只有管线的最后一个点是动态更新的
                            _ = self.adjust(obj=self.last_line.control_points, ref=-2, index=-1)
                            正交吸附后的点 = self.last_line.mapToScene(_[-1])
                            pipe_item: PipeItem = self.items_scene_id.get(pipe_sid)
                            dis, p, line_idx = pipe_item.distance_to_point(正交吸附后的点)
                            self.flag_item.draw_ui(p)
                            self.adsorb_info.update_info(des_point=p,
                                                         des_sid=pipe_sid,
                                                         des_lid=line_idx,
                                                         des_pid=None,
                                                         des_port=None,
                                                         src_sid=self.last_line.scene_id,
                                                         src_point=event.scenePos(),
                                                         src_pid=-1,
                                                         src_port=None)  # 更新吸附信息
                        else:
                            self.flag_item.draw_ui(None)
                            self.adsorb_info.clear_adsorb_item()
                else:
                    self.flag_item.draw_ui(None)
            else:
                _item: YkGraphicsItem = self.items_scene_id[item]
                _port: Port = _item.ports[port]
                point_des = _item.mapToScene(_port.point)
                if not _port.is_connect and _port.type1 in _des:  # 如果端口未连接且类型匹配
                    self.flag_item.draw_ui(point_des)
                else:
                    self.flag_item.draw_ui(None)

            self.last_line.control_points[-1] = self.last_line.mapFromScene(point)  # 只有管线的最后一个点是动态更新的
            _ = self.adjust(obj=self.last_line.control_points, ref=-2, index=-1)
        elif self.state == "常规":
            pipe: PipeItem | None = self.dragging_pipe
            if pipe is not None:
                pipe.mouseMoveEvent(event)

        self.update(self.sceneRect())
        # noinspection all
        mw: QLabel = self.get_main_window().status_bar_coor
        mw.setText(f"{int(event.scenePos().x())},{int(event.scenePos().y())}")  # 状态栏鼠标位置信息更新

    def adjust(self, obj, ref=None, index=-1, torlence=10):
        """
        根据场景中的对象调整obj中控制点的位置，如果index不为None，则仅调整obj中索引为index的点。
        示例：
        self.adjust([(), ()], ref=-2, index=-1)， 则参考倒数第二个点调整倒数第一个点

        :param obj:
        :param ref: 参考的对象，可以是点，线，如果为空，则以obj的其他点为参考
        :param index:
        :param torlence: 可以接受的调整的最大值
        :return:
        """
        p_tuple = obj
        type_flag = None
        if isinstance(obj, list):
            if len(obj) >= 1:
                try:
                    if isinstance(obj[0], QPointF) or isinstance(obj[0], QPoint):
                        p_tuple = [(p.x(), p.y()) for p in obj]
                        type_flag = "QPointF"
                    elif isinstance(obj[0], tuple):
                        pass
                except:
                    traceback.print_exc()
                    logger.debug(f"{obj=}")
                    exit(1)
            else:
                return obj
        try:
            p = p_tuple[index]
            if isinstance(ref, int):  # 参考是个索引值，则从当前对象中获取该索引对应的点
                ref_p = p_tuple[ref]
            elif ref is None:  # 如果为空，则以当前对象的其他点为参考
                ref_p = p_tuple
            else:  # 以指定的ref为参考
                ref_p = ref

            if isinstance(p, tuple) and isinstance(ref_p, tuple):  # 如果参考点和待调整点都为点，则直接调整
                p = (ref_p[0], p[1]) if abs(p[0] - ref_p[0]) < torlence else p
                p = (p[0], ref_p[1]) if abs(p[1] - ref_p[1]) < torlence else p

            # 构建返回值
            if type_flag == "QPointF":
                obj[index].setX(p[0])
                obj[index].setY(p[1])
            return obj
        except:
            return obj

    def get_matched_port_type(self, type1):
        if type1 == "Inlet":
            _des = ["Outlet"]
        elif type1 == "Outlet":
            _des = ["Inlet"]
        elif type1 == "Signal Inlet":
            _des = ["Signal Outlet"]
        elif type1 == "Signal Outlet":
            _des = ["Signal Inlet"]
        else:
            _des = ["Inlet", "Outlet"]
        return _des

    def add_new_point_to_pipeline(self, event, pipeline):
        # 不能连接，则添加新点后继续绘制管线
        _last_point = pipeline.mapToScene(pipeline.control_points[-2])
        _last_distance = distance(_last_point, event.scenePos())
        # 计算点击的位置与管线上上一个点的位置的距离，如果距离过近，则忽略当前点，否则会吸附至同一点
        if _last_distance is not None:
            if _last_distance <= 吸附距离:
                ...  # 小于吸附距离，只是忽略当前点，但仍然处于绘制管线状态，因此不做任何操作
            else:
                _ = self.adjust(obj=pipeline.control_points, ref=-2, index=-1,
                                torlence=吸附距离)  # 坐标轴吸附
                _.append(pipeline.mapFromScene(event.scenePos()))  # 添加新的动点
                pipeline.update_line(vectors_item=_)

    def adsorb_line_to_point(self, adsorb_info: AdsorbInfo):
        """
        绘制管线时，将管线的最后一个点吸附到目标管线的目标点上

        :param adsorb_info: 吸附信息
        """
        self.state = "常规"  # 结束绘制管线操作

        # ------------------------- 在目标管线上新建控制点，并添加该点的链接为正在绘制的管线 ---------------------------------
        des_line_item: PipeItem = self.items_scene_id.get(adsorb_info.des_sid)
        src_line_item: PipeItem = self.items_scene_id.get(adsorb_info.src_sid)
        if isinstance(des_line_item, PipeItem):
            des_line_item.control_points.insert(adsorb_info.des_lid + 1,
                                                des_line_item.mapFromScene(adsorb_info.des_point))

            ci1 = ConnectItem(des_line_item, point_id=-1, des_point_id=adsorb_info.des_lid + 1)
            src_line_item.connect_items.append(ci1)
            ci2 = ConnectItem(src_line_item, point_id=adsorb_info.des_lid + 1, des_point_id=-1)
            des_line_item.connect_items.append(ci2)
        # ------------------------- 在目标管线上新建控制点，并添加该点的链接为正在绘制的管线 ---------------------------------

        # ------------------------- 将源管线上的最后一个点移动到吸附的目标点 ----------------------------------
        src_line_item.move_point(-1, pos=adsorb_info.des_point)
        self.flag_item.draw_ui(None)
        # ------------------------- 将源管线上的最后一个点移动到吸附的目标点 ----------------------------------

        self.adsorb_info.clear_adsorb_item()

    def adsorb_line_to_port(self, item_des_sid, port_des_id, pipeline, event):
        """
        绘制管线时，将管线的最后一个点吸附到目标组件的目标端口上

        :param item_des_sid: 目标组件的场景id
        :param port_des_id: 目标端口编号
        :param pipeline: 正在绘制的管线对象
        """

        item_des: YkGraphicsItem = self.items_scene_id.get(item_des_sid)
        port_des: Port = item_des.ports.get(port_des_id)

        ci_src = pipeline.connect_items[0]
        ci_src: ConnectItem
        item_src: YkGraphicsItem = self.items_scene_id.get(ci_src.item_sid)
        port_src: Port = item_src.ports[ci_src.port_id]
        _des = self.get_matched_port_type(port_src.type1)  # 与管线匹配的可以连接的端口的类型

        if not port_des.is_connect and port_des.type1 in _des:  # 至此，类型也匹配，端口也未连接，则直接吸附
            point_des = item_des.mapToScene(port_des.point)
            pipeline.control_points[-1] = pipeline.mapFromScene(point_des)
            pipeline.update_line(vectors_item=pipeline.control_points)
            self.state = "常规"
            self.views()[0].viewport().setCursor(Qt.ArrowCursor)
            # 更新数据连接
            # [{"item": YkGraphicsItem().scene_id, "port_id": 1, "point_id": 0}]
            pipeline.connect_items.append(ConnectItem(item_des_sid, port_des_id, -1))
            port_des.set_edit_stream(pipeline, pid=-1)
            self.flag_item.draw_ui(None)
            self.adsorb_info.clear_adsorb_item()
        else:
            self.add_new_point_to_pipeline(event, pipeline)

    def get_nearest_pipeitem_point(self, pos: QPointF):
        """
        获取距离点击位置距离最近的管线及管线上距离最近的点（排除self.last_line），该点可以不是管线上的控制点，一般为点击位置与目标管线的垂足点

        如果点与管线上的垂足位于管线线段以外区域，则返回None, None, None, None

        return 返回参数为: (管线的场景id, 距离, 点索引, 线段索引)
        """
        dis = 100000
        p, line_idx = None, None
        pipe_sid = None
        for pipe in self.items["流"]:
            pipe: PipeItem
            if pipe == self.last_line:
                continue
            _dis, _p, _line_idx = pipe.distance_to_point(pos)
            if _dis < dis:
                dis, p, line_idx = _dis, _p, _line_idx
                pipe_sid = pipe.scene_id
        if dis >= 10000:
            return None, None, None, None
        return pipe_sid, dis, p, line_idx

    def pipe_item_at(self, scene_pos: QPointF, upper: 'PipeItem' = None):
        """
        查找场景中在scene_pos位置处的管线对象

        :param scene_pos: 场景坐标
        :param upper: 鼠标点击位置最上层的管线对象，该管线对象的boundingRect与鼠标点击位置重叠
        """
        if upper is None:
            if self.items.get("流") is not None:
                for pipe in self.items["流"]:
                    pipe: PipeItem
                    if pipe.boundingRect().contains(pipe.mapFromScene(scene_pos)):
                        if pipe.contains_point(scene_pos):
                            return pipe
        else:
            for pipe in upper.collidingItems():
                if isinstance(pipe, PipeItem):
                    if pipe.contains_point(scene_pos):
                        return pipe
        return None

    def addItem(self, item: YkGraphicsItem, scene_id=None, id=None) -> None:
        """
        向项目场景中添加组件，所有的组件添加必须经过该方法

        :@param
        """
        # -------------------------------- 添加组件后，更新场景的items参数 -------------------------------
        # scene.items以组件分类形式记录了场景中的所有组件，便于其他地方使用组件
        if isinstance(item, YkGraphicsItem):
            items = self.items.get(item.NAME)
            if items is None or len(self.items[item.NAME]) == 0:
                self.items.update({item.NAME: [item]})
                if id is None:
                    item.id = 1
                else:
                    item.id = id
            else:  # 当前类必然存在至少一个实例组件
                if id is None:
                    com: YkGraphicsItem = self.items[item.NAME][-1]  # 取当前类的最后一个组件的id，id+1为当前新加组件的id
                    item.id = com.id + 1
                else:
                    item.id = id
                self.items[item.NAME].append(item)  # 必须置于id设置之后
        if hasattr(item, "init_default_values"):
            item.init_default_values()  # 初始化组件的默认参数

        super(YkGraphicsScene, self).addItem(item)  # 无论是否是YkGraphicsItem，都要调用父类的addItem方法
        # -------------------------------- 添加组件后，更新场景的items参数 -------------------------------

        # -------------------------------- 添加组件后，更新场景的items_scene_id参数 -------------------------------
        # scene.items_scene_id以场景索引形式记录了场景中的所有组件，只要知道组件在场景中的id，即可快速拿到组件对象
        if scene_id is None:
            item.set_scene_id(self.ids_total)  # 不能直接给scene_id赋值，需要通过set_scene_id方法
        else:
            item.set_scene_id(scene_id)
        self.items_scene_id.update({item.scene_id: item})
        if scene_id is None:
            self.ids_total += 1
        else:
            self.ids_total = max(self.ids_total + 1, scene_id + 1)
        # -------------------------------- 添加组件后，更新场景的items_scene_id参数 -------------------------------
        self.item_changed_signal.emit(str(self.ids_total - 1))

    def removeItem(self, item: QGraphicsItem) -> None:
        """
        移除项目场景中的组件，所有的组件删除必须经过该方法
        """
        try:
            if self.main_window is None:
                self.main_window = self.get_main_window()
            for k, v in self.items.items():
                for item_ in v:
                    if item.scene_id == item_.scene_id:
                        self.items[k].remove(item_)

            scene_model_name = f"{item.NAME}_{item.id} / S{item.scene_id}"

            self.items_scene_id.pop(item.scene_id)
            if item.scene_id == self.ids_total - 1:  # 如果删除的是场景中最后一个添加的元素，则将场景中下一个元素的索引减1
                self.ids_total -= 1

            self.item_changed_signal.emit(f"del {scene_model_name}")
            super(YkGraphicsScene, self).removeItem(item)
        except:
            traceback.print_exc()

    def hide_grid(self):
        if self.grid_item is not None:
            self.removeItem(self.grid_item)
            self.grid_item = None

    def show_grid(self):
        if self.grid_item is None:
            self.grid_item = SceneGridItem(self.scene_rect)
            self.addItem(self.grid_item)

    def hide_coor(self):
        if self.coor_item is not None:
            self.removeItem(self.coor_item)
            self.coor_item = None

    def show_coor(self):
        if self.coor_item is None:
            self.coor_item = CoordinateItem()
            self.addItem(self.coor_item)

    def add_flag_item(self):
        if self.flag_item is None:
            self.flag_item = SceneFlagItem()
            self.addItem(self.flag_item, scene_id=-1, id=1)

    def setSceneRect(self, rect: QRectF) -> None:
        """
        该方法会导致反复添加场景中的组件

        """
        rect = QRectF(rect)
        self.scene_rect = rect
        super(YkGraphicsScene, self).setSceneRect(rect)
        self.hide_grid()
        self.show_grid()
        self.hide_coor()
        self.show_coor()

    def get_main_window(self, widget=None):
        from yangke.ebsilon.ALPHA import MainWindow
        if widget is None:
            widget = self.views()[0]
        if self.main_window is not None:
            return self.main_window
        else:
            _ = widget
            while _.parentWidget() is not None:
                _ = _.parentWidget()
                if isinstance(_, YkWindow):
                    # noinspection all
                    self.main_window: MainWindow = _
                    return _

        logger.debug("未找到YkGraphicsView的父窗口")

    def get_item_port_of_pos(self, pos_scene: QPointF):
        """
        获取场景坐标是否位于某个组件端口的邻域内，如果是，返回组件id及port_id
        """
        for sid, item in self.items_scene_id.items():
            item: YkGraphicsItem = item
            if hasattr(item, "ports"):
                for port_id, port in item.ports.items():
                    point = item.mapToScene(port.point)
                    dis = distance(pos_scene, point)
                    if dis < 吸附距离:
                        return sid, port_id
        return None, None


class YkGraphicsView(QGraphicsView):
    """
    视图窗口中的视图类
    """

    def __init__(self, scene):
        super(YkGraphicsView, self).__init__(scene)
        from yangke.ebsilon.ALPHA import MainWindow  # 不能在全局引入，否则会和ALPHA模块循环引用
        self.main_window: MainWindow | None = None
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        self.setAcceptDrops(True)  # 使场景组件可以接受拖放事件

    def dragEnterEvent(self, event: QtGui.QDragEnterEvent) -> None:
        """
        拖放事件，拖放鼠标进入当前场景时
        """
        event.accept()

    def dragMoveEvent(self, event: QGraphicsSceneDragDropEvent) -> None:
        """
        必须实现该方法，才能触发dropEvent
        """
        event.accept()

    def dropEvent(self, event: QGraphicsSceneDragDropEvent) -> None:
        mime_data = event.mimeData()
        pos = self.mapFromScene(self.scene().coor_item.pos())  # scene的坐标原点在在view中的坐标
        if mime_data.hasFormat('com_data'):  # 说明拖放的是一个组件对象
            data = bytes(mime_data.data('com_data')).decode("utf8")
            data = eval(data)
            idx = data.get('ebs_id')
            if idx is not None:
                item: YkGraphicsItem = self.get_main_window().all_comps[f"Comp{idx}"]()
                item.setPos(event.pos() - pos)  # event.pos()是鼠标在view中的坐标，减去pos则为鼠标在scene中的坐标
                self.scene().addItem(item)
                item.setFocus(Qt.MouseFocusReason)
        elif mime_data.hasFormat('text/plain'):  # 说明拖放的是一个参数对象
            obj = None
            try:
                obj = eval(mime_data.text())
            except:
                pass
            if obj is not None:
                if obj.get("cls") == "YkItem":  # 拖入某个参数时，显示参数的值
                    value = obj.get("value") or '####'
                    item: TextItem = TextItem(value)
                    item.setPos(event.pos() - pos)
                    self.scene().addItem(item)
                    item.setFocus(Qt.MouseFocusReason)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """
        视图的键盘响应函数

        :param event:
        :return:
        """
        if self.scene().focusItem() is None:  # 如果没有选中图元，则执行视图缩放
            if event.key() == Qt.Key_Left:
                self.scale(1.2, 1.2)
            elif event.key() == Qt.Key_Right:
                self.scale(1 / 1.2, 1 / 1.2)
            elif event.key() == Qt.Key_Up:
                self.rotate(30)
            elif event.key() == Qt.Key_Down:
                self.rotate(-30)
            elif event.key() == Qt.Key_F5:
                self.repaint()
                self.update()
        super(YkGraphicsView, self).keyPressEvent(event)  # 执行后，场景按键事件才会触发

    def get_main_window(self, widget=None):
        from yangke.ebsilon.ALPHA import MainWindow
        if widget is None:
            widget = self
        if self.main_window is not None:
            return self.main_window
        else:
            _ = widget
            while _.parentWidget() is not None:
                _ = _.parentWidget()
                if isinstance(_, YkWindow):
                    # noinspection all
                    self.main_window: MainWindow = _
                    return _

        logger.debug("未找到YkGraphicsView的父窗口")

    def scene(self) -> YkGraphicsScene | QGraphicsScene:
        return super(YkGraphicsView, self).scene()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        """
        视图的右键菜单

        :param event:
        :return:
        """
        logger.debug("mouse press event from View")
        if event.button() == Qt.RightButton:
            if self.scene().state != "绘制管道":
                menu = QMenu()
                move_action = QAction("隐藏背景网格")
                act_action = QAction("隐藏坐标系")
                menu.addAction(move_action)
                menu.addAction(act_action)
                # selected_action = menu.exec(event.screenPos())
                # if selected_action == move_action:
                #     self.get_main_window().content_widget.scene.hide_grid()
            # self.scene().state = "常规"  # 重置state的操作在scene的鼠标事件中操作

        super(YkGraphicsView, self).mousePressEvent(event)

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:
        super(YkGraphicsView, self).paintEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        # 任何情况下，在软件绘图界面中移动鼠标，都会触发该事件，如果在该方法中打印信息，会导致界面卡死，在该方法中进行的操作尽量控制操作频率不要太高。
        # logger.debug("mouse move event from YkGraphicsView")
        if self.scene().state == "绘制管道":
            self.viewport().setCursor(Qt.CrossCursor)
        else:
            self.viewport().setCursor(Qt.ArrowCursor)

        super(YkGraphicsView, self).mouseMoveEvent(event)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        """
        鼠标滚轮缩放事件

        :param event:
        :return:
        """
        # if event.angleDelta().y() > 0.5:  # 滚轮缩放与滚动条上下移动功能冲突，已删除
        #     self.scale(1.2, 1.2)
        # else:
        #     self.scale(1 / 1.2, 1 / 1.2)
        super(YkGraphicsView, self).wheelEvent(event)


def over_defined(set_var: list):
    """
    判断传入的列表中的参数是否过定义，如果过定义，返回过定义的参数列表，否则返回False
    """
    set_var_def = []
    for var in set_var:
        var: dict
        for k, v in var.items():
            if not hasattr(v, "derived") or not v.derived:
                if v in set_var_def:
                    return [v]
                else:
                    set_var_def.append(k)

    if "P" in set_var_def and "T" in set_var_def and "H" in set_var_def:
        return ["焓"]
    return None


class TextItem(YkGraphicsItem, QGraphicsTextItem):
    def __init__(self, text):
        """
        文本图元
        """
        super().__init__()
        self.NAME = "文本"
        self.EBS_ID = "25001"
        self.EBS_NAME = "Text Field"
        self.id = 1  # 场景中的组件编号，是个变量
        self.EBS_TYPE = "Edit text fields"
        self.text = text
        self.height = 20
        self.width = 60
        # TextItem的计算必须放在所有组件计算完成之后
        self.cal_order = 2  # 默认的计算序列是0，表示首先计算，计算序列取值越大，计算越靠后
        self.setZValue(2)

    def calculate(self, step=None):
        pass

    def spread_values(self, step=None, symbols=None):
        pass

    def paint(self, painter: QtGui.QPainter, option: QStyleOptionGraphicsItem,
              widget: typing.Optional[QWidget] = ...) -> None:
        painter.save()
        painter.drawText(QPointF(0, 0), self.text)
        super().paint(painter, option, widget)
        painter.restore()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            if self.textInteractionFlags() == Qt.TextEditorInteraction:  # 如果是可编辑状态，则相应鼠标事件
                super().mousePressEvent(event)
            else:
                self.setFocus(Qt.MouseFocusReason)
                self.setSelected(True)
        else:
            super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        if event.button() == Qt.LeftButton:
            self.setTextInteractionFlags(Qt.TextEditorInteraction)
            self.setFocus()
            super().mouseDoubleClickEvent(event)


class PipeItem(YkGraphicsItem):
    def __init__(self, fluid_type="Steam"):
        """
        管线的位置是管线起点的位置

        :param fluid_type:
        """
        super(PipeItem, self).__init__()

        self.connect_items = ConnectItems()

        self.NAME = "流"
        self.EBS_ID = "-100"
        self.EBS_NAME = fluid_type
        self.id = 1  # 场景中的组件编号，是个变量
        self.EBS_TYPE = "Edit streams"
        self.control_points = []  # 管线的图元坐标，[QPointF()]
        self.setZValue(管线图层id)  # 管线的图层为-1

        self.init_preferred_color()

        self.pen[1].setColor(Qt.black)  # 绘制管线上的点的画笔
        self.pen[1].setWidth(8)

        self.pen[2].setWidth(self.SELECTION_HANDLE_SIZE)  # 绘制管线两个端点的画笔

        self.icon = QIcon(os.path.join(os.path.dirname(__file__), "UI", "resource", "flow_pipe.png"))
        self.emphasize = False
        self.SpecificationValues = {
            "管线参数请查看结果页": [
            ],
        }
        self.Result = {
            "常规": [
                ["压力", "P", "", Pressure("MPa"), "disabled"],
                ["温度", "T", "", Temperature("℃"), "disabled"],
                ["焓", "H", "", Enthalpy("kJ/kg"), "disabled"],
                ["质量流量", "M", "", MassFlow("t/h"), "disabled"],
            ]
        }

    def get_connect_items(self):
        """
        获取管线连接的组件的信息。示例：
        [{"item": YkGraphicsItem(), "port_idx": 1}]

        :return:
        """
        return self.connect_items

    def update_line(self, vectors_scene=None, vectors_item=None):
        """

        :param vectors_scene: 控制点在场景中的坐标 ["point": QPointF(), "point": QPointF]
        :param vectors_item: 控制点的图元坐标 [QPointF(), QPointF()]
        :return:
        """
        if vectors_scene is not None:
            if len(vectors_scene) > 1 and isinstance(vectors_scene[0], QPointF):
                scene_points = vectors_scene
            else:
                scene_points = [i.get("point") for i in vectors_scene]
            self.control_points = [self.mapFromScene(p) for p in scene_points]  # 场景坐标转换为图元坐标
        else:
            self.control_points = vectors_item
        top_left = QPointF(0, 0)
        bottom_right = QPointF(0, 0)
        if len(self.control_points) >= 2:
            for p in self.control_points:
                if top_left.x() > p.x():
                    top_left.setX(p.x())
                if top_left.y() > p.y():
                    top_left.setY(p.y())
                if bottom_right.x() < p.x():
                    bottom_right.setX(p.x())
                if bottom_right.y() < p.y():
                    bottom_right.setY(p.y())
        pen_width = QPointF(self.pen[0].width() / 2, self.pen[0].width() / 2)
        self.bounding = QRectF(top_left - pen_width, bottom_right + pen_width)
        self.update()
        self.moveBy(0, 1)  # 移动操作可以刷新组件的边框，否则边框更新不完全，导致点击事件和边框不匹配
        self.moveBy(0, -1)

    def remove_control_point(self, idx):
        """
        移除管线上的某个控制点

        :param idx:
        :return:
        """
        # 首先判断删除的电上是否连接这其他组件
        for ci in self.connect_items:
            ci: ConnectItem
            if ci.point_id == idx:
                logger.debug(f"删除的控制点上连接着其他设备组件S{ci.item_sid}，请先删除设备组件！")
                return

        # 删除控制点后，其他控制点在control_points中的索引会发生变化，这里需要更新
        for ci in self.connect_items:
            _ci_pid = ci.point_id
            if _ci_pid < idx or _ci_pid == -1:
                continue
            else:
                ci.point_id = _ci_pid - 1  # 删除点以后的点的索引值减1

        # 最后，从控制点中删除指定的点，并刷新管线
        self.control_points.pop(idx)
        self.update_line(vectors_item=self.control_points)

    def paint(self, painter: QtGui.QPainter, option: QStyleOptionGraphicsItem,
              widget: typing.Optional[QWidget] = ...) -> None:
        painter.save()
        lines = []
        if self.control_points is None:
            return
        for i in range(len(self.control_points) - 1):
            line = QLineF(self.control_points[i], self.control_points[i + 1])
            lines.append(line)
        if self.emphasize:  # 如果管线处于强调状态，如端点吸附时
            self.pen[0].setWidth(self.pen_width * 2)
        else:
            self.pen[0].setWidth(self.pen_width)

        painter.setPen(self.pen[0])
        painter.drawLines(lines)
        if self.isSelected() or self.hasFocus():
            painter.setPen(self.pen[4])
            painter.drawRect(self.bounding)

            painter.setPen(self.pen[1])
            painter.drawPoints(self.control_points)

        # 根据管线连接点的类型，按不同颜色绘制端点，Inlet为灰色，Outlet为黑色
        if len(self.connect_items) >= 1:
            connect_item: ConnectItem = self.connect_items[0]
            _scene_id = connect_item.item_sid
            _port = connect_item.port_id
            if self.scene().items_scene_id.get(_scene_id) is None:  # 在删除组件时，组件可能删除了，但该方法还是会执行一次
                self.pen[2].setColor(Qt.gray)
            elif self.scene().items_scene_id.get(_scene_id).ports.get(_port).type1 == "Inlet":
                self.pen[2].setColor(Qt.gray)
            elif self.scene().items_scene_id.get(_scene_id).ports.get(_port).type1 == "Outlet":
                self.pen[2].setColor(Qt.black)
            elif self.scene().items_scene_id.get(_scene_id).ports.get(_port).type1 == "Set Value":
                self.pen[2].setColor(Qt.green)
            painter.setPen(self.pen[2])
            if len(self.control_points) >= 1:
                painter.drawPoint(self.control_points[0])
                if len(self.control_points) >= 2:
                    painter.drawPoint(self.control_points[-1])
        painter.restore()

    def move_point(self, idx, pos):
        """
        将管线中某个点移动到指定位置

        :param idx: 点的索引
        :param pos: 点在场景中的坐标
        :return:
        """
        points_scene = [self.mapToScene(p) for p in self.control_points]  # 将图元坐标转换为场景坐标
        if len(points_scene) == 0:
            return
        points_scene[idx] = pos  # 将指定点移动到指定位置
        self.setPos(points_scene[0])  # 先移动管线的位置，在更新管线在场景中的坐标，管线的位置即为场景中第一个点的位置
        self.update_line(points_scene)

    def get_connect_point_ids(self, need_port_type=False):
        """
        获取管线中与设备组件端口连接的点的id列表

        :param need_port_type: 是否按端口类型返回列表，如果为True，则返回五个列表，分别对应Inlet、Outlet、Set Value、LoginIn和LogicOut五类端口
        :return:
        """
        if need_port_type:
            input_ids = []
            output_ids = []
            set_ids = []
            logic_in_ids = []
            logic_out_ids = []
            for ci in self.connect_items:
                ci: ConnectItem
                _pid = ci.point_id
                if _pid == -1:
                    _pid = len(self.control_points) - 1
                port: Port = self.scene().items_scene_id.get(ci.item_sid).ports[ci.port_id]
                if port.type1 == "Inlet":
                    input_ids.append(_pid)
                elif port.type1 == "Outlet":
                    output_ids.append(_pid)
                elif port.type1 == "Set Value":
                    set_ids.append(_pid)
                elif port.type1 == "Signal Inlet":
                    logic_in_ids.append(_pid)
                elif port.type1 == "Signal Outlet":
                    logic_out_ids.append(_pid)
            return input_ids, output_ids, set_ids, logic_in_ids, logic_out_ids
        else:
            port_ids = []
            for ci in self.connect_items:
                port_ids.append(ci.point_id)
            return port_ids

    def get_connect_item_by_point_id(self, pid):
        """
        获取与管线某点连接的设备图元项

        :param pid:
        :return:
        """
        for ci in self.connect_items:  # 移动与管线连接的Set Value端口所属的组件图元
            ci: ConnectItem
            if ci.point_id == pid:
                item: YkGraphicsItem = self.scene().items_scene_id.get(ci.item_sid)
                return item

        return None

    def get_connect_components(self):
        """
        获取当前管线连接的组件列表
        """
        items = []
        for ci in self.connect_items:
            ci: ConnectItem
            if ci.get_port_type(self.scene()) is not None:
                item: YkGraphicsItem = self.scene().items_scene_id.get(ci.item_sid)
                items.append(item)
        return items

    def mouseDoubleClickEvent(self, event):
        print("double click from pipe item")
        super().mouseDoubleClickEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """
        只移动除锚点外的其他点，也就是管线Item的位置不变

        :param event:
        :return:
        """
        try:
            print("mouse move event from PipeItem")
            if not hasattr(self, "moving_point"):  # 如果没有moving_point属性，则说明不是移动管线操作
                ...
            elif self.moving_point is not None:  # 说明在移动管线上的某个点
                # 这里的坐标从event.pos()修改为self.mapFromScene(event.scenePos())，否则PyQt6中的event.pos()总是(0,0)
                # self.control_points[self.moving_point] = event.pos()
                self.control_points[self.moving_point] = self.mapFromScene(event.scenePos())
                self.update_line(vectors_item=self.control_points)
            else:  # 说明移动的是整条管线
                if self.move_start_pos is None:
                    return

                # -------------------------------移动管线时，与Inlet等端口连接的点不移动 ---------------------------------
                pos = event.scenePos()
                dp = pos - self.move_start_pos  # 计算鼠标拖动的相对位移
                temp_control_points = []
                pids1, pids2, pids3, sig_in, sig_out = self.get_connect_point_ids(need_port_type=True)
                pids1.extend(pids2)  # Inlet和Outlet类型的端口位置在移动管线时保持不变
                pids1 = pids1 + sig_in + sig_out  # Signal Inlet和Signal Outlet类型的端口位置在移动管线时保持不变
                for i, p in enumerate(self._move_start_vectors):  # 移动开始时，管线的初始坐标
                    # 检查点是否连接着某个组件
                    if i in pids1:
                        temp_control_points.append(p)
                    else:
                        temp_control_points.append(p + dp)
                self.update_line(vectors_item=temp_control_points)
                # -------------------------------移动管线时，与Inlet等端口连接的点不移动 ---------------------------------

                # ----------------------------移动管线时，与Set Value等端口连接的点对应的图元位置也要移动------------------
                for ci in self.connect_items:  # 移动与管线连接的Set Value端口所属的组件图元
                    ci: ConnectItem
                    item: YkGraphicsItem = self.scene().items_scene_id.get(ci.item_sid)
                    port = item.ports[ci.port_id]
                    if port.type1 == "Set Value":
                        port_in_item_point = port.point
                        pid = ci.point_id
                        port_new_point = self.mapToScene(temp_control_points[pid])
                        item.setPos(port_new_point.x() - port_in_item_point.x(),
                                    port_new_point.y() - port_in_item_point.y())
                # ----------------------------移动管线时，与Set Value等端口连接的点对应的图元位置也要移动------------------

        except:
            traceback.print_exc()

    def boundingRect(self) -> QRectF:
        return self.bounding  # 这里必须覆盖父类的boundingRect方法，因为父类的bounding是随width和height变化的

    def mouseReleaseEvent(self, event: 'QGraphicsSceneMouseEvent') -> None:
        self.move_start_pos = None
        self.moving_point = None
        super(PipeItem, self).mouseReleaseEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        """

        :param event:
        :return:
        """
        print("mouse press from PipeItem")

        self.scene().flag_item.selected_item = None
        if event.button() == Qt.LeftButton:
            idx = points_contains(self.control_points, self.mapFromScene(event.scenePos()), tolerance=self.pen_width)
            if idx >= 0:  # 如果鼠标在管线上的某个锚点按下，则移动该锚点
                self.moving_point = idx  # 记录锚点的索引
                self.clearFocus()
                self.scene().views()[0].viewport().setCursor(Qt.CrossCursor)
                # event.accept()
                self._move_start_vectors = self.control_points
                # self.setAcceptedMouseButtons(Qt.LeftButton)
                self.setSelected(True)
                self.focusItem()

            if self.contains_point(event.scenePos()):
                self._move_start_vectors = self.control_points
                super(PipeItem, self).mousePressEvent(event)
            else:  # 点击到了管线区域，但未点击到管线线段上
                self.clearFocus()
                self.setSelected(False)
                self.scene().flag_item.selected_item = self
        super(PipeItem, self).mousePressEvent(event)

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        """
        item的键盘响应函数

        :param event:
        :return:
        """
        # 先断开与当前管道连接的其他设备组件的端口
        super(PipeItem, self).keyPressEvent(event)

    def contains_point(self, pos_scene):
        """
        判断指定位置是否位于管线上

        :param pos_scene: 场景上的坐标点
        :return:
        """
        pos = self.mapFromScene(pos_scene)
        for i in range(len(self.control_points) - 1):
            point1 = self.control_points[i]
            point2 = self.control_points[i + 1]
            line = Line(point1=[point1.x(), point1.y()], point2=[point2.x(), point2.y()])
            distance = line.distance([pos.x(), pos.y()])
            if distance < 6:
                return True
        return False

    def calculate(self, step=None):
        """
        管线至少需要计算P、T、H、F四个参数。
        从管线的所有连接端口上获取参数，从端口到管线的参数传递是区分result和values的，在管线计算中判断是否过定义或欠定义。并将计算结果也按
        照values.values和values.result写回管线上的端口，下一个组件计算时，也可以从新端口上获取参数判断是否过定义或欠定义。但计算过的组件
        不能再次计算，否则因为计算过的组件上的values.values参数已经传递过，会误判为过定义。
        """
        # 从管线的所有连接端口上获取参数
        set_var = []
        if step >= 1:
            self.values.values_steps[step] = self.values.values_steps[step - 1].copy()  # 当前时间步的初始值为上一个时间步的值
            self.values.values = self.values.values_steps[step]
        for connect_item in self.connect_items:
            connect_item: ConnectItem
            item_scene_id = connect_item.item_sid
            port_idx = connect_item.port_id
            item = self.scene().items_scene_id.get(item_scene_id)
            port = item.ports.get(port_idx)

            # 组件之间的过定义只在PipeItem上进行判断，组件内部的过定义由组件负责
            # 因此其他组件上不需要如下的过定义判断
            # 在第一个计算步判断是否过定义
            if step == 1:
                # port.values的第0步永远没有参数，只有组件的第0步才有设置信息
                # set_var.append(port.values.get_initial(need_unit=True, with_none=False))  # 将第0步中已定义的参数添加到set_var中
                set_var.append(port.values.get_values_of_step(step=1, need_unit=True, with_none=False))

            self.values.update(step=step, values=port.values, set_none=False)  #

        if step == 1:  # 只在第一个迭代步对过定义进行判断
            _ = over_defined(set_var)
            if _ is not None:
                return f"Error: 场景ID为{self.scene_id}的组件过定义！{_} --- break"  # --- break会通知外部计算循环直接退出

        P = self.get("P", need_unit=True)  # 管线上不能设置参数，因此从结果中获取参数
        T = self.get("T", need_unit=True)
        H = self.get("H", need_unit=True)
        M = self.get("M", need_unit=True)

        # 判断P、T、H、M是否为数值
        try:
            if P is not None:
                var = "P"
                _ = float(P.value)
            if T is not None:
                var = "T"
                _ = float(T.value)
            if H is not None:
                var = "H"
                _ = float(H.value)
            if M is not None:
                var = "M"
                _ = float(M.value)
        except ValueError:
            return f"Error: {self.scene_id}号组件参数{var}取值错误，无法转换为数值！--- break"

        # 校验P、T、H、M四个参数是否满足计算要求
        # 首先检测质量流量是否存在
        if M is None:
            return f"unfinished: {self.scene_id}号组件缺少质量流量！"

        # 其次检测是否焓值过定义或欠定义
        suc, msg = validate_water_parameters(p=P, t=T, h=H)  # 压力和温度不一定能确定水蒸汽状态，如湿蒸汽，则需要湿度或焓值等参数
        if suc:
            ...
        else:
            return f"Error: {msg}"

        if P is not None and T is not None:
            H = get_h_by_pt(P, T)
            H = Value(H, "kJ/kg")
            H.derived = True
            self.values.update({"H": H}, step=step)
        elif P is not None and H is not None:
            T = get_t_by_hp(H, P)
            T = Value(T, "℃")
            T.derived = True
            self.values.update({"T": T}, step=step)
        elif T is not None and H is not None:
            P = get_p_by_th(T, H)
            P = Value(P, "MPa")
            P.derived = True
            self.values.update({"P": P}, step=step)

        return "done"

    def spread_values(self, step=None, symbols=None):
        """
        将管线上的参数传递给管线连接的端口，空值也会传递，如果是端口向管线传递数据，则空值不会传递

        :return:
        """
        # super().spread_values(step=step, symbols=["P", "T", "H", "M", "NCV"])  # 不能调用父组件的值，因为自己是管道，没有ports属性
        for ci in self.connect_items:
            ci: ConnectItem
            item = self.scene().items_scene_id.get(ci.item_sid)
            port = item.ports.get(ci.port_id)

            # 管线上的所有参数都传递给其两个端口，这里不能设置set_none为True，否则会导致多个组件计算的空值覆盖已有值
            # 如果要清空端口上保存的计算数据或设置数据，需要在计算开始前由主程序负责清空
            # 因为面板至后台数据保存时调用了update(set_none=True)不在调用本方法。
            port.values.update(step=step, values=self.values, set_none=False)

    def get_unconnected_points(self):
        """
        获取管线上未连接组件的端口的图元坐标，以及点在管线上control_points中的编号
        """
        if len(self.connect_items) == 0:  # 没有连接点，说明首尾两个端点都未连接组件
            if len(self.control_points) <= 2:
                return self.control_points, [0, -1]
            else:
                return [self.control_points[0], self.control_points[-1]], [0, -1]
        else:
            unconnect_points_index = [0, -1]
            # [{"item": YkGraphicsItem().scene_id, "port_id": 1, "point_id": 0}]
            for _ci in self.connect_items:
                _ci: ConnectItem
                if _ci.point_id == 0:
                    unconnect_points_index.remove(0)
                elif _ci.point_id == -1:
                    unconnect_points_index.remove(-1)
                elif _ci.point_id == len(self.control_points) - 1:
                    unconnect_points_index.remove(-1)
            unconnect_points = [self.control_points[i] for i in unconnect_points_index]
            return unconnect_points, unconnect_points_index

    def get_input_output_type(self):
        """
        判断管线是进口还是出口连接，如果只连接一个端口，则返回连接的端口进口还是出口类型，如果两个端口都连接或都未连接，则返回空，如果只连接了
        Set Value这类端口，则返回空
        """
        if len(self.connect_items) == 0:
            return None
        else:
            for _ci in self.connect_items:
                _ci: ConnectItem
                item: YkGraphicsItem = self.scene().items_scene_id.get(_ci.item_sid)
                port = item.ports.get(_ci.port_id)
                if port.type1 in ["Inlet", "Outlet", "Signal Inlet", "Signal Outlet"]:
                    return port.type1
            return None

    def distance_to_point(self, pos):
        """
        管线距离点的最近的距离，返回管线上最近距离的点的坐标及距离

        :param pos:
        :return: distance, p, line_idx
        """
        from yangke.base import Line
        control_points = [self.mapToScene(p) for p in self.control_points]
        distance = 10000
        p = None
        line_idx = 0
        for i in range(len(control_points) - 1):
            p1, p2 = control_points[i], control_points[i + 1]
            line = Line(point1=(p1.x(), p1.y()), point2=(p2.x(), p2.y()))
            _distance, _p = line.distance(point=(pos.x(), pos.y()), need_project_point=True)
            if _distance < distance:
                if line.contains_point(_p, as_line_segment=True):
                    distance = _distance
                    p = QPointF(_p[0], _p[1])
                    line_idx = i
        return distance, p, line_idx

    def set_color(self, color, index=0):
        """
        设置画笔的颜色
        """
        if isinstance(color, list):
            for i, c in enumerate(color):
                self.set_color(c, i)
        else:
            self.pen[index].setColor(color)

    def set_width(self, widths, index=0):
        """
        设置画笔的宽度
        """
        if isinstance(widths, list):
            for i, w in enumerate(widths):
                self.set_width(w, i)
        else:
            self.pen[index].setWidth(widths)

    def set_connect_items(self, connect_items):
        self.connect_items = connect_items

    def init_preferred_color(self, color=None):
        """
        设置管线的颜色
        """
        if color is None:
            if self.EBS_NAME == "Steam":
                color = Qt.red
                self.pen_width = 4
                self.pen[0].setWidth(self.pen_width)
            elif self.EBS_NAME == "Logic":
                color = Qt.black
                self.pen_width = 2
                self.pen[0].setWidth(self.pen_width)
            elif self.EBS_NAME == "Water":
                color = QColor("#0000f7")
                self.pen_width = 4
                self.pen[0].setWidth(self.pen_width)
            elif self.EBS_NAME == "Air":
                color = Qt.yellow
                self.pen_width = 4
                self.pen[0].setWidth(self.pen_width)
            elif self.EBS_NAME == "Flue":
                color = QColor("#7b0000")
                self.pen_width = 4
                self.pen[0].setWidth(self.pen_width)
            elif self.EBS_NAME == "Shaft":
                color = QColor("#007b00")
                self.pen_width = 4
                self.pen[0].setWidth(self.pen_width)
        self.color = color
        try:
            self.pen[0].setColor(color)
        except TypeError:
            logger.warning(f"颜色初始化失败！{color=} 并且 {self.EBS_NAME=}")


class CoordinateItem(QGraphicsItem):
    """
    视图窗口中，场景坐标的坐标系
    """

    def __init__(self):
        self.brush_color = QColor(0, 0, 255, 100)
        self.pen = QPen()
        self.pen.setWidth(2)
        self.icon = QIcon(os.path.join(os.path.dirname(__file__), "UI", "resource", "coor.png"))
        super(CoordinateItem, self).__init__()
        self.NAME = "COORDINATE"
        self.EBS_ID = None
        self.EBS_NAME = None
        self.EBS_TYPE = None
        self.id = 1
        self.scene_id = None
        self.setZValue(背景图层id)

    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, 1, 1)

    def set_scene_id(self, scene_id):
        self.scene_id = scene_id

    def paint(self, painter: QtGui.QPainter, option: QStyleOptionGraphicsItem,
              widget: typing.Optional[QWidget] = ...) -> None:
        painter.save()
        painter.setPen(self.pen)
        painter.setBrush(self.brush_color)
        painter.drawPoint(QPointF(0, 0))
        painter.drawLine(QLineF(0, 0, 30, 0))
        painter.drawLine(QLineF(0, 0, 0, 30))
        painter.drawText(QPointF(32, 5), "X")
        painter.drawText(QPointF(-3, 40), "Y")
        painter.restore()


class SceneFlagItem(YkGraphicsItem):
    def __init__(self):
        """
        用于在场景中显示临时效果，如强调的圆圈，点等，场景中只能有一个该Item
        """
        super(SceneFlagItem, self).__init__()
        self.NAME = "Flag"
        self.EBS_ID = None
        self.EBS_NAME = None
        self.EBS_TYPE = None
        self.id = 1
        self.scene_id = -1
        self.bounding = QRectF(0, 0, 0, 0)  # x,y,w,h
        self.ui = None
        self.selected_item = None  # 当前选中的组件，在管线选择是需要使用该参数判断重叠管线的选择情况

    def boundingRect(self) -> QRectF:
        return self.bounding

    def paint(self, painter: QtGui.QPainter, option: QStyleOptionGraphicsItem,
              widget: typing.Optional[QWidget] = ...) -> None:
        self.pen[0].setColor(Qt.blue)
        self.pen[0].setWidth(self.SELECTION_HANDLE_SIZE * 3)
        painter.setPen(self.pen[0])
        if self.ui is None and self.isVisible():
            self.hide()
        else:
            if isinstance(self.ui, QRect) or isinstance(self.ui, QRectF):
                painter.drawRect(self.ui)  # //绘制边框
                self.height = self.ui.height() + self.pen_width
                self.width = self.ui.width() + self.pen_width
            elif isinstance(self.ui, QPoint) or isinstance(self.ui, QPointF):
                painter.drawPoint(self.ui)
                self.width = self.pen_width
                self.height = self.pen_width
            elif isinstance(self.ui, dict):
                if self.ui.get("type") == 'circle':
                    # 绘制圆
                    ...
            if not self.isVisible():
                self.show()

    def draw_ui(self, ui):
        """
        在场景中显示该组件，ui可以取QPointF、QRect等对象
        """
        self.ui = ui
        if ui is not None:
            if not self.isVisible():
                self.show()
        else:
            if self.isVisible():
                self.hide()


class SceneGridItem(QGraphicsItem):
    def __init__(self, bounding):
        """
        视图窗口中，场景的边框及网格线
        :param bounding:
        """
        super(SceneGridItem, self).__init__()
        self.bounding = bounding or QRectF(0, 0, 800, 600)
        self.icon = QIcon(os.path.join(os.path.dirname(__file__), "UI", "resource", "网格.png"))
        self.NAME = "MESH"
        self.id = 1
        self.scene_id = 0
        self.setZValue(背景图层id)

    def boundingRect(self) -> QRectF:
        return self.bounding

    def set_scene_id(self, scene_id):
        self.scene_id = scene_id

    def paint(self, painter: QtGui.QPainter, option: QStyleOptionGraphicsItem,
              widget: typing.Optional[QWidget] = ...) -> None:
        bound_pen = QPen(QColor(Qt.blue))
        bound_pen.setStyle(Qt.DashLine)
        painter.setPen(bound_pen)
        painter.drawRect(self.bounding)  # //绘制边框


class YkStyledItemDelegate(QStyledItemDelegate):
    def __init__(self):
        """
        【所有组件】面板中所有组件的显示方式
        """
        super(YkStyledItemDelegate, self).__init__()
        self.width = 275
        self.height = 40

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        if index.isValid():
            painter.save()
            user_data = index.data(Qt.UserRole)
            type_com = user_data.get("type")  # 组件的类型
            ebs_name = user_data.get("ebs_name") or ""
            idx = user_data.get("ebs_id") or "888"  # 组件在Ebsilon中的id
            name = index.data()
            icon = index.data(Qt.DecorationRole)
            rect = QRectF()
            rect.setX(option.rect.x())
            rect.setY(option.rect.y())
            rect.setWidth(self.width - 1)
            rect.setHeight(self.height - 1)

            # 绘制圆角矩形
            radius = 7
            path: QPainterPath = QPainterPath()
            path.moveTo(rect.topRight() - QPointF(radius, 0))
            path.lineTo(rect.topLeft() + QPointF(radius, 0))
            path.quadTo(rect.topLeft(), rect.topLeft() + QPointF(0, radius))
            path.lineTo(rect.bottomLeft() + QPointF(0, -radius))
            path.quadTo(rect.bottomLeft(), rect.bottomLeft() + QPointF(radius, 0))
            path.lineTo(rect.bottomRight() - QPointF(radius, 0))
            path.quadTo(rect.bottomRight(), rect.bottomRight() + QPointF(0, -radius))
            path.lineTo(rect.topRight() + QPointF(0, radius))  # 8
            path.quadTo(rect.topRight(), rect.topRight() + QPointF(-radius, -0))

            # 绘制数据位置
            icon_rect = QRect(int(rect.left() + 5), int(rect.top() + 5), 30, 30)  # 图标所在的区域
            name_rect = QRect(int(rect.left() + 50), int(rect.top() + 5), int(rect.width() - 30), 20)  # 中文组件名所在的区域
            ebs_name_rect = QRect(int(rect.left() + 50), int(rect.top() + 22), int(rect.width() - 30), 20)  # 英文组件名
            id_rect = QRect(int(rect.right() - 40), int(rect.bottom() - 25), int(rect.width() - 10), 20)  # EBS_ID

            if option.state & QStyle.State_Selected:
                painter.setPen(QPen(Qt.blue))
                painter.setBrush(QColor(0, 241, 255))
                painter.drawPath(path)
            elif option.state & QStyle.State_MouseOver:
                painter.setPen(QPen(Qt.green))
                painter.setBrush(QColor(229, 241, 255))
                painter.drawPath(path)
                icon_rect = QRect(int(rect.left() + 0), int(rect.top() + 0), 40, 40)
            else:
                painter.setPen(QPen(Qt.gray))
                painter.setBrush(Qt.NoBrush)
                painter.drawPath(path)

            # 绘制组件名
            # painter.drawEllipse(circle)
            painter.setPen(QPen(Qt.black))
            painter.setFont(QFont("Times", 10, QFont.Bold))
            painter.drawText(name_rect, Qt.AlignLeft, name)  # 绘制中文组件名
            painter.drawText(ebs_name_rect, Qt.AlignLeft, ebs_name)  # 绘制英文组件名

            # 绘制右侧的EBS_ID
            painter.setPen(QPen(Qt.black))
            painter.setFont(QFont("Times", 10))
            painter.drawText(id_rect, Qt.AlignLeft, str(idx))

            _ = icon.pixmap(200, 200).toImage()
            painter.drawImage(icon_rect, _)

            painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex):
        return QSize(self.width, self.height)


def pixmap_from_item(item: YkGraphicsItem, keep_ratio=True):
    func = item.boundingRect
    if keep_ratio:
        bounding = item.boundingRect()
        x, y = bounding.x(), bounding.y()
        width, height = bounding.width(), bounding.height()
        if width != height:
            width, height = [max(width, height)] * 2
            item.boundingRect = lambda: QRectF(-width / 2, -height / 2, width, height)

    pixmap = QPixmap(item.boundingRect().size().toSize())
    pixmap.fill(QColor('#FFFFFF'))
    painter = QPainter(pixmap)
    option = QStyleOptionGraphicsItem()
    painter.translate(-1 * (item.boundingRect().topLeft()))
    item.paint(painter, option)
    item.boundingRect = func
    return pixmap


class YkIndexDelegate(QStyledItemDelegate):
    def __init__(self):
        """
        场景面板中组件的显示方式
        """
        super(YkIndexDelegate, self).__init__()
        self.width = 265
        self.height = 40

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        if index.isValid():
            painter.save()

            painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex):
        return QSize(self.width, self.height)


class DisplayPanel(QWidget):
    def __init__(self):
        """
        用于显示组件的信息的面板，可以设置值与读取值

        """
        super().__init__()
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(1)

    def set_values(self, values: dict):
        """
        将values中的数据显示到面板上，如果value为None，则面板不改变，即使是values.result中的数值，也会显示到面板上
        """
        values_bak = copy.deepcopy(values)
        for w in self.get_child_yk_items():
            _var = w.label.text().split("[")[1].replace("]", "").strip()
            val = values_bak.get(_var)
            if val is None:
                ...
            elif isinstance(val, Value):
                if val.value.__class__.__name__ in ["str", "int", "bool", "NoneType"]:
                    w.set_value(f"{val.value}")  # 设置val.value会导致values.values值变化，因为会触发combobox的值改变事件
                    if val.unit is not None:
                        if isinstance(val.unit, str):
                            w.set_unit(val.unit)
                        else:
                            w.set_unit(val.unit.unit)
                elif val.value.__class__.__name__ in ["float"]:
                    w.set_value(f"{val.value:10.5f}")
                    if val.unit is not None:
                        if isinstance(val.unit, str):
                            w.set_unit(val.unit)
                        else:
                            if isinstance(val.unit, dict):
                                pass  # 动态参数时，会在绑定信号槽前设置初始数据，此时单位可能是：{'func': 'dynamic_unit(FL2)'}
                            else:
                                w.set_unit(val.unit.unit)
                else:
                    w.set_value('')
            elif isinstance(val, str):  # "FTYP"等类型参数的值
                w.set_value(val)
            else:
                w.set_value('')

        values = values_bak  # 恢复values的值

    def get_values(self, symbols=None) -> dict:
        """
        从面板上获取指定符号对应的数据，如果不指定symbols，则默认返回当前面板中所有的数据
        """
        res = {}
        for w in self.get_child_yk_items():
            w: YkItem = w
            label, value, unit = w.get_value_and_unit(need_label=True)
            # if value.strip() == "": # 不能略过空值，因为用户可能特意删除某个参数的值
            #     continue
            _var = label.split("[")[1].replace("]", "").strip()
            res.update({_var: Value(value, unit)})  # 空值也会返回
        return res

    def get_child_folder(self):
        """
        获取显示面板中所有的YkFoldableWidget
        """
        res = [i for i in self.children() if isinstance(i, YkFoldableWidget)]
        return res

    def get_child_yk_items(self, symbol=None):
        """
        获取显示面板中所有的YkItem对象
        """
        folder = self.get_child_folder()
        res = []
        for fold in folder:
            w = fold.widget
            _ = [yk_item for yk_item in w.children() if isinstance(yk_item, YkItem)]
            res.extend(_)
        if symbol is None:
            return res
        else:
            for yk_item in res:
                if isinstance(yk_item, YkItem):
                    if f'[{symbol}]' in yk_item.label.text():
                        return yk_item
