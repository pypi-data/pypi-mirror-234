from yangke.common.qt import (YkWindow, run_app, logger, QApplication, YkFoldableWidget, QWidget, QLabel, QComboBox,
                              QLineEdit, YkItem, YkInputPanel)
from yangke.game.gf import Step, Steps, Frame, NotExist, Exist, Region, AnchorRegion, RectRegion, Position, Offset
from yangke.base import start_threads, stop_threads


class StepWidget(YkItem):
    def __init__(self, idx, op, target, judge, condition, wait_method):
        self.step = Step(op, target, judge, condition, wait_method)
        code = ["press", "double-press", "left-click", "right-click"]  # QComboBox只支持添加元素为字符串的类型
        # self.op_widget = QComboBox()
        # self.op_widget.addItems(code)
        # self.op_widget.setCurrentIndex(0)

        self.op_widget = YkItem(["press", "click", "right click", "double click"],
                                value="",
                                unit=YkItem(label=["重复", "等待"], value=["直到", "无"], unit=["无", "存在", "不存在"],
                                            size=[10, 20, 20],
                                            margins=(10, 0, 10, 0)),
                                size=[20, 20, 50],
                                margins=(10, 0, 10, 0))
        unit = '<button on-click="remove_step">移除步骤</button>'
        super().__init__(f"步骤{idx}", value=self.op_widget, unit=unit, size=[20, 200, 50])
        # self.target_widget = QLineEdit("")
        # self.judge_widget = QComboBox(self)
        # self.judge_widget.addItems(["until", "无"])
        # self.condition_widget = QComboBox(self)
        # self.condition_widget.addItems(["Exist", "NotExist"])


