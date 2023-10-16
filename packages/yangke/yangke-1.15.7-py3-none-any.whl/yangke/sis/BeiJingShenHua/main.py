import copy
import random

from yangke.performance.iapws97 import get_h_by_pt
from yangke.common.config import logger, add_file_logger
from tags import TagsRead, TagsWrite, get_pump_type_by_int, availableType, get_pump_type_by_char, get_available_type, \
    power_cold, get_less_cold, get_larger_cold
from yangke.sis.dll_file import read_data, get_tag_value, init_write_sis, init_dbp_api
import pandas as pd
from yangke.base import interpolate_nd, interpolate_value_complex, execute_function_by_interval, \
    interpolate_value_simple
import datetime
from yangke.sis.export_history_values import load_history_file, find_condition

add_file_logger()  # 添加日志记录文件
print("last　version：20220913")
debug = False


def Q_热井出水(F_凝结水1, F_凝结水2, F_减温水至杂项, P_热井出水, T_热井出水):
    F_热井出水 = F_凝结水1 + F_凝结水2 - F_减温水至杂项
    H_热井出水 = get_h_by_pt(P_热井出水, T_热井出水)
    return F_热井出水 * H_热井出水 * 1000  # kJ/h


def load_db(db_path=r"D:\ProgramData\lengduan_DB_20210918.xlsx"):
    _ = pd.read_excel(db_path)
    _ = _.dropna(how="any", axis=1)
    data_total = {}
    for 循泵方式 in ["A", "B", "C", "D", "E", "F", "G", "H"]:
        for 风机数量 in [3, 4, 5, 6, 7, 8]:
            value = _[_["循泵方式"] == 循泵方式]
            value = value[value["机力塔数量"] == 风机数量]
            data_total.update({
                f"{循泵方式}{风机数量}": copy.deepcopy(value)
            })
    return data_total


init_write_sis(ip="10.2.128.168", port=12084, user="admin", passwd_str="admin")
data = load_db()
pressure_funcs = {}
# coal_funcs = {}

for 循泵方式 in ["A", "B", "C", "D", "E", "F", "G", "H"]:
    for 风机数量 in [3, 4, 5, 6, 7, 8]:
        state = f"{循泵方式}{风机数量}"
        df = data[state]
        pressure_func = interpolate_nd(dataframe=df, df_x_titles=["凝汽器热负荷", "温度", "湿度"], df_y_title=["背压"])
        # coal_func = interpolate_nd(dataframe=df, df_x_titles=["凝汽器热负荷", "温度", "湿度"], df_y_title=["煤耗"])
        pressure_funcs.update({state: pressure_func})

Qc_C = [  # 凝汽器热负荷-微增出力系数
    [100, 1.7712],
    [150, 1.5629],
    [200, 1.3745],
    [250, 1.2062],
    [300, 1.0578],
    [350, 0.9295],
    [400, 0.8211],
    [450, 0.7328],
    [500, 0.6644],
    [550, 0.6161],
]

power_range = []  # 负荷波动阈值
t_range = []  # 温度波动阈值
heat_range = []  # 热负荷波动阈值
pres_range = []  # 背压变化阈值
time_range = []  # 时间阈值，超过时间范围强制重算
last_state = {}  # 上一个优化状态
last_state_act = "A0"  # 上一个运行状态，初始状态为'A0'
上次冷端运行方式调整时间 = None  # 冷端运行方式调整的时候，调整的时间会被该参数记录
上次冷端运行方式调整时的背压差 = None  # 冷端运行方式调整的时候，最佳真空和真实真空会被该参数记录
time_steady = 1800  # 当运行方式调整后，需要经过time_steady秒背压才能达到稳定状态
his_df = load_history_file(r"D:\ProgramData\历史数据库.xlsx")


def all_in_range(*v_range):
    for v_r in v_range:
        v = list(v_r.keys())[0]
        r = list(v_r.values())[0]
        if r[0] <= v <= r[1]:
            continue
        else:
            return False
    return True


