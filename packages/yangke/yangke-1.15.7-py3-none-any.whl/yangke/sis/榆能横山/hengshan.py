import pandas as pd
import numpy as np

from yangke.common.config import logger
from yangke.sis.榆能横山.tags import (get_backpressure, get_opt_type, TagsRead, TagsWrite, load_data,
                                  get_flowrate, get_pump_power, get_dpower_per_kpa, get_coal_consume, )
from yangke.dataset.PIDB import PIDB
from yangke.sis.dll_file import get_tag_value, ColdResult
from yangke.base import execute_function_by_interval
import datetime

_ = load_data(r"D:\LDYH\冷端优化软件输入数据.xlsx")
backpressure, type_opt_df, pump_info, coal_info = _
db = PIDB()
cold_result = ColdResult()
cold_result.设置背压标签(["最优运行方式下背压1", "最优运行方式下背压2", "优化后机组节煤量1",
                    "优化后机组节煤量2"])  # 背压标签的值不会受到cold_result.平抑波动()方法影响
allowed_range = [("power1", "±10"), ("temp1", "±4"), ("power2", "±10"), ("temp2", "±2")]  # 1、2号机的参数分别判断
cold_result.设置允许的运行参数波动范围(allowed_range)
计时器1号机 = {}
计时器2号机 = {}


def get_average_value(values):
    """
    求数组的平均值，并希望能删除明显偏离正常值的错误数据

    :param values:
    :return:
    """
    if isinstance(values, list):
        values = np.array(values)
        average = values.mean()
        return average


def get_pump_type_str(pump1_I, pump4_I, pump2_IH, pump2_IL, pump3_IH, pump3_IL, need_detail=False):
    高速台数 = 0
    低速台数 = 0
    detail = {}
    if pump1_I > 10:
        高速台数 = 高速台数 + 1
        detail.update({1: "高速"})
    else:
        detail.update({1: "关"})
    if pump4_I > 10:
        高速台数 += 1
        detail.update({4: "高速"})
    else:
        detail.update({4: "关"})
    if pump2_IH > 10:
        高速台数 += 1
        detail.update({2: "高速"})
    elif pump2_IL > 10:
        低速台数 += 1
        detail.update({2: "低速"})
    else:
        detail.update({2: "关"})
    if pump3_IH > 10:
        高速台数 += 1
        detail.update({3: "高速"})
    elif pump3_IL > 10:
        低速台数 += 1
        detail.update({3: "低速"})
    else:
        detail.update({3: "关"})

    if (高速台数, 低速台数) == (4, 0):
        type_ = "四台高速"
    elif (高速台数, 低速台数) == (3, 1):
        type_ = "三高一低"
    elif (高速台数, 低速台数) == (2, 2):
        type_ = "两高两低"
    elif (高速台数, 低速台数) == (3, 0):
        type_ = "三台高速"
    elif (高速台数, 低速台数) == (2, 1):
        type_ = "两高一低"
    elif (高速台数, 低速台数) == (1, 2):
        type_ = "一高两低"
    elif (高速台数, 低速台数) == (2, 0):
        type_ = "两台高速"
    elif (高速台数, 低速台数) == (1, 1):
        type_ = "一高一低"
    elif (高速台数, 低速台数) == (0, 2):
        type_ = "两台低速"
    elif (高速台数, 低速台数) == (0, 1):
        type_ = "一台低速"
    elif (高速台数, 低速台数) == (0, 0):
        type_ = "泵全停"
    elif (高速台数, 低速台数) == (1, 0):
        type_ = "一台高速"
    else:
        type_ = "未知方式"
    if need_detail:
        return type_, detail
    else:
        return type_


def get_pump_type_int(type_: str):
    if type_ == "四台高速":
        return 4, 0
    elif type_ == "三高一低":
        return 3, 1
    elif type_ == "两高两低":
        return 2, 2
    elif type_ == "三台高速":
        return 3, 0
    elif type_ == "两高一低":
        return 2, 1
    elif type_ == "一高两低":
        return 1, 2
    elif type_ == "两台高速":
        return 2, 0
    elif type_ == "一高一低":
        return 1, 1
    elif type_ == "两台低速":
        return 0, 2
    elif type_ == "一台低速":
        return 0, 1
    elif type_ == "泵全停":
        return 0, 0
    elif type_ == "一台高速":
        return 1, 0
    else:
        return 0, 0


