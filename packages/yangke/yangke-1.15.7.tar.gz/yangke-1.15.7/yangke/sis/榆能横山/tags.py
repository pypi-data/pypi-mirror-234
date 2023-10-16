import math
from enum import Enum, unique

import pandas as pd

from yangke.base import get_key_value, is_number, interpolate_value_complex, interpolate_value_simple
from yangke.common.config import logger
from yangke.common.fileOperate import read_excel


@unique
@get_key_value
class TagsRead(Enum):
    机组1循环水泵1电流 = "DCS1:PAC20AP001CE"
    机组1循环水泵2高速电流 = "DCS1:PAC20AP002HCE"
    机组1循环水泵2低速电流 = "DCS1:PAC20AP002LCE"
    机组1循环水泵3高速电流 = "DCS1:PAC20AP003HCE"
    机组1循环水泵3低速电流 = "DCS1:PAC20AP003LCE"
    机组1循环水泵4电流 = "DCS1:PAC20AP004CE"

    机组1高压凝汽器压力1 = "DCS1:MAG10CP101"
    机组1高压凝汽器压力2 = "DCS1:MAG10CP102"
    机组1高压凝汽器压力3 = "DCS1:MAG10CP103"
    机组1高压凝汽器压力4 = "DCS1:MAG10CP104"
    机组1低压凝汽器压力1 = "DCS1:MAG20CP101"
    机组1低压凝汽器压力2 = "DCS1:MAG20CP102"
    机组1低压凝汽器压力3 = "DCS1:MAG20CP103"
    机组1低压凝汽器压力4 = "DCS1:MAG20CP104"

    机组1凝汽器真空 = "DCS1:DMNQQZK"
    机组1低压凝汽器循环水进水温度2 = "DCS1:PAB33CT301"
    机组1低压凝汽器循环水进水温度1 = "DCS1:PAB31CT301"
    机组1高压凝汽器循环水出水温度2 = "DCS1:PAB34CT301"
    # 机组1高压凝汽器循环水出水温度1 = "DCS1:PAB32CT302"
    机组1低压凝汽器进水压力 = "DCS1:PAB33CP101"
    机组1高压凝汽器出水压力 = "DCS1:PAB32CP101"
    机组1大气压力1 = "DCS1:PAD00CP101"
    机组1大气压力2 = "DCS1:PAD00CP102"
    # 机组1大气压力3 = "DCS1:PAC00CP103"
    机组1环境温度1 = "DCS1:PAD00CT311"
    机组1环境温度2 = "DCS1:PAD00CT312"
    机组1环境温度3 = "DCS1:PAD00CT313"
    机组1环境温度4 = "DCS1:PAD00CT314"
    机组1环境温度5 = "DCS1:PAD00CT315"
    机组1环境温度6 = "DCS1:PAD00CT316"
    机组1环境温度7 = "DCS1:PAD00CT317"
    机组1环境温度8 = "DCS1:PAD00CT318"
    机组1环境温度9 = "DCS1:PAD00CT319"
    发电机功率1 = "DCS1:LOAD"
    总燃料量1 = "DCS1:TFFREAL"

    机组2循环水泵1电流 = "DCS2:PAC20AP001CE"
    机组2循环水泵2高速电流 = "DCS2:PAC20AP002HCE"
    机组2循环水泵2低速电流 = "DCS2:PAC20AP002LCE"
    机组2循环水泵3高速电流 = "DCS2:PAC20AP003HCE"
    机组2循环水泵3低速电流 = "DCS2:PAC20AP003LCE"
    机组2循环水泵4电流 = "DCS2:PAC20AP004CE"

    机组2高压凝汽器压力1 = "DCS2:MAG10CP101"
    机组2高压凝汽器压力2 = "DCS2:MAG10CP102"
    机组2高压凝汽器压力3 = "DCS2:MAG10CP103"
    机组2高压凝汽器压力4 = "DCS2:MAG10CP104"
    机组2低压凝汽器压力1 = "DCS2:MAG20CP101"
    机组2低压凝汽器压力2 = "DCS2:MAG20CP102"
    机组2低压凝汽器压力3 = "DCS2:MAG20CP103"
    机组2低压凝汽器压力4 = "DCS2:MAG20CP104"

    机组2凝汽器真空 = "DCS2:DMNQQZK"
    机组2低压凝汽器循环水进水温度2 = "DCS2:PAB33CT301"
    机组2低压凝汽器循环水进水温度1 = "DCS2:PAB31CT301"
    机组2高压凝汽器循环水出水温度2 = "DCS2:PAB34CT301"
    # 机组2高压凝汽器循环水出水温度1 = "DCS2:PAB32CT302"
    机组2低压凝汽器进水压力 = "DCS2:PAB33CP101"
    机组2高压凝汽器出水压力 = "DCS2:PAB32CP101"

    机组2大气压力1 = "DCS2:PAD00CP101"
    机组2大气压力2 = "DCS2:PAD00CP102"
    # 机组2大气压力3 = "DCS2:PAC00CP103"
    机组2环境温度1 = "DCS2:PAD00CT311"
    机组2环境温度2 = "DCS2:PAD00CT312"
    机组2环境温度3 = "DCS2:PAD00CT313"
    机组2环境温度4 = "DCS2:PAD00CT314"
    机组2环境温度5 = "DCS2:PAD00CT315"
    机组2环境温度6 = "DCS2:PAD00CT316"
    机组2环境温度7 = "DCS2:PAD00CT317"
    机组2环境温度8 = "DCS2:PAD00CT318"
    机组2环境温度9 = "DCS2:PAD00CT319"
    发电机功率2 = "DCS2:LOAD"
    总燃料量2 = "DCS2:TFFREAL"


