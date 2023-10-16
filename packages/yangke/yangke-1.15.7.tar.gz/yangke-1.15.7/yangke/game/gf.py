# game frame
import os.path
import random
import sys
import time

from yangke.common.win.win_x64 import (find_window, capture_pic_undecorated, post_key, do_click,
                                       get_size_of_window, find_pic)
from yangke.objDetect.ocr import ocr
from yangke.base import show_pic, get_pic_size, is_number, draw_element_on_pic, get_draw_element_on_pic_handle
from yangke.common.config import logger
from yangke.common.win.dminput import DM, DMRemote
import cv2


class RectRegion:
    def __init__(self, center=None, left=None, right=None, top=None, bottom=None):
        """
        长方形区域，由上下左右四条边限定的长方形区域，区域位置为区域的中心点
        """
        self.center = center
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    def set_xyxy(self, x1, y1, x2, y2):
        self.left = x1
        self.right = x2
        self.top = y1
        self.bottom = y2
        return self

    def x1(self):
        return self.left

    def y1(self):
        return self.top

    def x2(self):
        return self.right

    def y2(self):
        return self.bottom

    def transfer_to_positive(self, width, height):
        """
        将负数表示的坐标转换成正数，负数表示点距离最大值的距离
        """
        self.right = self.right + width if self.right < 0 else self.right
        self.left = self.left + width if self.left < 0 else self.left
        self.top = self.top + height if self.top < 0 else self.top
        self.bottom = self.bottom + height if self.bottom < 0 else self.bottom
        return self.left, self.top, self.right, self.bottom

    def w(self):
        assert self.right > 0 and self.left > 0, "坐标值必须为正才可使用w()方法获取区域宽度"
        return self.right - self.left

    def h(self):
        assert self.right > 0 and self.left > 0, "坐标值必须为正才可使用h()方法获取区域高度"
        return self.bottom - self.top

    def set_xywh(self, x1, y1, w, h):
        self.left = x1
        self.top = y1
        self.right = self.left + w
        self.bottom = self.top + h
        return self

    def get_xyxy(self):
        return self.left, self.top, self.right, self.bottom

    def get_xywh(self):
        return self.left, self.top, self.right - self.left, self.bottom - self.top

    def get_center(self):
        return int((self.left + self.right) / 2), int((self.top + self.bottom) / 2)

    def get_sub_pos(self, start, end, length, axis=0):
        """
        获取Position的子位置

        :param start: 子位置开始的索引
        :param end: 子位置结束的索引
        :param length: 当前位置的长度
        :param axis: 获取子位置的方向
        """
        if axis == 0:
            sep = (self.right - self.left) / length
            return RectRegion().set_xyxy(self.left + sep * start, self.top, self.left + sep * end, self.bottom)


class Map:
    def __init__(self):
        ...


class Chat:
    def __init__(self, region, channels=None):
        """
        聊天面板
        :param region: 聊天面板的区域
        :param channels: 聊天频道列表
        """
        self.region = region
        self.channels = channels


class TimePanel:
    def __init__(self, region, frame: "Frame"):
        self.region = region
        self.frame = frame

    def get_time(self):
        return self.frame.get_text(self.region)


class Task:
    def __init__(self, region_xyxy=None, frame: "Frame" = None):
        self.region_xyxy = region_xyxy  # (x1, y1, x2, y2)
        self.frame: "Frame" | None = frame

    def get_task_text(self, frame: "Frame" = None):
        self.frame = frame or self.frame
        snapshot = self.frame.capture_window_xyxy(*self.region_xyxy)
        text = ocr(snapshot, paragraph=True)
        return text

    def get_text_link_pos_global(self, text: str):
        """
        获取任务面板上指定文字在整个画面上的坐标位置
        """
        snapshot = self.frame.capture_window_xyxy(*self.region_xyxy)
        texts = ocr(snapshot, paragraph=False)
        pos_rel = RectRegion()
        for res in texts:
            p_left_top, p_right_top, p_right_bottom, p_left_bottom = res[0]
            text_, probability = res[1]
            if text in text_:
                pos = RectRegion().set_xyxy(p_left_top[0], p_left_top[1], p_right_bottom[0], p_right_bottom[1])
                start = text_.index(text)
                end = start + len(text)
                pos_rel = pos.get_sub_pos(start, end, len(text_))
                break

        pos_global = self.to_global(pos_rel)
        return pos_global

    def set_frame(self, frame: "Frame"):
        self.frame = frame or self.frame

    def to_global(self, pos_rel: RectRegion | None = None):
        x1, y1, x2, y2 = pos_rel.left, pos_rel.top, pos_rel.right, pos_rel.bottom
        x_offset = self.region_xyxy[0]
        y_offset = self.region_xyxy[1]
        pos_global = RectRegion().set_xyxy(x1 + x_offset, y1 + y_offset, x2 + x_offset, y2 + y_offset)
        return pos_global