def deal_different_fan(delta, state_max, cur_state, snapshot):
    """
    对不同的风机数量进行修正，只调整优化结果的delta数据
    """
    cur_fan = int(cur_state[1])
    opt_fan = int(state_max[1])
    _state_max = state_max
    p_cur = delta[cur_state]["背压"]
    p_opt = delta[state_max]["背压"]
    p_act = get_tag_value(snapshot, TagsRead.当前背压)
    t_cyc_in1 = get_tag_value(snapshot, TagsRead.凝汽器循环水进水温度1)
    t_cyc_in2 = get_tag_value(snapshot, TagsRead.凝汽器循环水进水温度2)
    t_cyc_in = (t_cyc_in1 + t_cyc_in2) / 2
    t0 = get_tag_value(snapshot, TagsRead.环境温度)
    delta_p = delta[state_max]["背压增加值"] * 0.9
    if cur_fan == opt_fan:
        delta[state_max]["背压"] = p_act
    elif cur_fan - opt_fan > 0:  # 优化结果认为应少开风机
        if delta_p < 0:  # 优化结果运行的风机少，背压增加值应>0
            logger.warning("优化结果背压变化规律错误...")
            delta_p = delta[state_max]["背压增加值"] = -delta_p
        if p_act < 7:
            # 背压增加值按照(1, 0.1), (3, 0.2), (5, 0.5), (7, 1)进行插值
            delta_p_sim = interpolate_value_complex(p_act, [(1, 0.1), (4, 0.2), (5, 0.4), (7, 0.7)])
            delta_p = delta_p * interpolate_value_simple(p_act, 5, 0.7, 7, 1)
            if abs(delta_p / delta_p_sim) > 1.5:  # 说明少开一台风机，背压增加值要远小于理论计算值，因此可以少开风机
                # opt_fan = opt_fan + 1
                # return deal_different_fan(delta, f"{state_max[0]}{opt_fan}", cur_state, p_act)
                delta_p = delta_p_sim
                delta[state_max]["背压增加值"] = delta_p
                delta[state_max]["背压"] = p_opt + delta_p
            else:
                delta_p = (delta_p_sim + delta_p) / 2
                delta[state_max]["背压增加值"] = delta_p
                delta[state_max]["背压"] = p_opt + delta_p
        if p_act > 8:  # 如果当前背压很高时，不应再少开风机
            state_max = cur_state
            delta_p = random.random() / 20
        elif p_act > 9:  # 如果当前背压极高，应该增开冷端设备
            state_max = get_larger_cold(cur_state)
    else:  # 优化结果认为应增开风机
        if delta_p > 0:  # 优化结果要增开风机，背压应下降
            logger.warning("优化结果被压变化规律错误...")
            delta_p = delta[state_max]["背压增加值"] = -delta_p
        if p_act < 7:
            delta_p_sim = - interpolate_value_complex(p_act, [(1, 0.1), (4, 0.2), (5, 0.4), (7, 0.7)]) * abs(
                cur_fan - opt_fan)
            delta_p = delta_p  # * interpolate_value_simple(p_act, 5, 0.7, 7, 1)
            if abs(delta_p / delta_p_sim) > 1.5:  # 说明增开一台风机，背压下降值达不到理论计算值，理论计算结果过于乐观
                delta_p = delta_p_sim
            else:
                delta_p = (delta_p_sim + delta_p) / 2
            delta[state_max]["背压增加值"] = delta_p  # 必须添加该语句，因为后面state_max可能会被修改，而主循环中保持状态不变时，仍会取到该参数
        if p_act < 4.5:  # 实际背压很低时，不应再增开风机
            state_max = cur_state
            delta_p = random.random() / 20
            delta[state_max]["背压增加值"] = delta_p
        if t_cyc_in - (t0 - 1) < 0:  # 如果循环水经机力塔冷却后的温度已经低于环境温度，则说明机力塔可用的冷却潜力不大，
            # 不应再增大风机数量，此处环境温度测点不准，向下修正3℃
            state_max = get_less_cold(cur_state)  # cur_state
            # delta_p = random.random() / 20
            logger.debug(f"环境温度与循环水温差对运行方式调整，{t0=}，{t_cyc_in=}")
        if p_act < 3:  # 实际背压极低时，减小冷端功率
            # 冬季工况，环境温度可低至零下，但循环水冷却后温度可以为20摄氏度左右，此时背压很低，需要减小冷端设备运行
            if power_cold[state_max] >= power_cold[cur_state]:
                state_max = get_less_cold(cur_state)
        elif p_act > 9:
            if power_cold[state_max] <= power_cold[cur_state]:
                state_max = get_larger_cold(cur_state)

    if state_max == _state_max:
        delta[state_max]["背压增加值"] = delta_p
        delta[state_max]["背压"] = p_act + delta_p  # 预测背压 = 真实背压 + 理论背压差
    delta[cur_state]["背压增加值"] = random.random() / 20
    delta[cur_state]["背压"] = p_act + delta[cur_state]["背压增加值"]
    return delta, state_max


