import copy
import datetime
import os
import random

from yangke.performance.iapws97 import get_h_by_pt
from yangke.common.config import logger
from yangke.common.fileOperate import write_excel, pd_set_na, read_excel
from yangke.sis.BeiJingShenHua.tags import TagsRead, TagsWrite
from yangke.sis.dll_file import read_data, get_tag_value, init_write_sis, init_dbp_api
import pandas as pd
from yangke.sis.BeiJingShenHua.tags import get_pump_type_by_int
from yangke.base import is_number

ip = "10.2.128.168"
port = "12084"
user = "admin"
passwd = "admin"

fit_index = {
    "A3": [],
    "A4": [],
    "A5": [],
    "A6": [],
    "A7": [],
    "A8": [],
    "B3": [],
    "B4": [],
    "B5": [],
    "B6": [],
    "B7": [],
    "B8": [],
    "C3": [],
    "C4": [],
    "C5": [],
    "C6": [],
    "C7": [],
    "C8": [],
    "D3": [-0.006961224, 0.010512006, 2.200054686],
    "D4": [],
    "D5": [],
    "D6": [],
    "D7": [],
    "D8": [],
    "E3": [],
    "E4": [],
    "E5": [],
    "E6": [],
    "E7": [],
    "E8": [],
    "F3": [],
    "F4": [],
    "F5": [],
    "F6": [],
    "F7": [],
    "F8": [],
    "G3": [],
    "G4": [],
    "G5": [],
    "G6": [],
    "G7": [],
    "G8": [],
    "H3": [],
    "H4": [],
    "H5": [],
    "H6": [],
    "H7": [],
    "H8": [],
    "I3": [],
    "I4": [],
    "I5": [],
    "I6": [],
    "I7": [],
    "I8": [],
}


def filter_(df, tag, value_range):
    """
    从df中删除参数不在范围内的数据，示例
    filter_(his_value, "#1电功率", [200,300])  # 只保留电功率在200~300之间的行
    filter_(his_value, "#1电功率", [200,None]) # 只保留电功率在200以上的行
    filter_(his_value, "#1电功率", [None,100])  # 只保留电功率在100以下的行
    """
    min_value = value_range[0]
    max_value = value_range[1]
    if min_value is not None:
        df = df[df[tag] >= min_value]
    if max_value is not None:
        df = df[df[tag] <= max_value]
    return df


def get_history(tags, des, months=12, days=0, start_time: datetime.datetime = None, end_time: datetime.datetime = None,
                time_interval=60, save_to: str | None = None):
    """
    从RDBProxy代理服务器上导出历史数据，如果导出数据的时标是1970年，请检查tags标签是否正确。
    本方法要加载settings.yaml文件中的RDBP服务器信息。
    默认下载最近一年的历史数据。

    :param tags: list类型，导出测点的标签，需要与DCS系统上测点的KKS码或标签名一致
    :param des: list类型，导出测点的描述，可以自定义，用于注释导出的测点，如果传入该参数，则长度必须与tags相同
    :param months: 如果需要下载最近n月的历史数据，通过该参数传入下载历史数据的月数，如果按起止时间下载历史数据，无需设置该参数
    :param days: 如果需要下载最近n天的历史数据，通过该参数传入下载历史数据的天数，如果按起止时间下载历史数据，无需设置该参数
    :param start_time: 下载历史数据的起始时间，如果下载最近n月/天的历史数据，该参数留空
    :param end_time: 下载历史数据的截止时间，如果下载最近n月/天的历史数据，该参数留空
    :param time_interval: 下载数据的时间间隔，单位为秒，默认60s
    :param save_to: 是否保存到文件，默认不保存，如果需要保存，传入文件名
    """
    from yangke.base import merge_two_dataframes

    if start_time is not None and end_time is not None:  # 按起止时间下载历史数据
        if start_time >= end_time:
            return
        now = datetime.datetime.now()
        if start_time > now:
            return
        if end_time > now:
            end_time = now

        his_values = []
        delta_time = datetime.timedelta(days=1)
        _end = start_time + delta_time
        while _end < end_time:
            api = init_dbp_api()
            his_value = api.get_his_value(tags=tags, tags_description=des, start_time=start_time, end_time=_end,
                                          time_interval=time_interval)
            his_values.append(his_value)
            _end = _end + delta_time
            api.close()
        api = init_dbp_api()
        his_value = api.get_his_value(tags=tags, tags_description=des, start_time=_end, end_time=end_time,
                                      time_interval=time_interval)
        api.close()
        his_values.append(his_value)
        res = his_values[0]
        for v in his_values[1:]:
            res = merge_two_dataframes(res, v)
    else:
        now = datetime.datetime.now()
        if months != 0:
            _start_time = now - datetime.timedelta(days=months * 30, hours=0)
            _end_time = now
            res = get_history(tags, des, start_time=_start_time, end_time=_end_time, time_interval=time_interval,
                              save_to=None)
        else:
            # 下载最后days天的历史数据
            _start_time = now - datetime.timedelta(days=days, hours=0)
            _end_time = now
            res = get_history(tags, des, start_time=_start_time, end_time=_end_time, time_interval=time_interval,
                              save_to=None)
    if save_to:
        res.to_csv(save_to)
    return res