@unique
@get_key_value
class TagsWrite(Enum):
    建议循泵运行方式11 = "DCS1:P_NUM_OPT1"
    建议循泵运行方式12 = "DCS1:P_NUM_OPT2"
    建议循泵运行方式13 = "DCS1:P_NUM_OPT3"
    建议循泵运行方式14 = "DCS1:P_NUM_OPT4"
    建议循泵运行方式21 = "DCS2:P_NUM_OPT1"
    建议循泵运行方式22 = "DCS2:P_NUM_OPT2"
    建议循泵运行方式23 = "DCS2:P_NUM_OPT3"
    建议循泵运行方式24 = "DCS2:P_NUM_OPT4"
    最优运行方式下背压1 = "DCS1:BP_Best_Con"
    最优运行方式下背压2 = "DCS2:BP_Best_Con"
    优化后机组节煤量1 = "DCS1:Coal_Saving_Run"
    优化后机组节煤量2 = "DCS2:Coal_Saving_Run"
    循环水流量1 = "DCS1:Cycle_F"
    循环水流量2 = "DCS2:Cycle_F"
    循泵总功率1 = "DCS1:Power_Pump"
    循泵总功率2 = "DCS2:Power_Pump"
    净电功率增益1 = "DCS1:Power_Net_Inc"
    净电功率增益2 = "DCS2:Power_Net_Inc"

    循泵切换小时数11 = "Dcs1:xhsbtime_hour"
    循泵切换分钟数11 = "Dcs1:xhsbtime_minute"
    循泵切换小时数21 = "Dcs1:xhsbtime_hour2"
    循泵切换分钟数21 = "Dcs1:xhsbtime_minute2"
    循泵切换小时数31 = "Dcs1:xhsbtime_hour3"
    循泵切换分钟数31 = "Dcs1:xhsbtime_minute3"
    循泵切换小时数41 = "Dcs1:xhsbtime_hour4"
    循泵切换分钟数41 = "Dcs1:xhsbtime_minute4"
    循泵切换小时数12 = "Dcs2:xhsbtime_hour"
    循泵切换分钟数12 = "Dcs2:xhsbtime_minute"
    循泵切换小时数22 = "Dcs2:xhsbtime_hour2"
    循泵切换分钟数22 = "Dcs2:xhsbtime_minute2"
    循泵切换小时数32 = "Dcs2:xhsbtime_hour3"
    循泵切换分钟数32 = "Dcs2:xhsbtime_minute3"
    循泵切换小时数42 = "Dcs2:xhsbtime_hour4"
    循泵切换分钟数42 = "Dcs2:xhsbtime_minute4"

    高速泵运行台数实时值1 = "DCS1:NUM_CWP_H"
    低速泵运行台数实时值1 = "DCS1:NUM_CWP_L"
    高速泵运行台数推荐值1 = "DCS1:NUM_CWP_H_OPT"
    低速泵运行台数推荐值1 = "DCS1:NUM_CWP_L_OPT"
    高速泵运行台数实时值2 = "DCS2:NUM_CWP_H"
    低速泵运行台数实时值2 = "DCS2:NUM_CWP_L"
    高速泵运行台数推荐值2 = "DCS2:NUM_CWP_H_OPT"
    低速泵运行台数推荐值2 = "DCS2:NUM_CWP_L_OPT"
    循泵总功率实际值1 = "DCS1:Power_Pump_Act"
    循泵总功率实际值2 = "DCS2:Power_Pump_Act"

    阻塞背压1 = "DCS1:BP_ZUSE"
    阻塞背压2 = "DCS2:BP_ZUSE"