class AnchorRegion:
    def __init__(self, x1, y1, x2, y2):
        """
        根据锚点确定的区域类
        示例：
        AnchorRegion("anchor.x1+100", "anchor.y1-10", 200, 400)
        """
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.anchor_region: list | tuple | None = None  # 如果是list，表示有多个anchor对象，如果是tuple，表示是一个anchor对象的四个坐标xyxy

    def get_region(self, anchor_region, window_size):
        """
        根据参考点坐标及窗口大小获取AnchorRegion的区域
        可以有多个参考点坐标，此时anchor_region为列表[(x1, y1, x2, y2), (x3, y3, x4, y4)]


        """
        self.anchor_region = anchor_region
        if isinstance(self.x1, str):
            self.x1 = int(self.parse_pos(self.x1))
        if isinstance(self.x2, str):
            self.x2 = int(self.parse_pos(self.x2))
        if isinstance(self.y1, str):
            self.y1 = int(self.parse_pos(self.y1))
        if isinstance(self.y2, str):
            self.y2 = int(self.parse_pos(self.y2))

        if self.x1 < 0:
            self.x1 = self.x1 + window_size[0]
        if self.x2 < 0:
            self.x2 = self.x2 + window_size[0]
        if self.y1 < 0:
            self.y1 = self.y1 + window_size[1]
        if self.y2 < 0:
            self.y2 = self.y2 + window_size[1]
        return self.x1, self.y1, self.x2, self.y2

    def parse_pos(self, pos, anchor=None):
        anchor = anchor or self.anchor_region  # 临时使用的anchor，不能更改self.anchor_region
        if isinstance(anchor, RectRegion):
            anchor = (anchor.left, anchor.top,
                      anchor.right, anchor.bottom)
        if isinstance(anchor, list):
            logger.warning("暂不支持多个anchor")
        elif isinstance(anchor, tuple):
            if "+" in pos:
                _1, _2 = pos.split("+")
                if is_number(_1):
                    _1 = float(_1)
                else:
                    _1 = self.parse_pos(_1, anchor)
                if is_number(_2):
                    _2 = float(_2)
                else:
                    _2 = self.parse_pos(_2, anchor)
                return _1 + _2
            elif "-" in pos:
                _1, _2 = pos.split("-")
                if is_number(_1):
                    _1 = float(_1)
                else:
                    _1 = self.parse_pos(_1, anchor)
                if is_number(_2):
                    _2 = float(_2)
                else:
                    _2 = self.parse_pos(_2, anchor)
                return _1 - _2
            else:
                if pos.endswith("x1"):
                    return anchor[0]
                elif pos.endswith("y1"):
                    return anchor[1]
                elif pos.endswith("x2"):
                    return anchor[2]
                elif pos.endswith("y1"):
                    return anchor[3]


class Offset:
    def __init__(self, x_offset, y_offset=0):
        """
        ALign对象记录了一个元素相对另一个元素的偏移量或其他对齐信息，如果Step类的第二个参数为Offset类型，则表示相对于上一个步骤pos成员变量的偏移值
        """
        self.dx = int(x_offset)
        self.dy = int(y_offset)
        self.x = None
        self.y = None

    def set_anchor_pos(self, rx, ry):
        """
        rx, ry是Align对象参考的其他元素的坐标
        """
        self.x = self.dx + int(rx)
        self.y = self.dy + int(ry)
        return self.x, self.y

    def __str__(self):
        return f"Offset({self.dx}, {self.dy})"


class Position:
    def __init__(self, value=None, align: str | Offset = 'center', region=None):
        """
        定义画面上的位置对象，根据文字或图片定义位置

        @param value:
        @param align:
        @param region: 可以是AnchorRegion对象，由Step类自动设置Anchor的区域
        """
        self.value = value
        self.align = align
        self.region: RectRegion | AnchorRegion | None | tuple = region

    def get_point(self, win_frame: "Frame"):
        """
        获取位置在画面上的相对坐标
        @param win_frame:
        @return:
        """
        if isinstance(self.value, str):
            pos = win_frame.get_text_position(self.value)
            return pos
        else:
            return None


