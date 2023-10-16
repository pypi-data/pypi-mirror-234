import datetime
from enum import Enum
from typing import Optional
import numpy as np
import pandas as pd
from yangke.common.config import logger
from yangke.sis.dll_file import read_data, init_dbp_api, get_tag_value
from yangke.base import get_key_value, execute_function_every_day


class Duty:
    def __init__(self, turns="4值3倒", time_section=None, batch=2):
        """
        电厂运行排班计划类，目前只适用于turns="4值3倒"
        示例：
        time_section = {
                "甲": ("2022-02-25 1:00", "2022-02-25 8:00"),
                "丁": ("2022-02-25 8:00", "2022-02-25 16:00"),
                "丙": ("2022-02-25 16:00", "2022-02-26 1:00"),  # 跨天的班必须放在最后一个
            }
        duty = Duty(4, time_section=time_section)

        :param turns: 值数
        :param time_section:
        :param batch=2: 两天一换班，例如4值3倒，则为 甲丁丙 甲丁丙 乙甲丁 乙甲丁 丙乙甲 丙乙甲 丁丙乙 丁丙乙 甲丁丙 甲丁丙
        """
        if time_section is None:
            time_section = {
                "甲": ("2022-06-01 1:00", "2022-06-01 8:00"),
                "丁": ("2022-06-01 8:00", "2022-06-01 16:00"),
                "丙": ("2022-06-01 16:00", "2022-06-02 1:00"),
            }
        start_date_time = None
        self.turns_duty = []
        day_turn = []
        for k, v in time_section.items():
            day_turn.append(k)
            if isinstance(v[0], str):
                start_time = pd.to_datetime(v[0])
                end_time = pd.to_datetime(v[1])
                time_section.update({k: (start_time, end_time)})
                if start_date_time is None:
                    start_date_time = start_time

        self.time_section = time_section
        self.start_date_time = start_date_time  # 排班开始的日期，从该日期计算循环天数
        self.day_turn = None
        if turns == "4值3倒":
            self.turns_num_duty = 3  # 1天3个值班时间段
            self.turns_num_people = 4  # 4班人马
            self.period = 8
            _ = {"甲", "乙", "丙", "丁"} - set(day_turn)
            day_turn.append(_.pop())
            self.day_turn = day_turn * self.period
            self.day_turn = np.array(self.day_turn)[:int(self.period / 2) * self.turns_num_duty]
            self.day_turn = self.day_turn.reshape((int(self.period / 2), self.turns_num_duty))
            self.day_turn = np.hstack((self.day_turn, self.day_turn))
            self.day_turn = self.day_turn.reshape(self.period, self.turns_num_duty)
        elif turns == "5值4倒":
            self.turns_num_duty = 4  # 1天4个值班时间段
            self.turns_num_people = 5  # 5班人马
            self.period = 8  # 周期数不对
        elif turns == "5值3倒":
            self.turns_num_duty = 3  # 1天3个值班时间段
            self.turns_num_people = 5  # 5班人马
            self.period = 8  # 周期数不对

    def get_turns(self, date_time: Optional[str] = None):
        """
        查询给定时间的值次，返回”甲、乙、丙、丁"等

        :param date_time:
        :return:
        """
        if date_time is None:
            date_time = datetime.datetime.now()
        # 将date_time转换为pd.TimeStamp对象
        if isinstance(date_time, str):
            date_time = pd.to_datetime(date_time)
        elif isinstance(date_time, datetime.datetime):
            date_time = pd.to_datetime(date_time)

        time_index = self.get_time_index(date_time)
        delta_days = (date_time - self.start_date_time).days
        delta_days = delta_days % self.period  # 时间差对周期求余
        return self._get_turns(delta_days, time_index)

    def _get_turns(self, day_idx, time_idx):
        """
        获得一个周期中，第day_idx天第time_idx个班的班序号

        :param day_idx:
        :param time_idx:
        :return:
        """
        day_turn = self.day_turn[day_idx]
        return day_turn[time_idx]

    def get_time_index(self, time):
        """
        计算当前时间是当天的第几个班
        self.get_time_index(pd.to_datetime("20220625 3:12"))

        :param time: 时间标签
        :return:
        """
        time = pd.to_datetime(time).time()
        i = 0
        for k, v in self.time_section.items():
            if v[0].time() < v[1].time():
                if v[0].time() <= time < v[1].time():
                    return i
            else:  # 该种情况下v[1]是第二天的时间，因此不再参与判断
                if v[0].time() <= time:
                    return i
                elif time < v[1].time():
                    return i
            i = i + 1