def load_data(
        file=r"C:\Users\YangKe\Documents\WPS Cloud Files\217145378\6科研项目\2022\榆能横山\冷端优化软件输入数据.xlsx"):
    """
    加载性能试验优化结果

    :param file:
    :return:
    """
    backpressure = {}
    dfs = read_excel(file=file, need_merge=False, index_col=0)
    for sheet in ["900MW", "800MW", "700MW", "600MW", "500MW", "400MW"]:
        df = dfs[sheet]
        df.dropna(how="all", axis=0, inplace=True)
        backpressure.update({sheet: df})
    type_opt = dfs["最佳运行方式"]
    pump_info = dfs["循泵"]
    coal_info = dfs["煤耗"]
    return backpressure, type_opt, pump_info, coal_info


def get_backpressure(power=450, type_="四台高速", t=23, bp_total=None):
    """
    根据机组负荷、循泵运行方式、循环水温度计算凝汽器背压

    :param power:
    :param type_:
    :param t:
    :return:
    """
    lower_power = math.floor(power / 100) * 100
    upper_power = math.ceil(power / 100) * 100
    if lower_power == 300:  # 小于300MW时，用400和500MW的数据插值计算
        lower_power = 500
    if upper_power == 1100:
        upper_power = 900
    lower_power_idx = str(f"{lower_power}MW")
    upper_power_idx = str(f"{upper_power}MW")
    lower_df = bp_total[lower_power_idx]
    upper_df = bp_total[upper_power_idx]
    if type_ in ["一台高速", "一台低速"]:
        type_ = "两台低速"
    lower_type = lower_df[type_]
    upper_type = upper_df[type_]

    lower_pressure = interpolate_value_complex(t, x_list=[float(i.replace("℃", "")) for i in lower_type.keys()],
                                               y_list=lower_type)
    upper_pressure = interpolate_value_complex(t, x_list=[float(i.replace("℃", "")) for i in upper_type.keys()],
                                               y_list=upper_type)
    pressure = interpolate_value_simple(power, x1=lower_power, y1=lower_pressure, x2=upper_power, y2=upper_pressure)
    return pressure


def get_opt_type(power=460, t=22.5, type_opt=None):
    power_ = round(power / 100) * 100
    power_idx = f"{power_}MW"
    t_ = round(t / 2) * 2
    t_idx = f"{t_}℃"
    return type_opt.loc[t_idx, power_idx]


def get_flowrate(type_, pump_info):
    if type_ not in ["四台高速", "三高一低", "两高两低", "三台高速", "两高一低", "一高两低", "两台高速", "一高一低",
                     "两台低速"]:
        logger.warning(f"查询的循泵运行方式不存在：{type_}")
        return 0
    return pump_info.loc[type_, "循环循环水流量(t/h)"]


def get_pump_power(type_, pump_info):
    if type_ not in ["四台高速", "三高一低", "两高两低", "三台高速", "两高一低", "一高两低", "两台高速", "一高一低",
                     "两台低速"]:
        logger.warning(f"查询的循泵运行方式不存在：{type_}")
        return 0
    return pump_info.loc[type_, "循环水泵功率(kW)"]


def get_coal_consume(power, coal_info):
    """
    计算发电机功率对应的煤耗，功率可以超出coal_info给定的范围，外延插值

    :param power:
    :param coal_info:
    :return:
    """
    x_list = list(coal_info.index)
    y_list = list(coal_info["供电煤耗g/(kW·h)"])
    return interpolate_value_complex(power, x_list=x_list, y_list=y_list)


def get_dpower_per_kpa(power, coal_info):
    """
    计算背压变化1kPa引起的发电机处理变化，功率可以超出coal_info给定的范围，外延插值

    :param power:
    :param coal_info:
    :return:
    """
    x_list = list(coal_info.index)
    y_list = list(coal_info["背压1kPa出力增加（kW）"])
    return interpolate_value_complex(power, x_list=x_list, y_list=y_list)