def deal_different_pump(delta, state_max, cur_state, snapshot):
    return delta, state_max


def deal_different_pump_and_fan(delta, state_max, cur_state, snapshot):
    pc_max = delta[state_max]["冷端耗功增加"]
    pc_cur = delta[cur_state]["冷端耗功增加"]
    _state_max = state_max
    p_act = get_tag_value(snapshot, TagsRead.当前背压)
    p_cur = delta[cur_state]["背压"]
    p_opt = delta[state_max]["背压"]
    delta_p = delta[state_max]["背压增加值"]
    p_act = get_tag_value(snapshot, TagsRead.当前背压)
    delta_p_sim = interpolate_value_complex(p_act, [(1, 0.1), (4, 0.2), (5, 0.4), (7, 0.7)]) * abs(
        pc_max / 230)  # 按冷端功率折算的背压变化
    if pc_max - pc_cur > 0:
        # 优化结果耗功增加，则背压必须降低
        if delta_p > 0:
            delta_p = -abs(delta_p_sim / 2)
        else:
            delta_p = -(abs(delta_p) + delta_p_sim) / 2
    else:
        # 优化结果耗功降低，则背压一般会上升
        if delta_p < 0:
            delta_p = abs(delta_p_sim) / 4
        else:
            delta_p = (delta_p + delta_p_sim / 2) / 2

    if p_act < 3:  # 实际背压极低时，减小冷端功率
        # 冬季工况，环境温度可低至零下，但循环水冷却后温度可以为20摄氏度左右，此时背压很低，需要减小冷端设备运行
        if power_cold[state_max] >= power_cold[cur_state]:
            state_max = get_less_cold(cur_state)
    elif p_act > 8.5:
        if power_cold[state_max] <= power_cold[cur_state]:
            state_max = get_larger_cold(cur_state)

    if state_max == _state_max:  # 如果没有调整优化结果的运行方式
        delta[state_max]["背压增加值"] = delta_p
        delta[state_max]["背压"] = p_act + delta_p  # 预测背压 = 真实背压 + 理论背压差
    return delta, state_max


def get_delta_coal(flow_ng, power_total, power_delta):
    """
    计算煤耗降低值
    flow_ng: Nm3/h，天然气流量
    power_total: MW，全厂总功率
    power_delta: kW，冷端优化产生的净功率增加值
    """
    flow_coal = flow_ng * 35588 / 29307  # kg/h
    coal1 = flow_coal / power_total  # g/(kWh)
    power_total2 = power_total + power_delta / 1000
    coal2 = flow_coal / power_total2
    return coal1 - coal2, coal1


def get_backpressure_by_history(Qc, t0, humid, state):
    unit_condition = [("凝汽器热负荷", Qc, "1%"), ("环境温度", t0, "±2"), ("环境湿度", humid, "±10")]
    cold_condition = {"循泵方式": state[0], "机力塔数量": int(state[1])}
    df: pd.DataFrame = find_condition(his_df, unit_condition, cold_condition, False)
    if df is not None:
        return df.mean(numeric_only=True)["当前背压"]
    else:
        return None