def deal_data(files=None, work_folder=None):
    if files is None:
        files = ["origin_1.csv", "origin_2.csv", "origin_3.csv", "origin_4.csv",
                 "origin_5.csv", "origin_6.csv", "origin_7.csv", "origin_8.csv",
                 "origin_9.csv", "origin_11.csv",
                 ]

    output_data = {}
    for file in files:
        logger.debug(f"处理{file=}")
        if work_folder is not None:
            file = os.path.join(work_folder, file)
        df = pd.read_csv(file)
        his = df.copy()
        df.set_index("DateTime", inplace=True)
        df.index = pd.DatetimeIndex(df.index)  # 将索引类型转换为DatetimeIndex以便可以使用按时间的插值方法
        # df = df.iloc[0:40]
        df["大气压力"] = df["大气压力"] / 10000  # MPa
        # 将大气压力低于0.03MPa的行的数据全部置为np.nan，因为发现有时候DCS系统数据传输故障，时序数据库中数据全都为0
        pd_set_na(df, {"大气压力": {"<": 0.03}}, expand=True, axis=0)
        df = df.interpolate(method="time")  # 31332
        df["天然气流量"] = df["计量单元天然气流量1"] + df["计量单元天然气流量2"] + df["计量单元天然气流量3"]
        df.drop(columns=["建议循泵运行方式", "建议风机运行方式", "最优运行方式下背压", "优化后机组节煤量",
                         "计量单元天然气流量1", "计量单元天然气流量2", "计量单元天然气流量3",
                         ], axis=1, inplace=True)
        for _fan_num in ["风机1电流", "风机2电流", "风机3电流", "风机4电流", "风机5电流", "风机6电流", "风机7电流",
                         "风机8电流",
                         "大泵1电流", "大泵2电流", "小高速3电流", "小高速4电流", "小低速3电流", "小低速4电流"]:
            df[_fan_num] = df[_fan_num].apply(lambda x: 0 if x <= 10 else x)
            df[_fan_num] = df[_fan_num].apply(lambda x: 1 if x > 10 else x)
        df["机力塔数量"] = df["风机1电流"] + df["风机2电流"] + df["风机3电流"] + df["风机4电流"] + \
                           df["风机5电流"] + df["风机6电流"] + df["风机7电流"] + df["风机8电流"]
        df["机力塔数量"] = df["机力塔数量"].apply(lambda x: int(x))
        df["当前大泵数量"] = df["大泵1电流"] + df["大泵2电流"]
        df["当前高速泵数量"] = df["小高速3电流"] + df["小高速4电流"]
        df["当前低速泵数量"] = df["小低速3电流"] + df["小低速4电流"]
        df.drop(columns=["风机1电流", "风机2电流", "风机3电流", "风机4电流", "风机5电流", "风机6电流", "风机7电流",
                         "风机8电流",
                         "大泵1电流", "大泵2电流", "小高速3电流", "小高速4电流", "小低速3电流", "小低速4电流"], axis=1,
                inplace=True)

        df["循泵方式"] = df["当前大泵数量"] * 100 + df["当前高速泵数量"] * 10 + df["当前低速泵数量"]
        df["循泵方式"] = df["循泵方式"].apply(lambda x: get_pump_type_by_int(int(x)))
        df["冷端耗功"] = df["当前大泵数量"] * 2200 + df["当前高速泵数量"] * 1381 + df["当前低速泵数量"] * 837 + df[
            "机力塔数量"] * 223
        df["净功率"] = df["全厂总功率"] * 1000 - df["冷端耗功"]  # kW
        df["气耗"] = df["天然气流量"] / df["净功率"]  # Nm3/(kWh)
        df.drop(columns=["当前大泵数量", "当前高速泵数量", "当前低速泵数量"], axis=1, inplace=True)

        df["主汽门前压力"] = df["主汽门前压力"] + df["大气压力"]
        df["高排压力"] = df["高排压力"] + df["大气压力"]
        df["中压主汽门前压力"] = df["中压主汽门前压力"] + df["大气压力"]
        df["低压蒸汽压力1"] = df["低压蒸汽压力1"] + df["大气压力"]
        df["低压蒸汽压力2"] = df["低压蒸汽压力2"] + df["大气压力"]
        df["热井出水压力"] = df["热井出水压力"] + df["大气压力"]

        df["主蒸汽焓"] = df.apply(lambda x: get_h_by_pt(x["主汽门前压力"], x["主汽门前温度"]), axis=1)
        df["高排焓"] = df.apply(lambda x: get_h_by_pt(x["高排压力"], x["高排温度"]), axis=1)
        df["主蒸汽流量"] = df["高压蒸汽流量1号炉"] + df["高压蒸汽流量2号炉"] + df["高压蒸汽减温水流量1号炉"] + df[
            "高压蒸汽减温水流量2号炉"]
        df["高压缸进汽能量"] = df["主蒸汽流量"] * df["主蒸汽焓"] * 1000
        合缸处漏气量 = 17.962
        df["高排流量"] = df["主蒸汽流量"] - 合缸处漏气量
        df["高排能量"] = df["高排焓"] * df["高排流量"] * 1000
        df["中压进汽流量"] = df["中压给水流量1号炉"] + df["中压给水流量2号炉"] + df["再热减温水流量1"] + \
                             df["再热减温水流量2"] + df["高排流量"] - df["FGH流量1号炉"] - df["FGH流量2号炉"]
        df["中压进汽焓"] = df.apply(lambda x: get_h_by_pt(x["中压主汽门前压力"], x["中压主汽门前温度"]),
                                    axis=1)
        df["中压进汽能量"] = df["中压进汽焓"] * df["中压进汽流量"] * 1000

        df.drop(columns=["主汽门前压力", "主汽门前温度", "高排压力", "高排温度", "主蒸汽焓", "高排焓", "主蒸汽流量",
                         "高排流量",
                         "中压给水流量1号炉", "中压给水流量2号炉", "再热减温水流量1", "再热减温水流量2", "FGH流量1号炉",
                         "FGH流量2号炉", "高压蒸汽减温水流量1号炉", "高压蒸汽减温水流量2号炉", "高压蒸汽流量1号炉",
                         "高压蒸汽流量2号炉", "中压主汽门前压力", "中压主汽门前温度", "燃机功率1", "燃机功率2"], axis=1,
                inplace=True)

        df["低压补汽能量1"] = df.apply(
            lambda x: get_h_by_pt(x["低压蒸汽压力1"], x["低压蒸汽温度1"]) * x["低压蒸汽流量1"] * 1000,
            axis=1)
        df["低压补汽能量2"] = df.apply(
            lambda x: get_h_by_pt(x["低压蒸汽压力2"], x["低压蒸汽温度2"]) * x["低压蒸汽流量2"] * 1000,
            axis=1)
        df["低压补汽能量"] = df["低压补汽能量1"] + df["低压补汽能量2"]

        df["热井出水流量"] = df["凝结水流量1号炉"] + df["凝结水流量2号炉"]
        df["热井出水焓"] = df.apply(lambda x: get_h_by_pt(x["热井出水压力"], x["热井出水温度"]), axis=1)
        df["热井出水能量"] = df["热井出水流量"] * df["热井出水焓"] * 1000

        df.drop(columns=["低压蒸汽压力1", "低压蒸汽温度1", "低压蒸汽流量1", "低压蒸汽压力2", "低压蒸汽温度2",
                         "低压蒸汽流量2",
                         "低压补汽能量1", "低压补汽能量2", "凝结水流量1号炉", "凝结水流量2号炉", "热井出水压力",
                         "热井出水温度", "热井出水流量", "热井出水焓", "中压进汽流量", "中压进汽焓"], axis=1,
                inplace=True)

        df["p"] = df["烟气热网加热器进水压力"] + df["大气压力"]
        df["热网加热器流量"] = df["烟气热网加热器进水流量"] / 2
        df["烟气换热量"] = df.apply(
            lambda x: (x["热网加热器流量"] * (get_h_by_pt(x["p"], x["烟气热网加热器供水温度1"]) - get_h_by_pt(x["p"], x[
                "烟气热网加热器进水温度1"]))
                       + x["热网加热器流量"] * (
                               get_h_by_pt(x["p"], x["烟气热网加热器供水温度2"]) - get_h_by_pt(x["p"], x[
                           "烟气热网加热器进水温度2"]))) * 1000,
            axis=1
        )

        df["供热能量"] = df["供热热量"] * 1000000 - df["烟气换热量"]
        df["轴功率"] = df["发电机有功功率_steam"] / 0.988 * 3600 * 1000
        df["凝汽器热负荷"] = df["高压缸进汽能量"] + df["中压进汽能量"] + df["低压补汽能量"] - df["高排能量"] - 18502790 \
                             - df["供热能量"] - df["轴功率"] - df["热井出水能量"]
        df["凝汽器热负荷"] = df["凝汽器热负荷"] / 3600 / 1000
        df.drop(columns=["供热热量", "供热能量", "发电机有功功率_steam", "轴功率", "高压缸进汽能量", "中压进汽能量",
                         "低压补汽能量", "高排能量", "供热能量", "热井出水能量", "大气压力", "热网加热器疏水流量1",
                         "热网加热器疏水流量2", "当前循泵运行方式", "当前风机运行方式", "凝汽器循环水进水温度1",
                         "凝汽器循环水进水温度2", "烟气热网加热器进水流量", "烟气热网加热器进水压力",
                         "烟气热网加热器进水温度1",
                         "烟气热网加热器供水温度1", "烟气热网加热器进水温度2", "烟气热网加热器供水温度2",
                         "热网加热器流量", "烟气换热量", "烟气热网加热器进水流量",
                         ], axis=1, inplace=True, errors='ignore')

        df["凝汽器热负荷"] = df["凝汽器热负荷"].rolling(window=10).mean()  # 因为凝汽器热负荷参数锯齿状波动严重，取移动平均值
        df["环境湿度"] = df["环境湿度"].rolling(10).mean()
        df = df[["全厂总功率", "凝汽器热负荷", "环境温度", "环境湿度", "循泵方式", "机力塔数量", "当前背压", "气耗"]]
        df = df.copy()
        df.drop(df.head(9).index, inplace=True)  # 删除前10行

        # 检测如果冷端运行方式改变，则删除后续的20分钟数据
        time_section = 20
        is_steady = ["F-top19"] * (time_section - 1)  # 前19行认为不稳定
        for row_idx in range(time_section, df.shape[0] + 1):
            _p = df.iloc[row_idx - time_section: row_idx][
                "循泵方式"]  # df.iloc[0, 20]["循泵方式"].all() -> df.iloc[19]=True
            _f = df.iloc[row_idx - time_section: row_idx]["机力塔数量"]
            if (_p.values == _p.values[0]).all() and (_f.values == _f.values[0]).all():
                is_steady.append("T")
            else:
                is_steady.append("F-冷端方式调整")

        # 考虑到需要保持时间的连续性，此处先标记该行数据需要删除，而不能直接对数据进行删除，否则会影响后续的稳定性条件判断

        # 检测功率如果波动超过20分钟内功率波动超过10MW，则删除数据
        for row_idx in range(time_section, df.shape[0] + 1):
            _p = df.iloc[row_idx - time_section:row_idx]
            if _p["凝汽器热负荷"].max() - _p["凝汽器热负荷"].min() > 10:
                is_steady[row_idx - 1] = "F-热负荷波动"  # 166
                # logger.debug(f"{row_idx=}, 热负荷max={_p['凝汽器热负荷'].max()},min={_p['凝汽器热负荷'].min()}")
            if _p["环境温度"].max() - _p["环境温度"].min() > 5:
                is_steady[row_idx - 1] = "F-环境温度波动"  # 39101
                # logger.debug(f"{row_idx=},环境温度max={_p['环境温度'].max()},min={_p['环境温度'].min()}")
            if _p["环境湿度"].max() - _p["环境湿度"].min() > 10:
                is_steady[row_idx - 1] = "F-环境湿度波动"  # 97
                # logger.debug(f"{row_idx=},环境湿度max={_p['环境湿度'].max()},min={_p['环境湿度'].min()}")

        df["steady"] = is_steady

        df = df[df["steady"].apply(lambda x: x.startswith("T"))]
        output_data.update({os.path.basename(file).split(".")[0]: df})

    write_excel("历史数据库.xlsx", output_data, index=True)