def cal_group(unit, snapshot):
    power = get_tag_value(snapshot, f"发电机功率{unit}", 0)
    pump1_I = get_tag_value(snapshot, f"机组{unit}循环水泵1电流", 0)
    pump4_I = get_tag_value(snapshot, f"机组{unit}循环水泵4电流", 0)  # 1、4为定速泵
    pump2_IL = get_tag_value(snapshot, f"机组{unit}循环水泵2低速电流", 0)
    pump2_IH = get_tag_value(snapshot, f"机组{unit}循环水泵2高速电流", 0)
    pump3_IL = get_tag_value(snapshot, f"机组{unit}循环水泵3低速电流", 0)
    pump3_IH = get_tag_value(snapshot, f"机组{unit}循环水泵3高速电流", 0)
    type_, detail = get_pump_type_str(pump1_I, pump4_I, pump2_IH, pump2_IL, pump3_IH, pump3_IL, need_detail=True)
    changed = []
    if unit == 1:
        计时器 = 计时器1号机
    else:
        计时器 = 计时器2号机
    if 计时器.get("last_state") is None:  # 初始状态
        计时器.update({"last_state_time": datetime.datetime.now(),
                    "last_state": detail, "initial_state": True})
        计时器.update({"last_state_time1": datetime.datetime.now(), "last_state1": detail.get(1)})
        计时器.update({"last_state_time2": datetime.datetime.now(), "last_state2": detail.get(2)})
        计时器.update({"last_state_time3": datetime.datetime.now(), "last_state3": detail.get(3)})
        计时器.update({"last_state_time4": datetime.datetime.now(), "last_state4": detail.get(4)})
    elif 计时器.get("last_state") == detail:  # 状态未发生变化
        pass
    else:
        # 说明机组冷端运行方式发生变化
        last_detail = 计时器.get("last_state")
        detail1 = last_detail[1]
        detail2 = last_detail[2]
        detail3 = last_detail[3]
        detail4 = last_detail[4]
        if detail1 != detail.get(1):
            changed.append(1)
            计时器.update({"last_state_time1": datetime.datetime.now(), "last_state1": detail.get(1)})
        if detail2 != detail.get(2):
            changed.append(2)
            计时器.update({"last_state_time2": datetime.datetime.now(), "last_state2": detail.get(2)})
        if detail3 != detail.get(3):
            changed.append(3)
            计时器.update({"last_state_time3": datetime.datetime.now(), "last_state3": detail.get(3)})
        if detail4 != detail.get(4):
            changed.append(4)
            计时器.update({"last_state_time4": datetime.datetime.now(), "last_state4": detail.get(4)})

        计时器.update({"last_state_time": datetime.datetime.now(),
                    "last_state": detail, "initial_state": False})
    # elif unit == 2:
    #     if 计时器2号机.get("last_state") is None:
    #         计时器2号机.update({"last_state_time": datetime.datetime.now(),
    #                        "last_state": type_, "initial_state": True})
    #     elif 计时器2号机.get("last_state") == type_:
    #         pass
    #     elif 计时器2号机.get("last_state") != type_:
    #         # 说明1号机组冷端运行方式发生变化
    #         计时器2号机.update({"last_state_time": datetime.datetime.now(),
    #                        "last_state": type_, "initial_state": False})

    # temp0 = get_tag_value(snapshot, f"机组{unit}环境温度1", 0)
    # temp1 = get_tag_value(snapshot, f"机组{unit}环境温度2", 0)
    # temp2 = get_tag_value(snapshot, f"机组{unit}环境温度3", 0)
    # temp3 = get_tag_value(snapshot, f"机组{unit}环境温度4", 0)
    # temp4 = get_tag_value(snapshot, f"机组{unit}环境温度5", 0)
    # temp5 = get_tag_value(snapshot, f"机组{unit}环境温度6", 0)
    # temp6 = get_tag_value(snapshot, f"机组{unit}环境温度7", 0)
    # temp7 = get_tag_value(snapshot, f"机组{unit}环境温度8", 0)
    # temp8 = get_tag_value(snapshot, f"机组{unit}环境温度9", 0)
    pres0 = get_tag_value(snapshot, f"机组{unit}大气压力1", 95)
    pres1 = get_tag_value(snapshot, f"机组{unit}大气压力2", 95)
    t_cyc_cold_1 = get_tag_value(snapshot, f"机组{unit}低压凝汽器循环水进水温度1", 0)
    t_cyc_cold_2 = get_tag_value(snapshot, f"机组{unit}低压凝汽器循环水进水温度2", 0)
    pres = get_average_value([pres0, pres1])
    bp_true = get_tag_value(snapshot, f"机组{unit}凝汽器真空", 0) + pres
    temp_group = get_average_value([t_cyc_cold_1, t_cyc_cold_2])  # 冷却塔出塔水温平均值

    if power > 300:
        type_opt = get_opt_type(power, temp_group, type_opt_df)
        bp_opt = get_backpressure(power, type_opt, temp_group, backpressure)
        bp_理论值 = get_backpressure(power, type_, temp_group, backpressure)
        pump_power_opt = get_pump_power(type_opt, pump_info)
        pump_power_true = get_pump_power(type_, pump_info)
        flowrate_opt = get_flowrate(type_opt, pump_info)
        _ = get_dpower_per_kpa(power, coal_info)
        出力增加值 = -_ * (bp_opt - bp_理论值)  # 当冷端功率增加时，出力也增加
        冷端功率增加值 = pump_power_opt - pump_power_true
        dpower = 出力增加值 - 冷端功率增加值  # 出力增加值-循泵耗功增加值
        coal_save = dpower / power / 1000 * get_coal_consume(power, coal_info)

        _opt = (type_opt, bp_opt, pump_power_opt, flowrate_opt, coal_save, dpower)
        _true = (power, temp_group, pump_power_true, bp_true, bp_理论值, type_, changed)
    else:  # 停机不运算
        _opt = (0, 0, 0, 0, 0, 0)
        _true = (power, temp_group, 0, 0, bp_true, "泵全停", [])
    return _opt, _true