class Exist:
    def __init__(self, value: str | list = "查找的文字或列表", type_=None, op="or", region=None,
                 last_time=0, interval=1):
        """
        判断画面中是否存在某个元素的类，如果条件判断过之后，可以通过对象的pos和obj成员变量获取具体的位置和对象信息.
        在last_time时间段内，任意一次查询找到了value，则Exist对象的satisfied方法返回True，否则返回False。默认1s查找一次

        @param type_: 元素的类型，可取值为text或pic，分别表示文字与图片
        @param value: 元素的值的列表
        @param op: 元素值列表存在于画面中的条件是 与还是或
        @param region: 可以通过该参数指定画面区域，则会在当前区域中查找
        @param last_time: 判断的持续时间，取值单位为s，例如10表示10s内一直满足存在判断条件时，则返回True。取值为0则只判断一次
        """
        self.value = value if isinstance(value, list) else [value]
        self.type_ = type_
        self.op = op
        self.region: AnchorRegion | None = region
        self.last_time = last_time
        self.interval = interval
        self.pos = None  # 如果找到目标，则目标所在的区域，xyxy
        self.obj = None

    def parse_region(self, anchor: RectRegion = None, window_size=None):
        if isinstance(self.region, AnchorRegion):
            self.region = self.region.get_region(anchor_region=anchor, window_size=window_size)
        elif isinstance(self.region, RectRegion):
            ...
        else:  # tuple
            ...

    def _satisfied(self, win_frame: "Frame"):
        """
        画面中存在某个元素的条件是否满足，该方法执行后，可以通过对象的pos和obj成员变量获取具体的位置和对象信息

        @param win_frame:
        @return:
        """
        if isinstance(self.region, AnchorRegion):
            logger.debug(
                f"Exist对象的satisfied()方法调用前需要先调用parse_region()方法以设置目标查询区域的参考区域")
            self.region = None
        if self.type_ is None:
            for v in self.value:
                if v.lower().endswith(".png") or v.lower().endswith(".jpg") or v.lower().endswith(".jpeg"):
                    self.type_ = "pic"
                    return self._satisfied(win_frame)
                else:
                    self.type_ = "text"
                    return self._satisfied(win_frame)
            logger.debug(f"判断条件不存在，默认满足条件！")
            return True
        elif self.type_ == "text":
            text = win_frame.get_text(self.region)
            if self.op == "or":
                for v in self.value:
                    if v in text:
                        logger.debug(f"当前画面中找到【{v}】 in 【{text}】")
                        self.pos = win_frame.get_text_position(v, self.region)
                        if self.pos is not None and self.pos[0] is not None:
                            self.pos = tuple([int(i) for i in self.pos])
                        self.obj = v
                        return True
                return False
            else:
                for v in self.value:
                    if v not in text:
                        return False
                return True
        elif self.type_ == "pic":
            if self.region is None:
                pic = win_frame.capture_window_xywh()
            else:
                pic = win_frame.capture_window_xywh()

            if len(self.value) == 1:
                small_pic_path = os.path.abspath(self.value[0])
                pic_w, pic_h = get_pic_size(small_pic_path)
                res = find_pic(small_pic_path, pic)  # 找到的坐标必然为正值
                self.pos = (res[1][0], res[1][1], res[1][0] + pic_w, res[1][1] + pic_h)
                self.pos = tuple([int(i) for i in self.pos])
                self.obj = self.value[0]
                return res[0]
            else:
                if self.op == "or":
                    for v in self.value:
                        small_pic_path = os.path.abspath(v)
                        res = find_pic(small_pic_path, pic)
                        pic_w, pic_h = get_pic_size(small_pic_path)
                        if res[0]:
                            self.obj = v
                            self.pos = (res[1][0], res[1][1], res[1][0] + pic_w, res[1][1] + pic_h)
                            self.pos = tuple([int(i) for i in self.pos])
                            return True
                    return False
                elif self.op == "and":
                    for v in self.value:
                        small_pic_path = os.path.abspath(v)
                        res = find_pic(small_pic_path, pic)
                        if not res[0]:
                            return False
                        self.obj = v
                        self.pos = res[1]
                    return True

    def satisfied(self, win_frame: "Frame", interval=1):
        if interval != 1 and self.interval == 1:
            self.interval = interval
        if self.last_time == 0:
            return self._satisfied(win_frame)
        else:
            for t in range(self.last_time + 1):
                if self._satisfied(win_frame):
                    return True
                time.sleep(self.interval)
            return False

    def __str__(self):
        return f"exist {self.value}"


class NotExist:
    def __init__(self, value: str | list = "查找的文字或列表", type_="text", op="or",
                 region=None,
                 last_time=0):
        """
        在last_time时间内一直找不到value，则NotExist对象的satisfied()方法返回True。任意一次找到则返回False。默认1s查找一次
        """
        self.exist = Exist(value=value, type_=type_, op=op, region=region, last_time=last_time)
        self.pos = self.exist.pos
        self.obj = self.exist.obj
        self.region = self.exist.region

    def satisfied(self, win_frame: "Frame", interval=1):
        return not self.exist.satisfied(win_frame, interval=interval)

    def __str__(self):
        return f"not exist {self.exist.value}"


