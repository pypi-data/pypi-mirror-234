import os.path

import pandas as pd

from yangke.common.fileOperate import read_csv_ex
from yangke.base import yield_all_file, merge_dataframes_simple
from yangke.common.config import logger
from yangke.performance.iapws97 import get_h_by_pt
from yangke.sis.export_history_values import find_condition, 删除非稳态数据

rho_gas = 0.68  # 天然气密度
ncv_m = 44112  # 天然气热值 kJ/Nm3
ncv_v = ncv_m * rho_gas  # 天然气热值 kJ/Nm3
power_pump_定频泵 = 280  # kW
power_pump_工频 = 280  # kW
功率因数_pump_变频 = 0.83 * 1.732
功率因数_fan = 0.865 * 1.732


def download_data(data_folder=r"C:\Users\YangKe\Desktop\桂林历史数据"):
    """
    下载历史数据

    :param data_folder:
    :return:
    """
    ...


def read_data(data_folder=r"C:\Users\YangKe\Desktop\桂林历史数据"):
    """读取历史数据文件"""

    his = []
    for file in yield_all_file(folder=data_folder, filter_=[".csv"]):
        data = read_csv_ex(file=file, index_col=0)
        logger.debug(f"加载历史数据:{file}")
        data["天然气流量"] = (data["天然气流量1"] + data["天然气流量2"]) / 2  # Nm3/h
        data.drop(data[data["天然气流量"] < 10].index, inplace=True)
        data["全厂发电总功率"] = data["电功率1"] + data["电功率2"] + data["电功率3"]
        data.drop(data[data["全厂发电总功率"] < 15].index, inplace=True)
        if data.shape[0] == 0:
            continue
        data["供热流量"] = data["北线供热流量"] + data["三金供热流量"]
        data["三金供热温度"] = data.apply(lambda x: x["北线供热温度"] if x["三金供热温度"] < 20 else x["三金供热温度"], axis=1)
        data["北线供热温度"] = data.apply(lambda x: x["三金供热温度"] if x["北线供热温度"] < 20 else x["北线供热温度"], axis=1)
        data["三金供热压力"] = data.apply(lambda x: x["北线供热压力"] if x["三金供热压力"] < 0.4 else x["三金供热压力"], axis=1)
        data["北线供热压力"] = data.apply(lambda x: x["三金供热压力"] if x["北线供热压力"] < 0.4 else x["北线供热压力"], axis=1)
        data["焓_北线"] = data.apply(lambda x: get_h_by_pt(x["北线供热压力"] + x["大气压力"] / 1000, x["北线供热温度"]), axis=1)
        data["焓_三金"] = data.apply(lambda x: get_h_by_pt(x["三金供热压力"] + x["大气压力"] / 1000, x["三金供热温度"]), axis=1)
        data["供热能量"] = data["北线供热流量"] * data["焓_北线"] * 1000 + data["三金供热流量"] * data["焓_三金"] * 1000  # kJ/kg*kg/h
        data["alpha"] = data.apply(lambda x: x["供热能量"] / (x["天然气流量"] * ncv_v), axis=1)

        data["背压1"] = data.apply(lambda x: 0 if x["电功率1"] < 20 else x["背压1"], axis=1)
        data["背压2"] = data.apply(lambda x: 0 if x["电功率2"] < 20 else x["背压2"], axis=1)
        data["冷却塔1频率"] = data["冷却塔1频率"].apply(lambda x: 0 if x < 10 else x)
        data["冷却塔2频率"] = data["冷却塔2频率"].apply(lambda x: 0 if x < 10 else x)
        data["冷却塔3频率"] = data["冷却塔3频率"].apply(lambda x: 0 if x < 10 else x)

        # data["供热气耗"] = data["供热能量"] / ncv / rho_gas  # kJ/h/(kJ/kg)=kg/h, kg/h*kg/m3 = Nm3/h
        data["循泵1转速"] = data["循泵1转速"].apply(lambda x: 0 if x < 20 else x)  # 转速小于20则置为0
        data["循泵3转速"] = data["循泵3转速"].apply(lambda x: 0 if x < 20 else x)  # 转速小于20则置为0

        data["循泵1功率"] = data.apply(
            lambda x: power_pump_工频 if x["循泵1变频模式"] == 0 else x["循泵1电流"] * 10 * 功率因数_pump_变频,
            axis=1)
        data["循泵1功率"] = data.apply(lambda x: x["循泵1功率"] if x["循泵1转速"] > 50 else 0, axis=1)
        data["循泵2功率"] = data.apply(lambda x: power_pump_定频泵 if x["循泵2开关"] < 1000 else 0, axis=1)  # kW
        data["循泵3功率"] = data.apply(
            lambda x: power_pump_工频 if x["循泵3变频模式"] == 0 else x["循泵3电流"] * 10 * 功率因数_pump_变频,
            axis=1)
        data["循泵3功率"] = data.apply(lambda x: x["循泵3功率"] if x["循泵3转速"] > 50 else 0, axis=1)
        data["循泵4功率"] = data.apply(lambda x: power_pump_定频泵 if x["循泵4开关"] < 1000 else 0, axis=1)  # 开关值小于1000则泵为开启状态
        data["循泵2开关"] = data["循泵2开关"].apply(lambda x: 1 if x < 1000 else x)  # <1000为开
        data["循泵2开关"] = data["循泵2开关"].apply(lambda x: 0 if x > 1000 else x)  # >1000为关
        data["循泵4开关"] = data["循泵4开关"].apply(lambda x: 1 if x < 1000 else x)
        data["循泵4开关"] = data["循泵4开关"].apply(lambda x: 0 if x > 1000 else x)

        data["循泵功率"] = data["循泵1功率"] + data["循泵2功率"] + data["循泵3功率"] + data["循泵4功率"]
        data["风机功率1"] = data.apply(lambda x: x["冷却塔1电流"] * 0.38 * 功率因数_fan if x["冷却塔1电流"] > 10 else 0, axis=1)
        data["风机功率2"] = data.apply(lambda x: x["冷却塔2电流"] * 0.38 * 功率因数_fan if x["冷却塔2电流"] > 10 else 0, axis=1)
        data["风机功率3"] = data.apply(lambda x: x["冷却塔3电流"] * 0.38 * 功率因数_fan if x["冷却塔3电流"] > 10 else 0, axis=1)
        data["风机开关1"] = data.apply(lambda x: 1 if x["冷却塔1电流"] > 10 else 0, axis=1)
        data["风机开关2"] = data.apply(lambda x: 1 if x["冷却塔2电流"] > 10 else 0, axis=1)
        data["风机开关3"] = data.apply(lambda x: 1 if x["冷却塔3电流"] > 10 else 0, axis=1)
        data["风机总功率"] = data["风机功率1"] + data["风机功率2"] + data["风机功率3"]
        data["冷端总功率"] = data["循泵功率"] + data["风机总功率"]

        data = 删除非稳态数据(data, "电功率1", slope=2, till=20)
        data = 删除非稳态数据(data, "电功率2", slope=2, till=20)
        data = 删除非稳态数据(data, "电功率3", slope=2, till=20)
        data = 删除非稳态数据(data, "供热流量", slope=4, till=10)
        data = 删除非稳态数据(data, "循泵1转速", slope=50, till=20)
        data = 删除非稳态数据(data, "循泵2开关", till=20)
        data = 删除非稳态数据(data, "循泵3转速", slope=50, till=20)
        data = 删除非稳态数据(data, "循泵4开关", till=20)
        data = 删除非稳态数据(data, "风机开关1", till=20)
        data = 删除非稳态数据(data, "风机开关2", till=20)
        data = 删除非稳态数据(data, "风机开关3", till=20)
        data = 删除非稳态数据(data, "天然气流量", slope=500, till=20, inplace=True)

        data["净气耗"] = data["天然气流量"] / (data["全厂发电总功率"] * 1000 - data["冷端总功率"]) * (1 - data["alpha"])  # Nm3/(kW.h)
        titles = ["大气压力", "环境温度", "环境湿度", "电功率1", "电功率2", "电功率3", "供热流量", "循泵1变频模式", "循泵1转速",
                  "循泵2开关", "循泵3变频模式", "循泵3转速", "循泵4开关", "冷却塔1频率", "冷却塔2频率", "冷却塔3频率", "净气耗",
                  "冷端总功率", "背压1", "背压2", "天然气流量"]

        data.drop(data[data["净气耗"] < 0.14].index, inplace=True)
        data.drop(data[data["净气耗"] > 0.28].index, inplace=True)
        # data.drop(data[data["电功率3"] < 1 && data["供热流量3"] > 1].index, inplace=True)
        data = data[titles].copy()
        his.append(data)
    return his