def transfer_pump_type(type_):
    if type_ == "四台高速":
        return 2, 2, 2, 2
    elif type_ == "三高一低":
        return 2, 2, 1, 2
    elif type_ == "两高两低":
        return 2, 1, 1, 2
    elif type_ == "三台高速":
        return 2, 2, 0, 2
    elif type_ == "两高一低":
        return 2, 0, 1, 2
    elif type_ == "一高两低":
        return 2, 1, 1, 0
    elif type_ == "两台高速":
        return 2, 0, 0, 2
    elif type_ == "一高一低":
        return 2, 0, 1, 0
    elif type_ == "两台低速":
        return 0, 1, 1, 0
    elif type_ == "一台低速":
        return 0, 0, 1, 0
    elif type_ == "一台高速":
        return 2, 0, 0, 0
    else:
        return 0, 0, 0, 0


def time_delta_2_hour_minute(time_delta: datetime.timedelta):
    seconds = time_delta.seconds
    days = time_delta.days
    minutes = seconds // 60  # 总的分钟数
    hours = minutes // 60 + days * 24  # 总的小时数
    minutes = minutes % 60  # 总的分钟数对60求余为剩余的分钟数
    return hours, minutes


def optimize():
    snapshot = db.get_snapshot(tags=TagsRead.get_values(), description=TagsRead.get_keys())
    _opt, _real = cal_group(1, snapshot)
    type_opt1, bp_opt1, pump_power_opt1, flowrate_opt1, coal_save1, dpower1 = _opt
    power1, temp1, pump_power1, bp_true1, bp_理论值1, type1_, changed1 = _real
    _opt, _real = cal_group(2, snapshot)
    type_opt2, bp_opt2, pump_power_opt2, flowrate_opt2, coal_save2, dpower2 = _opt
    power2, temp2, pump_power2, bp_true2, bp_理论值2, type2_, changed2 = _real

    pump11, pump12, pump13, pump14 = transfer_pump_type(type_opt1)
    pump21, pump22, pump23, pump24 = transfer_pump_type(type_opt2)

    opt_res = {
        "type_opt1": type_opt1,
        "pump11_unit1": pump11,  # 分机组平抑波动时，变量名最后一个字符必须与机组编号相同
        "pump12_unit1": pump12,
        "pump13_unit1": pump13,
        "pump14_unit1": pump14,
        "bp_opt1": bp_opt1,
        "pump_power_opt1": pump_power_opt1,
        "flowrate_opt1": flowrate_opt1,
        "coal_save1": coal_save1,
        "dpower1": dpower1,

        "type_opt2": type_opt2,
        "pump21_unit2": pump21,  # 分机组平抑波动时，变量名最后一个字符必须与机组编号相同
        "pump22_unit2": pump22,
        "pump23_unit2": pump23,
        "pump24_unit2": pump24,
        "bp_opt2": bp_opt2,
        "pump_power_opt2": pump_power_opt2,
        "flowrate_opt2": flowrate_opt2,
        "coal_save2": coal_save2,
        "dpower2": dpower2,

    }

    true_res = {
        "power1": power1,
        "temp1": temp1,
        "power2": power2,
        "temp2": temp2,
    }

    cold_result.pass_result(opt_result=opt_res, true_state=true_res)
    cold_result.平抑波动(unit=[1, 2])
    output_res = cold_result.opt_result

    if not 计时器1号机.get("initial_state"):
        time_now = datetime.datetime.now()
        time_last_state1 = 计时器1号机.get("last_state_time1")
        time_last_state2 = 计时器1号机.get("last_state_time2")
        time_last_state3 = 计时器1号机.get("last_state_time3")
        time_last_state4 = 计时器1号机.get("last_state_time4")
        time_delta1 = time_now - time_last_state1
        time_delta2 = time_now - time_last_state2
        time_delta3 = time_now - time_last_state3
        time_delta4 = time_now - time_last_state4
        hour11, minute11 = time_delta_2_hour_minute(time_delta1)
        hour21, minute21 = time_delta_2_hour_minute(time_delta2)
        hour31, minute31 = time_delta_2_hour_minute(time_delta3)
        hour41, minute41 = time_delta_2_hour_minute(time_delta4)
        logger.debug(f"{hour11}:{minute11}   {hour21}:{minute21}   {hour31}:{minute31}    {hour41}:{minute41}")
    else:
        hour11, minute11 = 0, 0
        hour21, minute21 = 0, 0
        hour31, minute31 = 0, 0
        hour41, minute41 = 0, 0

    if not 计时器2号机.get("initial_state"):
        time_now = datetime.datetime.now()
        time_last_state1 = 计时器2号机.get("last_state_time1")
        time_last_state2 = 计时器2号机.get("last_state_time2")
        time_last_state3 = 计时器2号机.get("last_state_time3")
        time_last_state4 = 计时器2号机.get("last_state_time4")
        time_delta1 = time_now - time_last_state1
        time_delta2 = time_now - time_last_state2
        time_delta3 = time_now - time_last_state3
        time_delta4 = time_now - time_last_state4
        hour12, minute12 = time_delta_2_hour_minute(time_delta1)
        hour22, minute22 = time_delta_2_hour_minute(time_delta2)
        hour32, minute32 = time_delta_2_hour_minute(time_delta3)
        hour42, minute42 = time_delta_2_hour_minute(time_delta4)
    else:
        hour12, minute12 = 0, 0
        hour22, minute22 = 0, 0
        hour32, minute32 = 0, 0
        hour42, minute42 = 0, 0
    hp1, lp1 = get_pump_type_int(type1_)
    hp2, lp2 = get_pump_type_int(type2_)
    hp1_opt, lp1_opt = get_pump_type_int(type_opt1)
    hp2_opt, lp2_opt = get_pump_type_int(type_opt2)
    res = {
        "建议循泵运行方式11": output_res["pump11_unit1"],
        "建议循泵运行方式12": output_res["pump12_unit1"],
        "建议循泵运行方式13": output_res["pump13_unit1"],
        "建议循泵运行方式14": output_res["pump14_unit1"],
        "建议循泵运行方式21": output_res["pump21_unit2"],
        "建议循泵运行方式22": output_res["pump22_unit2"],
        "建议循泵运行方式23": output_res["pump23_unit2"],
        "建议循泵运行方式24": output_res["pump24_unit2"],
        "最优运行方式下背压1": output_res["bp_opt1"],
        "最优运行方式下背压2": output_res["bp_opt2"],
        "优化后机组节煤量1": output_res["coal_save1"],
        "优化后机组节煤量2": output_res["coal_save2"],
        "净电功率增益1": output_res["dpower1"],
        "净电功率增益2": output_res["dpower2"],
        "循环水流量1": output_res["flowrate_opt1"],
        "循环水流量2": output_res["flowrate_opt2"],
        "循泵总功率1": output_res["pump_power_opt1"],
        "循泵总功率2": output_res["pump_power_opt2"],
        "循泵切换小时数11": hour11,
        "循泵切换分钟数11": minute11,
        "循泵切换小时数21": hour21,
        "循泵切换分钟数21": minute21,
        "循泵切换小时数31": hour31,
        "循泵切换分钟数31": minute31,
        "循泵切换小时数41": hour41,
        "循泵切换分钟数41": minute41,
        "循泵切换小时数12": hour12,
        "循泵切换分钟数12": minute12,
        "循泵切换小时数22": hour22,
        "循泵切换分钟数22": minute22,
        "循泵切换小时数32": hour32,
        "循泵切换分钟数32": minute32,
        "循泵切换小时数42": hour42,
        "循泵切换分钟数42": minute42,

        "高速泵运行台数实时值1": hp1,
        "低速泵运行台数实时值1": lp1,
        "高速泵运行台数推荐值1": hp1_opt,
        "低速泵运行台数推荐值1": lp1_opt,
        "高速泵运行台数实时值2": hp2,
        "低速泵运行台数实时值2": lp2,
        "高速泵运行台数推荐值2": hp2_opt,
        "低速泵运行台数推荐值2": lp2_opt,
        "循泵总功率实际值1": pump_power1,
        "循泵总功率实际值2": pump_power2,

        "阻塞背压1": 0.0052 * power1 - 0.0283,
        "阻塞背压2": 0.0052 * power2 - 0.0283,
    }
    tags_values = {TagsWrite.get(k): res.get(k) for k in res.keys()}
    db.write_snapshot(tags=tags_values.keys(), values=tags_values.values())
    logger.debug("写入SIS成功")


if __name__ == "__main__":
    execute_function_by_interval(optimize, minute=0, second=30, daemon=True)