def load_history_file(file):
    """
    加载历史数据文件

    :param file:
    :return:
    """
    df = pd.DataFrame()
    if os.path.exists(file):
        if file.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = read_excel(file, need_merge=True, index_col=0)
    return df


def find_condition(df, unit_condition, cold_condition: dict = None, auto_loose=False):
    """
    查找符合条件的历史工况，返回满足条件的历史数据及历史数据的统计平均值
    示例：
    df, df_mean = find_condition(file="历史数据库.xlsx",
                   unit_condition=[("凝汽器热负荷", 360, "1%"), ("环境温度", 27, "±2"), ("环境湿度", 50, "±10")],
                   cold_condition={"循泵方式": 'B', "机力塔数量": 8}
                   )

    :param auto_loose: 是否自动放宽条件限制，如果为True，当没有找到符合条件的工况时，会自动放宽允许的偏差为原来的两倍再次尝试，直到找到
    :param df: 历史数据dataframe，csv或者xlsx文件
    :param unit_condition: 机组的运行状态参数
    :param cold_condition: 冷端设备运行状态参数
    :return:
    """
    if df is None:
        return None
    origin_df = df.copy()
    # ------------------------------- 过滤冷端运行条件 -------------------------------------------------------
    cold_condition = {} if cold_condition is None else cold_condition  # 当不传入冷端运行条件时，直接跳过冷端条件限制
    for title, val in cold_condition.items():
        df = df[df[title] == val]
    if df.shape[0] == 0:
        logger.debug(f"历史上不存在{cold_condition}的冷端运行方式")
        return None
    # ------------------------------- 过滤冷端运行条件 -------------------------------------------------------

    for item in unit_condition:
        title, val, tolerance = item
        if is_number(val):
            if is_number(tolerance):
                val_min = val * (1 - tolerance)
                val_max = val * (1 + tolerance)
            elif tolerance.endswith("%"):
                tolerance = float(tolerance.replace("%", "")) / 100
                val_min = val * (1 - tolerance)
                val_max = val * (1 + tolerance)
            elif tolerance.startswith("±"):
                tolerance = float(tolerance.replace("±", ""))
                val_min = val - tolerance
                val_max = val + tolerance
            df = df[df[title] < val_max]
            df = df[df[title] > val_min]
    df = df.copy()
    if df.shape[0] < 5:
        if auto_loose:
            new_condition = []
            for item in unit_condition:
                title, val, tolerance = item
                if is_number(tolerance):
                    tolerance = tolerance * 2
                    if tolerance / val > 100:
                        return None
                elif tolerance.endswith("%"):
                    tolerance = float(tolerance.replace("%", "")) / 100
                    if tolerance > 10000:
                        return None
                    tolerance = f"{tolerance * 200}%"
                elif tolerance.startswith("±"):
                    tolerance = float(tolerance.replace("±", ""))
                    if tolerance / val > 100:
                        return None
                    tolerance = f"±{tolerance * 2}"
                new_condition.append((title, val, tolerance))
            # logger.debug(f"历史数据中满足条件的工况个数为{df.shape[0]}，放宽条件限制为：{new_condition}")
            return find_condition(origin_df, new_condition, cold_condition, auto_loose)
        else:
            return None
    else:
        # logger.debug(f"满足条件工况的平均参数为：{df.mean(numeric_only=True)}")
        return df