@get_key_value
class TagsSmallIndexR(Enum):
    发电气耗1 = ""
    厂用电率1 = ""
    排烟温度1 = ""
    主汽温度1 = ""
    除盐水耗1 = ""

    发电气耗理论值1 = ""
    厂用电率理论值1 = ""
    排烟温度理论值1 = ""
    主汽温度理论值1 = ""
    除盐水耗理论值1 = ""

    发电气耗目标值1 = ""
    厂用电率目标值1 = ""
    排烟温度目标值1 = ""
    主汽温度目标值1 = ""
    除盐水耗目标值1 = ""

    发电气耗奖励次数1 = ""
    厂用电率奖励次数1 = ""
    排烟温度奖励次数1 = ""
    主汽温度奖励次数1 = ""
    除盐水耗奖励次数1 = ""

    发电气耗2 = ""
    厂用电率2 = ""
    排烟温度2 = ""
    主汽温度2 = ""
    除盐水耗2 = ""

    发电气耗理论值2 = ""
    厂用电率理论值2 = ""
    排烟温度理论值2 = ""
    主汽温度理论值2 = ""
    除盐水耗理论值2 = ""

    发电气耗目标值2 = ""
    厂用电率目标值2 = ""
    排烟温度目标值2 = ""
    主汽温度目标值2 = ""
    除盐水耗目标值2 = ""

    发电气耗奖励次数2 = ""
    厂用电率奖励次数2 = ""
    排烟温度奖励次数2 = ""
    主汽温度奖励次数2 = ""
    除盐水耗奖励次数2 = ""

    发电气耗3 = ""
    厂用电率3 = ""
    排烟温度3 = ""
    主汽温度3 = ""
    除盐水耗3 = ""

    发电气耗理论值3 = ""
    厂用电率理论值3 = ""
    排烟温度理论值3 = ""
    主汽温度理论值3 = ""
    除盐水耗理论值3 = ""

    发电气耗目标值3 = ""
    厂用电率目标值3 = ""
    排烟温度目标值3 = ""
    主汽温度目标值3 = ""
    除盐水耗目标值3 = ""

    发电气耗奖励次数3 = ""
    厂用电率奖励次数3 = ""
    排烟温度奖励次数3 = ""
    主汽温度奖励次数3 = ""
    除盐水耗奖励次数3 = ""

    化学制水量 = ""
    化学制水量理论值 = ""
    化学制水量目标值 = ""
    化学制水奖励次数 = ""


def cal_tag(unit=1):  # 厂用电，每个整点的0:00、15:00、30:00、45:00运行一次
    """

    :param max_value:
    :param min_value:
    :param tag:
    :return:
    """

    snapshot = read_data(TagsSmallIndexR)
    dbp = init_dbp_api()
    tags = TagsSmallIndexR.get_values
    des = TagsSmallIndexR.get_keys
    end_time = datetime.datetime.now()
    start_time = end_time - datetime.timedelta(minutes=15)
    值编号 = duty.get_turns(start_time)
    his_value = dbp.get_his_value(tags=tags, tags_description=des, start_time=start_time, end_time=end_time)
    his_value = his_value.mean()

    gas_consume_bonus = get_tag_value(snapshot, TagsSmallIndexR.发电气耗奖励次数)
    _1 = get_tag_value(snapshot, TagsSmallIndexR.发电气耗理论值)
    _2 = get_tag_value(snapshot, TagsSmallIndexR.发电气耗目标值)
    if his_value["发电气耗"] < _2:
        gas_consume_bonus += 1

    厂用电率奖励次数 = get_tag_value(snapshot, TagsSmallIndexR.厂用电率奖励次数)
    _1 = get_tag_value(snapshot, TagsSmallIndexR.厂用电率理论值)
    _2 = get_tag_value(snapshot, TagsSmallIndexR.厂用电率目标值)
    if his_value["厂用电率"] < _2:
        厂用电率奖励次数 += 1

    排烟温度奖励次数 = get_tag_value(snapshot, TagsSmallIndexR.排烟温度奖励次数)
    _1 = get_tag_value(snapshot, TagsSmallIndexR.排烟温度理论值)  # 85
    _2 = get_tag_value(snapshot, TagsSmallIndexR.排烟温度目标值)  # 90
    if _1 < his_value["排烟温度"] < _2 and not punish_排烟温度:
        排烟温度奖励次数 += 1

    主汽温度奖励次数 = get_tag_value(snapshot, TagsSmallIndexR.主汽温度奖励次数)
    _1 = get_tag_value(snapshot, TagsSmallIndexR.主汽温度理论值)
    _2 = get_tag_value(snapshot, TagsSmallIndexR.主汽温度目标值)
    if _2 < his_value["主汽温度"] < _1 and not punish_主汽温度:
        主汽温度奖励次数 += 1

    除盐水耗奖励次数 = get_tag_value(snapshot, TagsSmallIndexR.除盐水耗奖励次数)
    _1 = get_tag_value(snapshot, TagsSmallIndexR.除盐水耗理论值)
    _2 = get_tag_value(snapshot, TagsSmallIndexR.除盐水耗目标值)
    if his_value["除盐水耗"] < _2:
        除盐水耗奖励次数 += 1





if __name__ == "__main__":
    xyz = [[1, 2, 1], [2, 3, 1], [4, 2, 5]]
    x, y, z = xyz_split(xyz)
    print(x)
    # time_section = {
    #     "甲": ("2022-02-25 1:00", "2022-02-25 8:00"),
    #     "丁": ("2022-02-25 8:00", "2022-02-25 16:00"),
    #     "丙": ("2022-02-25 16:00", "2022-02-26 1:00"),
    # }
    # duty = Duty()
    # logger.debug(duty.get_turns("20220608 19:00"))