def dispatch_delta_p(delta, state_max, snapshot, xi_now):
    """
    处理冷端运行方式调整后，背压变化的动态过程
    """
    global 上次冷端运行方式调整时的背压差, time_steady, last_state
    delta_p = delta[state_max]["背压增加值"]  # 当前步计算得到的背压变化值
    if 上次冷端运行方式调整时的背压差 is None:  # 必然不是None，每次调整冷端运行方式时，该值都会被设置，这里是为了保险，不让程序出错
        上次冷端运行方式调整时的背压差 = last_state[state_max]["背压增加值"]  # 上一步优化结果中的背压变化值
    now = datetime.datetime.now()
    delta_time_seconds = (now - 上次冷端运行方式调整时间).seconds  # 距离上次调整时间的秒数
    冷端运行方式调整导致的背压变化 = interpolate_value_simple(delta_time_seconds, 0, 上次冷端运行方式调整时的背压差,
                                                              time_steady, delta_p)  # (x, 0, -0.51, 1800, 0)

    delta[state_max]["背压增加值"] = 冷端运行方式调整导致的背压变化
    return delta


def cal_coal_save(snapshot, 推荐背压, pres_act, cur_state, 最佳运行状态, Q_c):
    power_total = get_tag_value(snapshot, TagsRead.全厂总功率, 10)
    power_steam = get_tag_value(snapshot, TagsRead.发电机有功功率_steam, 102)
    flow_ng = get_tag_value(snapshot, TagsRead.计量单元天然气流量1)
    flow_ng = flow_ng + get_tag_value(snapshot, TagsRead.计量单元天然气流量2)
    flow_ng = flow_ng + get_tag_value(snapshot, TagsRead.计量单元天然气流量3)
    flow_ng = flow_ng  # 天然气流量 Nm3/h
    c0 = interpolate_value_complex(Q_c, Qc_C)
    delta_wt = power_steam * (pres_act - 推荐背压) * c0 * 10  # kW，如果组合背压大于基准背压，则微增出力<0，该值为出力增加量
    delta_wc = power_cold[最佳运行状态] - power_cold[cur_state]
    return get_delta_coal(flow_ng, power_total, (delta_wt - delta_wc))