def generate_data(df):
    from yangke.base import interpolate_nd, kriging
    data = []
    points = []
    for Qc in range(100, 570, 20):
        for t0 in [-5, 0, 5, 10, 15, 20, 25, 30, 35]:
            for humid in [50]:
                for pump in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]:
                    for fan in [3, 4, 5, 6, 7, 8]:
                        res = find_condition(df,
                                             unit_condition=[("凝汽器热负荷", Qc, "±10"), ("环境温度", t0, "±2.5"),
                                                             ("环境湿度", humid, "±100")],
                                             cold_condition={"循泵方式": pump, "机力塔数量": fan},
                                             auto_loose=False
                                             )
                        if res is not None:
                            mean = res.mean(numeric_only=True)
                            bp = mean["当前背压"]
                            gas = mean["气耗"]
                            data.append([mean["凝汽器热负荷"], mean["环境温度"], mean["环境湿度"], pump, fan, bp, gas])
                            print(f"{Qc=}, {t0=}, {humid=}, {pump=}, {fan=}, {bp=}, {gas=}")
                        else:
                            bp = None
                            gas = None

    res_df = pd.DataFrame(data=data,
                          columns=["凝汽器热负荷", "环境温度", "环境湿度", "循泵方式", "机力塔数量", "当前背压",
                                   "气耗"])

    for Qc in [100, 150, 200, 250, 300, 350, 400, 450, 500, 550]:
        for t0 in [-5, 0, 5, 10, 15, 20, 25, 30, 35]:
            for humid in [50]:
                for pump in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]:
                    for fan in [3, 4, 5, 6, 7, 8]:
                        _df_slice = res_df[res_df["循泵方式"] == pump]
                        _df_slice = _df_slice[_df_slice["机力塔数量"] == fan]
                        if _df_slice.shape[0] < 5:
                            continue
                        _df_slice = _df_slice.copy()
                        points = _df_slice[["凝汽器热负荷", "环境温度", "当前背压"]]
                        input_data = points[["凝汽器热负荷", "环境温度"]].values.tolist()
                        output_data = points["当前背压"].values.tolist()
                        k = kriging(input_data, output_data)
                        val = k.predict([350, 25])
                        interpolate_nd(xi=[350, 25], dataframe=points, df_x_titles=["凝汽器热负荷", "环境温度"],
                                       df_y_title=["当前背压"])

    return res_df