def generate_pickle(file="default.pkl", force=False):
    """
    根据下载的历史数据生成冷端优化查询所需的pickle二进制文件

    :return:
    """
    data_folder = r'C:\Users\Administrator\Desktop\glxnfx\历史数据'
    if not os.path.isabs(file):
        file = os.path.join(data_folder, file)
    logger.debug(f"{os.path.abspath(file)}")
    if not os.path.exists(file) or force:  # 如果pickle文件不存在或需要强制生成
        dataframes = read_data(data_folder)
        data = merge_dataframes_simple(dataframes)
        data.to_pickle(file)
        logger.debug(f"pickle文件保存至{os.path.abspath(file)}")
    else:
        return


if __name__ == "__main__":
    pickle_file = os.path.join(r'C:\Users\Administrator\Desktop\glxnfx\历史数据', 'default.pkl')
    generate_pickle(file=pickle_file, force=True)
    data = pd.read_pickle(pickle_file)
    res = find_condition(df=data, unit_condition=[('电功率1', 0, "±2"), ("电功率2", 0, "±2"), ("电功率3", 30, "±2"),
                                                  ('供热流量', 60, "±2"), ('环境温度', 20, "±4"), ('大气压力', 100, '±10')],
                         auto_loose=True)
    if res is not None:
        res.sort_values(by="净气耗", ascending=True)
    logger.debug(res)