def optimize():
    """
    执行一次优化任务

    :return:
    """
    snapshot = read_data(TagsRead)
    power1 = get_tag_value(snapshot, TagsRead.燃机功率1, 10)
    power2 = get_tag_value(snapshot, TagsRead.燃机功率2, 10)
    power_total = get_tag_value(snapshot, TagsRead.全厂总功率, 10)
    热网疏水流量 = get_tag_value(snapshot, TagsRead.热网加热器疏水流量1, 0) \
                   + get_tag_value(snapshot, TagsRead.热网加热器疏水流量2, 0)
    t0 = get_tag_value(snapshot, TagsRead.环境温度, 24)
    t0 = -5 if t0 < -5 else t0
    t0 = 35 if t0 > 35 else t0
    p0 = get_tag_value(snapshot, TagsRead.大气压力, 1000) / 10000  # MPa
    humid = get_tag_value(snapshot, TagsRead.环境湿度, 58) / 100
    humid = 0.2 if humid < 0.2 else humid
    humid = 0.9 if humid > 0.9 else humid
    now = datetime.datetime.now()
    # Q_供热 = get_tag_value(snapshot, TagsRead.供热热量, 12)  # GJ/h
    Q_供热1 = init_dbp_api().get_his_value(tags="ldyh.rwjl1-17", tags_description="供热热量",
                                           start_time=now - datetime.timedelta(days=0, hours=0, minutes=10),
                                           end_time=now).copy()
    Q_供热 = Q_供热1.mean(numeric_only=True).values[0]  # 供热数据取十分钟平均值，因为供热数据在锯齿状波动
    # ------------------------- 烟气热网加热器供热量计算Q_flue -----------------------------
    F_flue_heater = get_tag_value(snapshot, TagsRead.烟气热网加热器进水流量, 0)
    if power1 > 20 and power2 > 20:  # 1、2号燃机均开机
        F_fh1 = F_fh2 = F_flue_heater / 2
    elif power1 > 20:  # 1号机运行，2号机停机
        F_fh1 = F_flue_heater
        F_fh2 = 0
    elif power2 > 20:  # 1号机停机，2号机运行
        F_fh1 = 0
        F_fh2 = F_flue_heater
    else:  # 两台机均停机
        F_fh1 = F_fh2 = 0
    P_fh = get_tag_value(snapshot, TagsRead.烟气热网加热器进水压力, 0.09) + p0
    T_fh1_in = get_tag_value(snapshot, TagsRead.烟气热网加热器进水温度1)
    T_fh1_out = get_tag_value(snapshot, TagsRead.烟气热网加热器供水温度1)
    T_fh2_in = get_tag_value(snapshot, TagsRead.烟气热网加热器进水温度2)
    T_fh2_out = get_tag_value(snapshot, TagsRead.烟气热网加热器供水温度2)
    H_fh1_in = get_h_by_pt(P_fh, T_fh1_in)
    H_fh1_out = get_h_by_pt(P_fh, T_fh1_out)
    H_fh2_in = get_h_by_pt(P_fh, T_fh2_in)
    H_fh2_out = get_h_by_pt(P_fh, T_fh2_out)
    Q_flue = (F_fh1 * (H_fh1_out - H_fh1_in) + F_fh2 * (H_fh2_out - H_fh2_in)) * 1000
    # ------------------------- 烟气热网加热器供热量计算Q_flue -----------------------------
    # Q_供热 = 0 if 热网疏水流量 < 5 else Q_供热  # 说明供热不是由连通管抽汽带的
    # Q_供热 = 0 if Q_供热 < 60 else Q_供热 - 60  # GJ/h，从供热热量中减去烟气余热利用提供的热量
    Q_供热 = Q_供热 * 1000000 - Q_flue
    Q_供热 = 0 if Q_供热 < 0 else Q_供热
    _p = get_tag_value(snapshot, TagsRead.热井出水压力, 0.0415) + p0
    _t = get_tag_value(snapshot, TagsRead.热井出水温度, 34.435)
    F_condense1 = get_tag_value(snapshot, TagsRead.凝结水流量1号炉, 0) if power1 > 20 else 0
    F_condense2 = get_tag_value(snapshot, TagsRead.凝结水流量2号炉, 298.588) if power2 > 20 else 0
    F_other = 0  # 凝结水疏水至杂项取0
    Q_wellout = Q_热井出水(F_condense1, F_condense2, F_other, _p, _t)  # kJ/h
    power_steam = get_tag_value(snapshot, TagsRead.发电机有功功率_steam, 102)
    power_shaft_steam = power_steam / 0.988 * 3600000  # 1MW=1MJ/s=1000kJ/s=1000*3600kJ/h
    Q_seal = 18502790  # 轴封漏汽热量；kJ/h
    _p = get_tag_value(snapshot, TagsRead.低压蒸汽压力1, 0.3) + p0
    _t = get_tag_value(snapshot, TagsRead.低压蒸汽温度1, 143)
    F_lms1 = get_tag_value(snapshot, TagsRead.低压蒸汽流量1, 0) if power1 > 20 else 0
    H_lms1 = get_h_by_pt(_p, _t)
    _p = get_tag_value(snapshot, TagsRead.低压蒸汽压力2, 0.4) + p0
    _t = get_tag_value(snapshot, TagsRead.低压蒸汽温度2, 220)
    F_lms2 = get_tag_value(snapshot, TagsRead.低压蒸汽流量2, 12.8) if power2 > 20 else 0
    H_lms2 = get_h_by_pt(_p, _t)
    Q_lms = (H_lms1 * F_lms1 + H_lms2 * F_lms2) * 1000  # 1t/h*1kJ/kg=1000kg/h*kJ/kg=1000kJ/h
    F_ms1 = get_tag_value(snapshot, TagsRead.高压蒸汽流量1号炉, 0) if power1 > 20 else 0
    F_ms2 = get_tag_value(snapshot, TagsRead.高压蒸汽流量2号炉, 245) if power2 > 20 else 0
    F_msds1 = get_tag_value(snapshot, TagsRead.高压蒸汽减温水流量1号炉, 0)
    F_msds2 = get_tag_value(snapshot, TagsRead.高压蒸汽减温水流量2号炉, 7.65)
    F_ms = F_ms1 + F_ms2 + F_msds1 + F_msds2
    _p = get_tag_value(snapshot, TagsRead.主汽门前压力, 6.876) + p0
    _t = get_tag_value(snapshot, TagsRead.主汽门前温度, 537.9)
    H_ms = get_h_by_pt(_p, _t)
    Q_ms = F_ms * H_ms * 1000  # kJ/h
    _p = get_tag_value(snapshot, TagsRead.高排压力, 2.05) + p0
    _t = get_tag_value(snapshot, TagsRead.高排温度, 391.72)
    H_ho = get_h_by_pt(_p, _t)
    F_合缸漏汽 = 17.962
    F_ho = F_ms - F_合缸漏汽
    Q_ho = F_ho * H_ho * 1000
    F_fw_medium1 = get_tag_value(snapshot, TagsRead.中压给水流量1号炉, 0)
    F_fw_medium2 = get_tag_value(snapshot, TagsRead.中压给水流量2号炉, 87.084)
    F_rhds1 = get_tag_value(snapshot, TagsRead.再热减温水流量1, 0) if power1 > 20 else 0
    F_rhds2 = get_tag_value(snapshot, TagsRead.再热减温水流量2, 2) if power2 > 20 else 0
    F_FGH1 = get_tag_value(snapshot, TagsRead.FGH流量1号炉, 0) if power1 > 20 else 0
    F_FGH2 = get_tag_value(snapshot, TagsRead.FGH流量2号炉, 29.6) if power2 > 20 else 0
    F_mi = F_fw_medium1 + F_fw_medium2 + F_ho - F_FGH1 - F_FGH2 + F_rhds1 + F_rhds2
    P_mi = get_tag_value(snapshot, TagsRead.中压主汽门前压力) + p0
    T_mi = get_tag_value(snapshot, TagsRead.中压主汽门前温度)
    H_mi = get_h_by_pt(P_mi, T_mi)
    Q_mi = F_mi * H_mi * 1000
    Q_c = (Q_ms - Q_ho + Q_mi + Q_lms - Q_seal - power_shaft_steam - Q_wellout - Q_供热) / 3600000  # MW
    Q_c = 100 if Q_c < 100 else Q_c
    Q_c = 550 if Q_c > 550 else Q_c
    pres_act = get_tag_value(snapshot, TagsRead.当前背压, 6)
    flow_ng = get_tag_value(snapshot, TagsRead.计量单元天然气流量1)
    flow_ng = flow_ng + get_tag_value(snapshot, TagsRead.计量单元天然气流量2)
    flow_ng = flow_ng + get_tag_value(snapshot, TagsRead.计量单元天然气流量3)
    flow_ng = flow_ng  # 天然气流量 Nm3/h

    c0 = interpolate_value_complex(Q_c, Qc_C)

    xi = (Q_c, t0, humid)
    p_back = {}
    # coal_consume = {}
    for 循泵方式 in ["A", "B", "C", "D", "E", "F", "G", "H"]:
        for 风机数量 in [3, 4, 5, 6, 7, 8]:
            condition = f"{循泵方式}{风机数量}"
            _ = pressure_funcs[condition](xi)
            # _coal = coal_funcs[condition](xi)
            p_back.update({condition: _})
            # coal_consume.update({condition: _coal})

    fan_num_cur = int(get_tag_value(snapshot, TagsRead.当前风机运行方式, 4))
    pump_num_cur = get_tag_value(snapshot, TagsRead.当前循泵运行方式, 0)
    if pump_num_cur == 0.0:  # 说明当前循泵未运行，则全厂处于停机状态，不进行寻优
        return 0
    pump_num_cur = get_pump_type_by_int(pump_num_cur)
    global debug
    if debug:
        fan_num_cur = fan_num_cur + 1
    cur_state = f"{pump_num_cur}{fan_num_cur}"  # 当前运行的组合方式

    delta = {}
    delta_power_max = 0
    state_max = cur_state  # 记录净功率增加最大的工况
    state_max2 = cur_state  # 记录净功率增加第二大的工况
    types = availableType.get(cur_state)
    for condition in types:
        # if Q_c < 200 and pres_act < 5:
        # if condition == "G6":
        #     delta.update({condition: {"微增功率": 0,
        #                               "冷端耗功增加": 0,
        #                               "净出力增加": -100,
        #                               "背压增加值": 0,
        #                               "背压": 0,
        #                               "煤耗降低值": 0,
        #                               "煤耗(不考虑供热)": 0,
        #                               },
        #                   })  # 相当于从结果中剔除G6
        #     continue

        delta_p = p_back[condition] - p_back[cur_state]  # 如果<0
        # delta_coal = coal_consume[condition] - coal_consume[cur_state]
        delta_wt = -power_steam * delta_p * c0 * 10  # kW，如果组合背压大于基准背压，则微增出力<0，该值为出力增加量
        delta_wc = power_cold[condition] - power_cold[cur_state]  # 如果组合背压大于基准背压，则冷端耗功差<0，该值为冷端耗功增加量
        delta_w = delta_wt - delta_wc  # 净功率增加量
        delta_c, c = get_delta_coal(flow_ng, power_total, delta_w)
        delta.update({condition: {"微增功率": delta_wt,
                                  "冷端耗功增加": delta_wc,
                                  "净出力增加": delta_w,
                                  "背压增加值": delta_p,
                                  "背压": p_back[condition],
                                  "煤耗降低值": delta_c,
                                  "煤耗(不考虑供热)": c,
                                  },
                      })
        if delta_w > delta_power_max:
            delta_power_max = delta_w
            state_max2 = state_max
            state_max = condition

    # -------------------------------- 校验当前优化结果是否合理 ---------------------------------
    # A:2大1小(高速)    B:2大             C:1大2小(高速)  D:1大1小(高速)
    # E:2小(高速)       F:2小(1高1低)     G:1大          H:1小(高速)
    if pump_num_cur == state_max[0]:
        delta, _ = deal_different_fan(delta, state_max, cur_state, snapshot)  # 对不同的风机数量结果进行校核
        if _ != state_max:
            delta, state_max = deal_different_fan(delta, state_max2, cur_state, snapshot)
    else:
        if fan_num_cur == state_max[1]:
            delta, state_max = deal_different_pump(delta, state_max, cur_state, snapshot)  # 对不同的泵速进行校核
        else:
            delta, state_max = deal_different_pump_and_fan(delta, state_max, cur_state, snapshot)
    # -------------------------------- 校验当前优化结果是否合理 ---------------------------------

    # -------------------------------- 优化结果更新阈值 ------------------------------------
    global t_range, power_range, heat_range, time_range, last_state, pres_range
    is_steady = True
    if len(t_range) == 0 and len(power_range) == 0:  # 初次计算
        need_update = True
    else:
        if now > time_range:  # 如果距离上一次优化结果更新时间超过10分钟，则强制重新计算优化结果
            # 更新结果
            need_update = True
            logger.debug(f"更新时间达到限制，强制更新：{now}：{time_range}")
        else:
            if all_in_range({power_steam: power_range}, {t0: t_range},
                            {Q_供热: heat_range}):  # 如果参数波动幅度都在允许范围之内，则保持上一个优化结果不变, {pres_act: pres_range}
                need_update = False
                is_steady = True
            else:
                is_steady = False
                need_update = True
                range_temp = [{power_steam: power_range}, {t0: t_range}, {Q_供热: heat_range}, {pres_act: pres_range}]
                logger.debug(f"参数波动超范围更新：功率/环境温度/供热量/背压 --> {range_temp}")
        if pres_act < 2.8 or pres_act > 9:  # 当超限值时，当前的优化结果必然是将背压向合理方向调整
            need_update = True
            logger.debug(f"背压超限值更新，{pres_act=}")

    if need_update:
        t_range = [t0 - 2, t0 + 2]
        power_range = [power_steam - 5, power_steam + 5]
        heat_range = [Q_供热 - 20 * 1000000, Q_供热 + 20 * 1000000]  # ±20GJ/h
        pres_range = [pres_act - 0.5, pres_act + 0.5]
        time_range = now + datetime.timedelta(
            minutes=60)  # 如果距离上一次优化结果更新时间超过60分钟，则强制重新计算优化结果，正常情况下，如果负荷波动小，则不重新计算，因此该时间值应较长
        last_state.update(delta)
        last_state.update({"state_max": state_max})
        logger.info("更新优化结果............")
    else:
        state_max = last_state["state_max"]  # 只是运行方式不更新，但是运行方式对应的背压和煤耗需要实时更新，更新数据在delta中
    # -------------------------------- 优化结果更新阈值 ------------------------------------

    #
    api = init_dbp_api()
    global last_state_act, 上次冷端运行方式调整时间, time_steady, 上次冷端运行方式调整时的背压差
    运行方式调整秒数 = (now - 上次冷端运行方式调整时间).seconds if 上次冷端运行方式调整时间 is not None else 2000
    if last_state_act != cur_state or 运行方式调整秒数 < time_steady:  # 说明运行人员调整了冷端运行方式，则时间更新重新计时，以等待运行工况稳定
        if need_update:
            # 如果优化结果更新，则无视现实中的冷端运行方式改变产生的动态过程，让更新后的运行结果直接跟踪当前状态
            pass
        else:
            time_range = now + datetime.timedelta(minutes=60)
            if last_state_act == "A0":
                pass  # 说明是软件刚启动，第一次进入该条件
            else:
                # 运行方式调整后，最佳真空值需要逐渐变化，不能瞬间将delta["背压变化值"]添加到实际背压上
                if last_state_act != cur_state:
                    上次冷端运行方式调整时间 = now
                    logger.debug(f"检测到冷端运行方式改变，{last_state_act} -> {cur_state}")
                    上次冷端运行方式调整时的背压差 = last_state[state_max]["背压增加值"]
                    if 运行方式调整秒数 < time_steady:
                        pass  # 说明上次调整后还没稳定，再次调整
                if is_steady:  # 稳定状态下,则保持推荐背压只跟随上一次推荐背压
                    xi_last = (last_state["凝汽器热负荷"], last_state["t0"], last_state["humid"])
                    p_last = pressure_funcs[state_max](xi_last)
                    p_now = pressure_funcs[state_max](xi)
                    负荷变化导致的背压变化 = p_now - p_last
                    if last_state.get(state_max) is None:  # state_max变化时，上一个last_state字典里可能没有当前state_max的值
                        last_state[state_max]["背压"] = last_state[last_state["state_max"]]["背压"]
                    delta[state_max]["背压"] = last_state[state_max]["背压"] + 负荷变化导致的背压变化
                    delta[state_max]["背压增加值"] = delta[state_max]["背压"] - pres_act
                else:
                    dispatch_delta_p(delta, state_max, snapshot, xi)
                delta[state_max]["背压"] = pres_act + delta[state_max]["背压增加值"]

    last_state_act = cur_state
    _debug1 = pressure_funcs[state_max](xi)  # 使用何欣欣数据库获得的背压
    _debug2 = get_backpressure_by_history(Qc=Q_c, t0=t0, humid=humid, state=state_max)
    pres_final = _debug1 if _debug2 is None else _debug2
    pres_his = init_dbp_api().get_his_value(tags="NPPC_P_Best_Con", tags_description="最优运行方式下背压",
                                            start_time=now - datetime.timedelta(days=0, hours=0, minutes=3),
                                            end_time=now)
    pres_his = pres_his.mean(numeric_only=True).values[0]  # 推荐历史背压历史3分钟的平均值
    pres_final = (pres_final + pres_his * 5) / 6
    delta[state_max]["背压"] = pres_final
    delta[state_max]["煤耗降低值"], _ = cal_coal_save(snapshot, _debug1, pres_act, cur_state, state_max, Q_c)
    result = {
        "建议循泵运行方式": float(get_pump_type_by_char(state_max[0])),
        "建议风机运行方式": float(state_max[1]),
        "最优运行方式下背压": delta[state_max]["背压"],
        "优化后机组节煤量": abs(delta[state_max]["煤耗降低值"])
    }
    last_state.update(delta)  # 记录上一个运行状态信息
    last_state.update({"凝汽器热负荷": Q_c, "t0": t0, "humid": humid*100})
    logger.debug(result)
    logger.debug({"理论计算推荐背压": _debug1, "历史运行工况背压": _debug2, "当前背压": pres_act, "当前运行方式": cur_state})
    api.write_snapshot_by_cmd(tags=[TagsWrite.get(k) for k in list(result.keys())], values=list(result.values()))


execute_function_by_interval(optimize, minute=0, second=30, daemon=True)