def 删除非稳态数据(df: pd.DataFrame, title=None, slope=None, till=None, inplace=False):
    """
    删除非稳态数据，要求df中具有时间列，且时间必须连续，不能是间断的时间。
    分为两种情况。
    一种是某个参数波动幅度过大，需要剔除，则调用方法为：
    删除非稳态数据(df, "电功率", slope=5, till=20)  # 表示标记出20分钟内电功率波动超过5的数据条目

    另一种是某个参数突变后，删除后续的一段时间的数据，如循泵运行台数从2变为3时，删除后续20分钟数据，调用方法为：
    删除非稳态数据(df, "循泵运行台数", till=20)

    inplace参数表示是否真的删除具体数据，这在以下情况中是非常有用的，例如：
    当需要对同一组数据的"电功率", "循泵运行台数"等多个参数进行非稳态数据删除时，如果连续调用：
    df = 删除非稳态数据(df, "电功率", slope=5, till=20, inplace=True)
    df = 删除非稳态数据(df, "循泵运行台数", till=20, inplace=True)
    则第一次调用后，因为会删除一些数据，导致剩余的数据时间段并不连续，在进行后续判断非稳态删除操作时，导致非稳态判断错误，因此，在最后一句真实的
    删除操作前，所有的删除非稳态数据的方法调用都应该指定inpalce=False，只对需要删除的数据行做标记，而不是真正的删除，这样，后续的函数调用时，
    传入的df时间仍是连续的。
    合理的删除操作应为：
    df = 删除非稳态数据(df, "电功率1", slope=5, till=20, inplace=False) # 只标记，不删除
    df = 删除非稳态数据(df, "电功率2", slope=5, till=20, inplace=False) # 只标记，不删除
    df = 删除非稳态数据(df, "电功率3", slope=5, till=20, inplace=False) # 只标记，不删除
    df = 删除非稳态数据(df, "循泵运行台数", till=20, inplace=True) # 标记后，根据标记结果进行删除

    :param title:
    :param range:
    :param till:
    :return:
    """
    if "steady" in df.columns.tolist():
        has_steady = True
        col_idx = df.columns.tolist().index("steady")
    else:
        has_steady = False
        is_steady = ["F-top"] * (till - 1)  # 前19行认为不稳定，是一个19行的字符串列表
        col_idx = -1

    if slope is None:
        for row_idx in range(till, df.shape[0] + 1):
            运行方式 = df.iloc[row_idx - till: row_idx][title]
            if (运行方式.values == 运行方式.values[0]).all():  # 如果持续时间内，运行方式都不变
                if not has_steady:
                    is_steady.append("T")
                else:
                    pass  # 如果有steady列，则不进行操作
            else:
                if not has_steady:
                    is_steady.append("F-冷端方式调整")
                else:
                    df.iat[row_idx, col_idx] = "F-冷端方式调整"
    else:
        # 检测功率如果波动超过20分钟内功率波动超过10MW，则删除数据
        for row_idx in range(till, df.shape[0] + 1):
            _p = df.iloc[row_idx - till:row_idx]
            if _p[title].max() - _p[title].min() > slope:
                if not has_steady:
                    is_steady.append(f"F-{title}波动")
                else:
                    df.iat[row_idx - 1, col_idx] = f"F-{title}波动"
            else:
                if not has_steady:
                    is_steady.append("T")
                else:
                    pass
    if not has_steady:
        df["steady"] = is_steady
    if inplace:
        df = df[df["steady"].apply(lambda x: x.startswith("T"))]
    return df.copy()


def beijingshenhua():
    """
    生成北京神华国华机组的背压计算数据库
    :return:
    """
    des1 = TagsRead.get_keys()
    tags1 = TagsRead.get_values()

    des2 = TagsWrite.get_keys()
    tags2 = TagsWrite.get_values()

    tags1.extend(tags2)
    des1.extend(des2)
    df = load_history_file("历史数据库.xlsx")
    res = generate_data(df)
    res.to_csv("结果3.csv", index=False)


if __name__ == "__main__":
    tags = TagsRead.get_values()
    des = TagsRead.get_keys()
    yyyy, mm, dd, hour, minute, second = (2022, 1, 1, 0, 0, 0)
    start_time = datetime.datetime(year=yyyy, month=mm, day=dd, hour=hour, minute=minute, second=second)
    yyyy, mm, dd, hour, minute, second = (2022, 1, 1, 23, 59, 59)
    end_time = datetime.datetime(year=yyyy, month=mm, day=dd, hour=hour, minute=minute, second=second)
    df = get_history(tags, des, start_time=start_time, end_time=end_time)