class Step:
    def __init__(self, op, target, judge=None, condition=None, wait_method=None):
        """
        定义步骤，
        示例1：
        Step("press", "Ctrl+C", "until", Exist("人物"))  # 按Ctrl+C，直到画面中出现"人物"
        示例2：
        Step(None, None, "until", Exist("竹林偷伐者"))  # 相当于一直等待，直到画面中出现"竹林偷伐者"，该步骤才能通过，进而执行下一步
        示例3：
        Step("long-press-5", "R", None, None)  # 长按R键5s

        :param op: 操作类型，可取值"press", "double-press","left-click", "long-press-{i}",None, "right-click"等，
        其中"long-press-{i}"表示长按某个键i秒，如示例3所示。None则表示不执行操作，可用于等到condition条件满足时使用，
        op也可以是一个函数或方法，这种情况下，Step.do()将直接调用该方法，此时self.target作为传递给该方法的参数。

        :param target: target可以是一个字符串，表示画面上的文字的位置，也可以是一个图片文件，表示画面中图片的位置，也可以是一个Offset对象，
        表示相对于上一个步骤的判断条件对象的偏移量。

        :param judge: 判断操作完成的类型，可取值为until、if或None，如果为None，则表示不判断
        :param wait_method: 条件不满足时，调用的方法，repeat表示重复执行op，如果取值为None，则等待而不重复操作
        """
        self.op = op

        # 按键操作则为键名，鼠标时间则为鼠标点击位置，鼠标点击位置可以通过Position类或Align定义
        self.target: Position | Offset | str | tuple = target
        self.target_region: RectRegion | None = None

        self.judge = judge
        self.condition: "Exist" = condition  # 如果Exist对象的region变量是一个AnchorRegion，则其anchor自动对应为self.target_region
        self.wait_method = wait_method

        self.pos = None  # 该步骤执行后，until后条件中判断的位置区域会保存在该变量中，便于后续使用，可能是(x1,y1,x2,y2)的形式，也可能是(x,y)的形式
        self.obj = None  # 该步骤执行后，until后条件中判断的对象名会保存在该变量中，便于后续使用
        self.frame: "Frame" | None = None
        self.last_step: Step | None = None
        self.before_action = None  # 本步骤操作前的画面
        self.after_action = None  # 本步骤操作后的画面
        self.window_size = None  # 窗口尺寸

    def pre_do(self, last_step):
        if last_step is None:
            return
        else:
            self.last_step = last_step

        if isinstance(self.target, Offset):
            if last_step.pos is not None:
                self.target.set_anchor_pos(last_step.pos[0], last_step.pos[1])
                self.target_region = RectRegion().set_xywh(self.target.x, self.target.y, 1, 1)
            else:
                logger.warning(f"操作的目标对象为Offset类型，但上一个步骤没有生成对应的参考位置，{last_step.pos=}")
                return
        elif isinstance(self.target, tuple):
            self.target_region = RectRegion().set_xywh(self.target[0], self.target[1], 1, 1)
        elif isinstance(self.target, str):
            if "press" in self.op:  # 说明target是个按键，按键不存在坐标位置
                self.target_region = None
            else:
                # 查找字符串或图片在画面中的位置
                self.target_region = None

    def _action(self, win_frame: "Frame"):
        logger.debug(f"操作：{self.op} {self.target}")
        self.window_size = win_frame.window_size
        if self.op is None:
            return
        elif callable(self.op):  # 如果op是一个可以调用的函数或方法，则直接调用
            if self.target is not None:
                self.op(self.target)
            else:
                self.op()
        elif self.op == "press":
            win_frame.press_key(self.target)
        elif self.op == "double-press":
            sleep_interval = random.randint(1, 10) / 100 + 0.1
            win_frame.press_key(self.target)
            time.sleep(sleep_interval)
            win_frame.press_key(self.target)
        elif self.op.startswith("long-press-"):
            # 长按某个键5s
            last_time = int(self.op.replace("long-press-", ""))
            # post_key(win_frame.window, self.target, last_time=last_time)
            win_frame.long_press_key(self.target, last_time=last_time)
        elif self.op == "left-click" or self.op == "click":
            if isinstance(self.target, Position):
                x, y = self.target.get_point(win_frame)
                win_frame.left_click(x, y)
            elif isinstance(self.target, tuple):
                x, y = self.target
                win_frame.left_click(x, y)
            elif isinstance(self.target, Offset):
                x, y = self.target.x, self.target.y
                win_frame.left_click(x, y)
        elif self.op == "right-click":
            if isinstance(self.target, Position):
                x, y = self.target.get_point(win_frame)
                win_frame.right_click(x, y)
            elif isinstance(self.target, tuple):
                x, y = self.target
                win_frame.right_click(x, y)
            elif isinstance(self.target, Offset):
                x, y = self.target.x, self.target.y
                win_frame.right_click(x, y)

    def do(self, win_frame: "Frame"):
        self.frame = win_frame
        logger.debug(f"执行步骤：{self.__str__()}")
        self.before_action = win_frame.capture_window_xywh()
        self._action(win_frame)
        if self.judge is not None:
            time.sleep(0.5)
            if isinstance(self.condition, Exist):
                self.condition.parse_region(anchor=self.target_region, window_size=win_frame.window_size)
            satisfied = self.condition.satisfied(win_frame)
            while not satisfied:  # 如果结束条件不满足，则继续执行本步骤定义的操作
                if self.wait_method is None:
                    time.sleep(0.5)
                else:
                    self._action(win_frame)
                    time.sleep(1)
                satisfied = self.condition.satisfied(win_frame)
            self.after_action = win_frame.capture_window_xywh()
            self.pos = self.condition.pos
            self.obj = self.condition.obj
        else:
            self.pos = None
            self.obj = None
        logger.debug(f"步骤执行完毕：{self.__str__()}")
        return True

    def __str__(self):
        if self.judge is not None:
            return f"{self.op} {self.target} {self.judge} {self.condition.__str__()}"
        else:
            return f"{self.op} {self.target}"

    def show(self, save_to=None):
        """
        调试时显示当前步骤的逻辑。

        上一步的参考区域为淡绿色实线框
        相对于上一步的偏移为绿色箭头
        查找的区域为红色实线框
        找到的目标为绿色实线框
        操作为红色字体

        :param save_to: 保存的gif图片的路径，必须以.gif结尾
        """
        if "press" in self.op:
            cv2.putText(self.before_action, text=f"{self.op} {self.target}", org=(20, 20),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 0, 0), thickness=2)
        elif "click" in self.op:
            if isinstance(self.target, Offset):
                last_pos = self.last_step.pos[0:2]
                p2 = (int(self.target.x), int(self.target.y))
                cv2.rectangle(self.before_action, pt1=last_pos, pt2=self.last_step.pos[2:4],
                              color=(0, 0, 255), thickness=2, lineType=cv2.LINE_AA)
                cv2.arrowedLine(self.before_action, pt1=last_pos, pt2=p2,
                                color=(0, 255, 0), thickness=2, line_type=cv2.LINE_AA, tipLength=0.2)
                cv2.putText(self.before_action, text=f"{self.op} {self.target}", org=p2,
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 0), thickness=2)
            elif isinstance(self.target, tuple):  # Offset类型会在执行过程中转换为tuple
                last_pos = self.last_step.pos[0:2]
                p2 = self.target
                cv2.rectangle(self.before_action, pt1=last_pos, pt2=self.last_step.pos[2:4],
                              color=(0, 0, 255), thickness=2, lineType=cv2.LINE_AA)
                cv2.arrowedLine(self.before_action, pt1=last_pos, pt2=p2,
                                color=(0, 255, 0), thickness=2, line_type=cv2.LINE_AA, tipLength=0.2)
                cv2.putText(self.before_action, text=f"{self.op} {self.target}", org=p2,
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(0, 255, 0), thickness=2)

        if isinstance(self.condition, Exist) or isinstance(self.condition, NotExist):
            if self.condition.region is None:  # 如果未指定存在条件的查找位置，则默认全屏查找
                cv2.rectangle(self.after_action, pt1=(0, 0), pt2=self.window_size,
                              color=(255, 0, 0), thickness=2, lineType=cv2.LINE_AA, )
            elif isinstance(self.condition.region, tuple):
                p1 = self.condition.region[0:2]
                p2 = self.condition.region[2:4]
                cv2.rectangle(self.after_action, pt1=p1, pt2=p2,
                              color=(255, 0, 0), thickness=2, lineType=cv2.LINE_AA)

            if isinstance(self.condition.pos, tuple):  # 如果存在条件的位置不为空，说明找到了相关目标，绘制该目标示意图
                p1 = (int(self.condition.pos[0]), int(self.condition.pos[1]))
                p2 = (int(self.condition.pos[2]), int(self.condition.pos[3]))
                w, h = p2[0] - p1[0], p2[1] - p1[1]
                cv2.rectangle(self.after_action, pt1=p1, pt2=p2,
                              color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA, )
                cv2.putText(self.after_action, text=f"Exist: {self.condition.obj},{w=},{h=}", org=p1,
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.6, color=(0, 255, 0), thickness=2)
        # before = draw_element_on_pic(self.before_action, False,
        #                              circle={"center": (0, 0), "radius": 20, "fill": "red", "outline": "yellow"})
        # self.target_region  # 目标区域
        # self.condition.region.get_region()  # 条件区域
        # self.last_step
        # show_pic([self.before_action, self.after_action])
        if save_to is not None:
            from PIL import Image
            if self.after_action is None:
                return
            images = [
                Image.fromarray(self.before_action),
                Image.fromarray(self.after_action)
            ]
            images[0].save(save_to, save_all=True, loop=True, append_images=images[1:], duration=2000)
        return


