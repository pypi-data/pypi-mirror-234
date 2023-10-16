# 用于测量屏幕上鼠标点击位置的距离

import pyWinhook
from pyWinhook.HookManager import MouseEvent
import pythoncom


class KeyBoardManager:
    keyIsPressed = False

    def __init__(self):
        self.start_pos = None
        self.end_pos = None
        self.pressed_key = None
        self.dragging = False

    def onKeyDown(self, event):
        print(f"按下键盘：{event.Key}")
        if self.keyIsPressed:
            return True
        self.keyIsPressed = True
        return True

    def onKeyUp(self, event):
        self.keyIsPressed = False
        print(str(event.Key) + ' is released')
        return True

    def mouseup(self, event: MouseEvent):
        self.end_pos = event.Position
        dx, dy = self.end_pos[0] - self.start_pos[0], self.end_pos[1] - self.start_pos[1]
        if dx > 1 or dy > 1:
            print(f"按下鼠标：{self.start_pos}")
            print(f"弹起鼠标：{event.Position}")
            # if self.dragging:
            print(f"dx, dy = {(self.end_pos[0] - self.start_pos[0], self.end_pos[1] - self.start_pos[1])}")
            self.dragging = False
        return True

    def mousedown(self, event: MouseEvent):
        self.start_pos = event.Position
        return True


if __name__ == '__main__':
    print("请在起点按下鼠标并拖动至终点开始测量")
    mykbmanager = KeyBoardManager()
    hookmanager = pyWinhook.HookManager()
    hookmanager.KeyDown = mykbmanager.onKeyDown
    hookmanager.KeyUp = mykbmanager.onKeyUp
    hookmanager.MouseLeftUp = mykbmanager.mouseup
    hookmanager.MouseLeftDown = mykbmanager.mousedown

    # hookmanager.HookKeyboard()  # 如果需要检测键盘按键，则取消该行注释
    hookmanager.HookMouse()
    pythoncom.PumpMessages()
