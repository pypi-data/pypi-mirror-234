# sendInput方法发送键盘鼠标事件
import ctypes
import time
import pydirectinput

from yangke.common.win.keyboard import get_virtual_keycode

SendInput = ctypes.windll.user32.SendInput

PUL = ctypes.POINTER(ctypes.c_ulong)


def key_click_dx(x, y):
    pydirectinput.click(x, y)


def key_double_click_dx(x, y):
    pydirectinput.doubleClick()


def post_key_dx(key):
    """
    key = "esc", "A", "shift"等
    """
    pydirectinput.press(key)


class KeyBdInput(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]


class HardwareInput(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_ushort)
    ]


class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]


class Input_I(ctypes.Union):
    _fields_ = [
        ("ki", KeyBdInput),
        ("mi", MouseInput),
        ("hi", HardwareInput),
    ]


class Input(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("ii", Input_I)
    ]


class POINT(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_ulong),
        ("y", ctypes.c_ulong)
    ]


def press_key(key):
    hex_key_code = get_virtual_keycode(key)
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hex_key_code, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def release_key(key):
    hex_key_code = get_virtual_keycode(key)
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hex_key_code, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def post_key(key, last_time=0.1):
    """
    前端按键，无法发送组合键
    """
    press_key(key)
    time.sleep(last_time)
    release_key(key)


def get_mouse_pos():
    """
    获取鼠标位置
    """
    orig = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(orig))
    return int(orig.x), int(orig.y)


def set_mouse_pos(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)


def mouse_press(x, y, button='left'):
    i = 2
    if button == 'right':
        i = 8
    set_mouse_pos(x, y)
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, i, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def mouse_release(x, y, button='left'):
    i = 4
    if button == 'right':
        i = 8
    set_mouse_pos(x, y)
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(0, 0, 0, i, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