class Steps:
    def __init__(self, steps, debug=False):
        """
        定义游戏内操作的步骤

        @param debug: 是否为调试模式，如果是调试模式，则会显示每一步的操作示意图
        """
        self.steps = steps

    def run(self, win_frame):
        """
        逐步执行Steps对象中记录的步骤
        """
        last_step: Step | None = None
        i = 1
        for step in self.steps:
            step: Step = step
            step.pre_do(last_step)  # 在步骤执行前进行的操作
            success = step.do(win_frame)  # 执行步骤，可能执行失败，如点击某个按钮但画面上找不到就会失败
            if not success and last_step is not None:  # 如果执行失败，就尝试再次执行上一个步骤
                last_step.do(win_frame)
                success = step.do(win_frame)

            if success:  # 如果当前步骤执行结束，就记录当前步骤
                step.show(save_to=f"step{i}.gif")
                last_step = step
            i += 1


class Frame:
    def __init__(self, title, game_path=None, sim_mode=None, sim_info=None):
        """
        游戏图像识别框架
        例如：frame = Frame("天谕",
                           sim_mode="大漠插件-remote",
                           sim_info={"display": "normal", # 大漠绑定窗口的图色模式，模式参数参考dm.BindWindowEx()方法
                                     "mouse": "normal", # 大漠绑定窗口的鼠标模式
                                     "keypad": "normal", # 大漠绑定窗口的键盘模式
                                     "public": "dx.public.active.api", # 大漠绑定窗口的公用模式
                                     "mode": 0,  # 大漠绑定窗口的总模式
                                     "key": "mmdlljafd8c5cbf193e99306e9eb61ceb5bd44",  # 大漠的注册码
                                     "add_key": "ewdSEKFZP",
                                     "guard_type": "memory4", # 开启大漠防护盾的类型，参考dm.DmGuard()方法
                                     "port": 8765,
                                     })  # 大漠的附加码

        :@param title: 游戏窗口标题，为标题的子字符串，但需要唯一确定的窗口
        :@param game_path: 游戏文件路径，如果不存在游戏窗口，则启动该可执行文件
        :@param sim_mode: 模拟键鼠的方法，默认是python自带的方法，可以取值【大漠插件】/【大漠插件-remote】则会使用大漠插件的模拟键鼠方法，
        使用大漠插件时，可以通过sim_info参数传入大漠插件绑定窗口的模式，【大漠插件-remote】使用restful接口请求远程大漠插件操作程序进行模拟鼠标键盘操作，该参数主要是为了解决
        大漠插件没有64位dll的问题，通过远程实现64位python调用32位大漠插件
        """
        if sim_info is None:
            sim_info = {}
        self.set_window_size_steps = None  # 设置窗口尺寸的步骤
        self.title = title
        self.snapshot = None
        self.window = find_window(title, exact=False)
        self.sim_mode = sim_mode
        if isinstance(self.window, dict) and len(self.window) == 1:
            _ = list(self.window.keys())[0]
            self.window_title = self.window[_]
            self.window = _
        else:
            if len(self.window) > 1:
                _ = list(self.window.keys())[0]
                self.window_title = self.window[_]
                self.window = _
                logger.warning(f"找到多个包含{title}的窗口，默认使用第一个:{self.window_title}")
            else:
                logger.error(f"未找到或找到多个包含{title}的窗口，目前不支持这种情况！")
                sys.exit()
        self.window_size = get_size_of_window(self.window, True)  # 不包括标题栏的大小
        self.udf_steps = {}
        if sim_mode is None:
            pass
        elif sim_mode == "大漠插件":
            logger.debug(f"使用大漠插件进行键鼠操作")
            self.dm = DM(key=sim_info.get("key"), add_key=sim_info.get("add_key"))
            if sim_info.get("guard_type") is not None:
                self.dm.DmGuard(1, sim_info.get("guard_type"))
            self.dm.set_bindmode(sim_info.get("display"), sim_info.get("mouse"),
                                 sim_info.get("keypad"), sim_info.get("public"),
                                 sim_info.get("mode"))
            self.dm.bind_window(self.window)
        elif sim_mode == "大漠插件-remote":
            logger.debug(f"使用大漠插件-remote进行键鼠操作")
            self.dm = DMRemote(key=sim_info.get("key"), add_key=sim_info.get("add_key"), port=sim_info.get("port"))
            if sim_info.get("guard_type") is not None:
                self.dm.DmGuard(1, sim_info.get("guard_type"))
            self.dm.bind_window(self.window, sim_info.get("display"), sim_info.get("mouse"),
                                sim_info.get("keypad"), sim_info.get("public"),
                                sim_info.get("mode"))

        self.map: Map | None = None
        self.chat: Chat | None = None
        self.task: Task | None = None
        self.time_panel: TimePanel | None = None  # 时间面板

    def press_key(self, key):
        if self.sim_mode == "大漠插件" or self.sim_mode == "大漠插件-remote":
            self.dm.press_key(key)
        else:
            post_key(self.window, key)

    def long_press_key(self, key, last_time):
        logger.debug(f"暂不支持")
        if self.sim_mode == "大漠插件" or self.sim_mode == "大漠插件-remote":
            self.dm.press_key(key)
        else:
            post_key(self.window, key)

    def left_click(self, x, y, offset=(0, 0)):
        x = x + offset[0]
        y = y + offset[1]
        if self.sim_mode == "大漠插件" or self.sim_mode == "大漠插件-remote":
            self.dm.left_click(x, y)
        else:
            do_click(x, y, self.window)

    def right_click(self, x, y, offset=(0, 0)):
        x = x + offset[0]
        y = y + offset[1]
        if self.sim_mode == "大漠插件" or self.sim_mode == "大漠插件-remote":
            self.dm.right_click(x, y)
        else:
            do_click(x, y, self.window, right=True)

    def drag_to(self, from_point, to_point, button="left"):
        """
        鼠标拖动，从from_point拖动到to_point，button表示是鼠标哪个键，可取值"left","right","mid"
        """
        if self.sim_mode == "大漠插件" or self.sim_mode == "大漠插件-remote":
            self.dm.drag_to(from_point, to_point, button)
        else:
            logger.warning(f"暂不支持鼠标拖动")

    def get_target_position(self, target, region=None):
        if target.lower().endswith("jpg") or target.lower().endswith("jpeg") or target.lower().endswith(
                "png"):
            res = self.get_pic_position_xyxy(target, region)
        else:
            res = self.get_text_position(target, region)
        return res

    def turn_direction_to(self, target, region=None):
        """
        将角色面向转向某个目标
        """
        res = self.get_target_position(target, region)  # (x,y,x,y)
        if res is None or res[0] is None:
            res = self.get_target_position(target, region)  # (x,y,x,y)
            if res is None or res[0] is None:
                logger.debug(f"未找到目标{target=}")
                return
        x1, y1 = int(self.window_size[0] / 2), int((res[1] + res[3]) / 2)
        x2, y2 = int((res[0] + res[2]) / 2), int((res[1] + res[3]) / 2)
        self.drag_to((x1, y1), (x2, y2), button="right")

    def show_snapshot(self):
        show_pic(self.snapshot)

    def define_set_window_size(self, steps: Steps):
        self.set_window_size_steps = steps

    def define_steps(self, steps_name, steps):
        self.udf_steps.update({steps_name: steps})

    def capture_window_xywh(self, x=0, y=0, w=0, h=0):
        """
        按照xywh四个点的坐标截取屏幕区域的图片
        """
        if w == 0:
            w = self.get_window_size()[0]
        if h == 0:
            h = self.get_window_size()[1]
        x2 = x + w
        y2 = y + h
        self.snapshot = capture_pic_undecorated(self.window, x, y, x2, y2)
        return self.snapshot

    def capture_window_xyxy(self, x1, y1, x2, y2):
        """
        按照xyxy四个点的坐标截取屏幕区域的图片，第一个xy是区域左上角坐标，第二个xy是区域右下角坐标
        """
        self.snapshot = capture_pic_undecorated(self.window, x1, y1, x2, y2)
        return self.snapshot

    def set_window_size(self, width=None, height=None):
        """
        将游戏窗口设置为指定大小
        @return:
        """
        # show_pic(self.capture_window())
        self.run_steps(self.set_window_size_steps)

    def run_steps(self, steps: Steps | str):
        if isinstance(steps, Steps):
            steps.run(self)
        else:
            if self.udf_steps.get(steps) is not None:
                self.run_steps(self.udf_steps.get(steps))
        logger.debug("步骤序列执行完毕")

    def run_steps_forever(self, steps: Steps | str, interval=5):
        """
        无限执行指定按键步骤，常用于卡键盘按键
        """

        while True:
            random_sec = random.randint(1, 10) / 10
            self.run_steps(steps)
            time.sleep(random_sec + interval)
            # logger.debug(f"运行步骤{steps=}")

    def get_text(self, region=None):
        self.snapshot = self.capture_region(region)

        return ocr(self.snapshot, paragraph=True)

    def capture_region(self, region):
        region = self.positive_region(region)

        if region is not None:
            if isinstance(region, tuple):
                pic = self.capture_window_xyxy(*region)
            else:  # RectRegion
                pic = self.capture_window_xyxy(region.x1(), region.y1(), region.x2(), region.y2())
        else:
            pic = self.capture_window_xywh()
        return pic

    def positive_region(self, region):
        if region is None:
            return
        w = self.window_size[0]
        h = self.window_size[1]
        if isinstance(region, tuple):
            x1 = region[0] + w if region[0] < 0 else region[0]
            x2 = region[2] + w if region[2] < 0 else region[2]
            y1 = region[1] + h if region[1] < 0 else region[1]
            y2 = region[3] + h if region[3] < 0 else region[3]
            region = (x1, y1, x2, y2)
        elif isinstance(region, RectRegion):  # RectRegion
            region.transfer_to_positive(width=self.window_size[0], height=self.window_size[1])
        else:  # Region
            region = region.transfer_to_positive(width=self.window_size[0], height=self.window_size[1])
        return region

    def get_text_position(self, text, region=None, method="first"):
        """
        获取给定文字在画面上的位置

        :param text: 需要查找的文字内容
        :param region: 查找文字的区域
        :param method: 可取值"first", "most similar"，表示查找到的第一个或者最相近的。
        """
        pic = self.capture_region(region)

        texts = ocr(pic, paragraph=False)
        x1, y1, x2, y2 = None, None, None, None  # 这是相对于region的坐标
        for line in texts:
            position, content = line
            p1, p2, p3, p4 = position
            text_content, text_probability = content
            if text in text_content:
                x1 = p1[0]
                y1 = p1[1]
                x2 = p3[0]
                y2 = p3[1]
                break

        if isinstance(region, RectRegion):
            rx = region.left
            ry = region.top
        elif region is None:
            rx = 0
            ry = 0
        elif isinstance(region, Region):
            rx = region.x1
            ry = region.y1
        else:
            rx = region[0]
            ry = region[1]

        if x1 is not None:
            x1 = x1 + rx
            x2 = x2 + rx
            y1 = y1 + ry
            y2 = y2 + ry

        return x1, y1, x2, y2

    def get_pic_position_xyxy(self, pic, region=None):
        """
        查找图片在画面中的绝对位置
        """
        screen = self.capture_region(region)
        exist, res = find_pic(pic, screen, 0.65)
        if not exist:
            logger.warning(f"查找的图片可信度较低，返回的图片位置可能错误{pic=}")
        size = get_pic_size(pic)
        x1, y1 = res
        x2, y2 = x1 + size[0], y1 + size[1]
        return x1, y1, x2, y2

    def get_window_size(self, refresh=False):
        if refresh:
            self.window_size = get_size_of_window(self.window)
        return self.window_size

    def init_chat(self, anchor: str | list = None, anchor_region: AnchorRegion | None = None, channels=None):
        if isinstance(anchor, str):  # 说明只有一个参考点
            _ = anchor.lower()
            if _.endswith(".jpg") or _.endswith(".png") or _.endswith("jpeg"):
                res = self.get_pic_position_xyxy(anchor)
            else:
                res = self.get_text_position(anchor)
            chat_region = anchor_region.get_region(anchor_region=res, window_size=self.window_size)
            self.chat = Chat(chat_region, channels)
        else:
            ...

    def init_time(self, region=None):
        if region is not None:
            self.time_panel = TimePanel(region=region, frame=self)

    def get_time(self):
        return self.time_panel.get_time()

    def init_task(self, region=None, find_region=None, anchor: str | None = None, anchor_region=None):
        """
        初始化任务面板

        :param region: 任务面板所处的绝对区域位置，为xyxy表示的四个int数值，如果任务面板位置不变的时候，可以使用该参数指定任务面板位置
        :param find_region: 查找任务面板位置的区域，在该区域内查找任务面板的参考点anchor的位置
        :param anchor: 任务面板参考点，根据该点确定任务面板位置
        :param anchor_region: 指定任务面板相对参考点的位置区域。
        """
        if region is not None:
            self.task = Task(region_xyxy=region)
            self.task.set_frame(self)
        else:
            if anchor is None:
                logger.warning(f"任务面板初始化失败，没有任务面板位置的识别特征")
                return
            elif anchor.lower().endswith("jpg") or anchor.lower().endswith("jpeg") or anchor.lower().endswith(
                    "png"):
                res = self.get_pic_position_xyxy(anchor, find_region)
            else:
                res = self.get_text_position(anchor, find_region)
            if res[0] is None:
                return False
            # res必须是正值的region
            task_region = anchor_region.get_region(anchor_region=res, window_size=self.window_size)
            self.task = Task(task_region, frame=self)
            return True

    def get_task_text(self):
        return self.task.get_task_text(self)

    def show_region(self, region):
        if isinstance(region, RectRegion):
            show_pic(self.capture_window_xyxy(*region.get_xyxy()))