class MainWindow(YkWindow):
    def __init__(self):
        super().__init__()
        self.add_input_panel("ui/ui_panel.yaml")
        self.thread = None
        self.running = False
        self.set_status_bar_label("天谕")
        self.frame: Frame | None = None
        self.add_input_panel(domain="自定义步骤")
        panel: YkInputPanel = self.panels.get("自定义步骤")
        item = StepWidget(1, "press", "R", None, None, None)
        panel.insert_item(1, item)
        self.add_content_tab(YkItem(), "存在条件设置")

    def add_step(self):
        panel: YkInputPanel = self.panels.get("自定义步骤")
        idx = panel.get_items_count()
        panel.insert_item(idx, StepWidget(idx, "press", "R", None, None, None))

    def init(self):
        settings = self.get_value_of_panel(need_dict=True, need_unit=False)
        role = settings.get("游戏角色名").strip()
        self.frame = Frame(role)
        # self.frame = Frame(role, sim_mode="大漠插件-remote", sim_info={
        #     "display": "gdi2",
        #     "mouse": "dx.mouse.position.lock.api|dx.mouse.position.lock.message|dx.mouse.clip.lock.api|dx.mouse.input.lock.api|dx.mouse.state.api|dx.mouse.api|dx.mouse.cursor",
        #     "keypad": "windows",
        #     "public": "",
        #     "mode": 11,
        #     "key": "mmdlljafd8c5cbf193e99306e9eb61ceb5bd44",
        #     "add_key": "ewdSEKFZP",
        #     "guard_type": "memory4",
        #     "port": 8765,
        # })
        self.frame.init_chat(anchor="ui/ZhaoMu.png", anchor_region=AnchorRegion(0, "anchor.y1", "anchor.x1", -10),
                             channels=["世界", "团队", "队伍", "附近", "阵营", "地区"])
        suc = self.frame.init_task(anchor="任务", find_region=RectRegion(left=-350, top=300, right=-1, bottom=-500),
                                   anchor_region=AnchorRegion("anchor.x1", "anchor.y1", -10, "anchor.y1+400"))
        if not suc:
            self.frame.init_task(anchor="驻地", find_region=RectRegion(left=-350, top=300, right=-1, bottom=-500),
                                 anchor_region=AnchorRegion("anchor.x1-100", "anchor.y1", -10, "anchor.y1+400"))

        # self.frame.init_time(region=(-170, 0, -2, 30))
        self.frame.init_time(region=(-25, 5, -2, 25))
        # self.frame.turn_direction_to("青蛙", region=Region(width_child=1000, height_child=800))

    def ShengWangRenWu(self):
        self.init()
        time = self.frame.get_time()
        steps_寻路至平海镇布告栏处 = Steps(steps=[
            # 打开人物属性面板
            Step("press", "ctrl+c", "until", Exist("ui/RWSX.png"), wait_method="repeat"),

            # 切换到声望面板
            Step("click", Offset(x_offset=326, y_offset=18), "until",
                 Exist("门派",
                       region=AnchorRegion(x1="anchor.x1-337", y1="anchor.y1+32",
                                           x2="anchor.x1-143", y2="anchor.y1+69")),
                 wait_method="repeat"),

            # 折叠门派声望
            Step("click", Offset(x_offset=0, y_offset=0), "until",
                 Exist("萤川郡",
                       region=AnchorRegion(x1="anchor1.x1-4", y1="anchor.y1+53",
                                           x2="anchor1.x1+80", y2="anchor.y1+100")),
                 wait_method="repeat"),

            # 展开莹川郡声望
            Step("click", Offset(x_offset=0, y_offset=0), "until",
                 Exist("平海镇",
                       region=AnchorRegion(x1="anchor1.x1-16", y1="anchor.y1+40",
                                           x2="anchor1.x1+80", y2="anchor.y1+100")),
                 wait_method="repeat"),

            # 点击平海镇声望
            Step("click", Offset(x_offset=0, y_offset=0), "until",
                 Exist("平海镇",
                       region=AnchorRegion(x1="anchor1.x1+250", y1="anchor.y1-100",
                                           x2="anchor1.x1+380", y2="anchor.y1-55")),
                 wait_method="repeat"),

            # 点击查看声望玩法
            Step("click", Offset(x_offset=468, y_offset=119), "until",
                 Exist("平海镇声望玩法",
                       region=AnchorRegion(x1="anchor1.x1+100", y1="anchor.y1-210",
                                           x2="anchor.x1+300", y2="anchor.y1-160")),
                 wait_method="repeat"),

            # 点击平海镇布告栏导航到平海镇布告栏处
            Step("click", Offset(53, 218), "until",
                 Exist("ui/PingHaiZhenBuGaoLan.png",
                       region=Region(win_frame=self.frame, align="center", width_child=600, height_child=400)),
                 wait_method=None),

            # 点击Esc退出布告栏，寻路完成
            Step("press", "esc", "until", NotExist("ui/PingHaiZhenBuGaoLan.png",
                                                   region=Region(win_frame=self.frame, align="center", width_child=600,
                                                                 height_child=400)),
                 wait_method="repeat"),

        ], debug=True)

        # 判断是否有任务
        ...

        # 接任务
        steps_收集炼金资料 = Steps(steps=[
            Step("click", )
        ])
        self.thread = start_threads(self.frame.run_steps, args_list=[steps_寻路至平海镇布告栏处])

        self.frame.get_text_position("与柏宁玛士荣工作板对话")

    def 寻路至仙姑声望(self):
        steps_寻路至平海镇布告栏处 = Steps(steps=[
            # 打开人物属性面板
            Step("press", "ctrl+c", "until", Exist("ui/RWSX.png"), wait_method="repeat"),

            # 切换到声望面板
            Step("click", Offset(x_offset=326, y_offset=18), "until",
                 Exist("门派",
                       region=AnchorRegion(x1="anchor.x1-337", y1="anchor.y1+32",
                                           x2="anchor.x1-143", y2="anchor.y1+69")),
                 wait_method="repeat"),

            # 折叠门派声望
            Step("click", Offset(x_offset=0, y_offset=0), "until",
                 Exist("苏澜郡",
                       region=AnchorRegion(x1="anchor1.x1-4", y1="anchor.y1+5",
                                           x2="anchor1.x1+80", y2="anchor.y1+100")),
                 wait_method="repeat"),

            # 展开苏澜郡声望
            Step("click", Offset(x_offset=0, y_offset=0), "until",
                 Exist("仙菇",
                       region=AnchorRegion(x1="anchor1.x1-16", y1="anchor.y1+170",
                                           x2="anchor1.x1+80", y2="anchor.y1+230")),
                 wait_method="repeat"),

            # 点击仙菇声望
            Step("click", Offset(x_offset=0, y_offset=0), "until",
                 Exist("仙菇",
                       region=AnchorRegion(x1="anchor1.x1+250", y1="anchor.y1-100",
                                           x2="anchor1.x1+380", y2="anchor.y1-55")),
                 wait_method="repeat"),

            # 点击查看声望玩法
            Step("click", Offset(x_offset=468, y_offset=119), "until",
                 Exist("仙菇声望玩法",
                       region=AnchorRegion(x1="anchor1.x1+100", y1="anchor.y1-210",
                                           x2="anchor.x1+300", y2="anchor.y1-160")),
                 wait_method="repeat"),

            # 点击柏宁玛士荣布告栏导航到平海镇布告栏处
            Step("click", Offset(64, 219), "until",
                 Exist("ui/BoNingMaShiRongBuGaoLan.png",
                       region=Region(win_frame=self.frame, align="center", width_child=600, height_child=400)),
                 wait_method=None),

            # 点击Esc退出布告栏，寻路完成
            Step("press", "esc", "until", NotExist("ui/BoNingMaShiRongBuGaoLan.png",
                                                   region=Region(win_frame=self.frame, align="center", width_child=600,
                                                                 height_child=400)),
                 wait_method="repeat"),

        ], debug=True)

    def run(self):
        self.init()
        settings = self.get_value_of_panel(need_dict=True, need_unit=False)
        key = settings.get("打怪技能按键")
        role = settings.get("游戏角色名").strip()
        mode = settings.get("打怪模式")
        freq = float(settings.get("按键频率"))
        # self.frame = Frame(role)
        # link_pos = self.frame.task.get_text_link_pos_global("打开公会")
        # self.frame.show_region(link_pos)
        #
        # self.frame.left_click(*link_pos.get_center(), offset=(16, 0))
        # self.frame.dm.unbind_window()
        if mode == "无脑打怪":
            steps_重复按键 = Steps(
                steps=[
                    Step("press", key, None, None),
                ]
            )
        else:
            steps_重复按键 = Steps(
                steps=[
                    Step("press", key, "until",
                         NotExist("竹林偷伐者", last_time=20, region=Region(align="center", width_child=600)),
                         wait_method="repeat"),
                    Step("double-press", "space", "until",
                         Exist("竹林偷伐者", last_time=60, interval=10, region=Region(align="center", width_child=600)),
                         wait_method="repeat"),
                ]
            )
        self.thread = start_threads(self.frame.run_steps_forever, args_list=[steps_重复按键, freq])
        self._input_panel.get_button("运行").setDisabled(True)
        self._input_panel.get_button("停止").setDisabled(False)

    def stop(self):
        stop_threads(self.thread)
        self.running = False
        logger.debug(f"停止挂机")
        self._input_panel.get_button("停止").setDisabled(True)
        self._input_panel.get_button("运行").setDisabled(False)

    def remove_step(self):
        ...


run_app(MainWindow)