class Region:
    def __init__(self, win_frame: "Frame | None" = None, align="center", width_child=0, height_child=0):
        """
        定义窗口中的某个区域，通过该类可以获取(x,y,w,h)这种类型的相对区域坐标
        示例：
        region = Region(frame)
        r.get_region(align="center", width_child=100, height_child=110)

        示例2：
        region = Region(align="center", width_child=100, height_child=110).get_region(win_frame)

        get_region()方法返回的是区域表示的(x,y,w,h)四个参数的tuple
        """
        self.frame = win_frame
        if self.frame is not None:
            self.width_window, self.height_window = win_frame.get_window_size()
            self.align = None
            self.width_child = None
            self.height_child = None
        else:
            self.width_window, self.height_window = None, None
            self.align = align
            self.width_child = width_child
            self.height_child = height_child
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None

    def get_region(self, win_frame=None, align=None, width_child=None, height_child=None):
        """
        根据传入的区域定义，获取区域的数字范围，默认返回整个窗口区域。例如：
        region.get_region("center", 100, 100)  # 表示窗口中间100*100范围的(x,y,w,h)定义
        return (x,y,w,h)
        """
        if win_frame is not None:
            self.frame = win_frame
            self.width_window, self.height_window = win_frame.get_window_size()
        self.align = align or self.align or "center"
        self.width_child = width_child or self.width_child
        self.height_child = height_child or self.height_child

        if self.width_child is None or self.width_child == 0:  # 如果不指定区域的宽和高，则默认宽和高等于窗口的宽和高
            self.width_child = self.width_window
        if self.height_child is None or self.height_child == 0:
            self.height_child = self.height_window
        if self.align == "center":
            left_pad = int((self.width_window - self.width_child) / 2)
            top_pad = int((self.height_window - self.height_child) / 2)
        elif align == "left":
            left_pad = 0
            top_pad = int((self.height_window - self.height_child) / 2)
        elif align == "right":
            left_pad = self.width_window - self.width_child
            top_pad = int((self.height_window - self.height_child) / 2)
        elif align == "top":
            left_pad = int((self.width_window - self.width_child) / 2)
            top_pad = 0
        elif align == "bottom":
            left_pad = int((self.width_window - self.width_child) / 2)
            top_pad = self.height_window - self.height_child
        else:
            left_pad = 0
            top_pad = 0
        self.x1 = left_pad
        self.y1 = top_pad
        self.x2 = left_pad + self.width_child
        self.y2 = top_pad + self.height_child
        return left_pad, top_pad, self.width_child, self.height_child

    def transfer_to_positive(self, width, height):
        self.width_window = width
        self.height_window = height
        x, y, w, h = self.get_region()
        x2, y2 = x + w, y + h
        return x, y, x2, y2


if __name__ == "__main__":
    # logger.debug(ocr("temp.png", paragraph=False))
    # frame = Frame('天谕-无束缚3D')
    # frame = Frame('舒海云')
    frame = Frame('天谕-无束缚3D幻想网游', sim_mode="大漠插件-remote", sim_info={
        "display": "gdi2",
        "mouse": "dx.mouse.position.lock.api|dx.mouse.position.lock.message|dx.mouse.clip.lock.api|dx.mouse.input.lock.api|dx.mouse.state.api|dx.mouse.api|dx.mouse.cursor",
        "keypad": "windows",
        "public": "",
        "mode": 11,
        "key": "mmdlljafd8c5cbf193e99306e9eb61ceb5bd44",
        "add_key": "ewdSEKFZP",
        "guard_type": "memory4",
        "port": 8765,
    })
    # frame = Frame('记事本')
    # frame = Frame('炎火前哨, 宁梦')
    # r = Region(frame)
    # steps_1 = Steps(
    #     steps=[
    #         # 按Esc键，直到窗口中心区域(317, 532)大小范围内出现文字"游戏设置"
    #         Step("press", "escape", "until", Exist(value="游戏设置", region=r.get_region("center", 317, 532))),
    #
    #         # 单击中心区域的【游戏设置】，直到中心区域(874, 609)出现【分辨率】
    #         Step("left-click", Position("游戏设置", region=r.get_region("center", 874, 609)), "until",
    #              Exist(value="分辨率", region=r.get_region("center", 874, 609))),
    #
    #         # 单机
    #         Step("left-click", Position("分辨率", align=Align(20)), "until", Exist())
    #     ])
    # frame.define_set_window_size(steps=steps_1)
    # frame.set_window_size()

    steps_2 = Steps(
        steps=[
            Step("press", "numpad0", "until", Exist(value='pic1.png', type_='pic'), wait_method="repeat"),
            Step("left-click", Offset(397, 16), "until", Exist("门派"), wait_method="repeat"),
            Step("left-click", Offset(0, 0), "until", Exist("苏澜郡"), wait_method="repeat"),
            Step("left-click", Offset(0, 0), "until", Exist("汐族"), wait_method="repeat"),
        ]
    )
    frame.define_steps("打开苏澜郡声望面板", steps_2)
    # frame.run_steps("打开苏澜郡声望面板")

    steps_重复按键 = Steps(
        steps=[
            # Step("press", "R", None),
            Step("press", "R", "until",
                 NotExist("竹林偷伐者", last_time=20, region=Region(align="center", width_child=600)),
                 wait_method="repeat"),
            Step("double-press", "space", "until",
                 Exist("竹林偷伐者", last_time=60, interval=10, region=Region(align="center", width_child=600)),
                 wait_method="repeat"),
            # Step(None, None, "until",
            #      Exist("草药", last_time=60, interval=5),
            #      wait_method="repeat"),  # 等待场景中出现【草药】
            # Step("right-click", "草药", "until",
            #      Exist(),
            #      wait_method=None
            #      )
        ]
    )

    # frame.run_steps(steps_重复按键)
    frame.run_steps_forever(steps_重复按键, interval=8)
    # frame.capture_window()
    # logger.debug(frame.get_text())
