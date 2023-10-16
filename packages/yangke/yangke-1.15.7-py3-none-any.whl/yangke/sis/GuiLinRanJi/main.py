import traceback

import numpy as np

from yangke.sis.dll_file import init_dbp_api
from yangke.sis.sis_io import get_tag_value
from yangke.web.flaskserver import start_server_app, logger
from yangke.performance.tools.natural_gas import NaturalGas


def deal(args):
    action = args.get("Action").lower()
    result = eval("{}(args)".format(action))
    return result


def naturalgas(args):
    try:
        # 获取前端传入的数据
        compositions = NaturalGas.get_components_name()
        comp = {name: float(args.get(name) or 0) for name in compositions}
        ng = NaturalGas(comp)
        p = float(args.get("P") or 0.101325)
        t = float(args.get("T") or 20)
        t0 = float(args.get("T0") or 20)
        res = {
            "M": ng.mole_weight,
            "Hmg": ng.get_gcv_mass(t0) / 1000,
            "Hvg": ng.get_gcv_voln(20, 20) / 1000,
            "Hcg": ng.get_gcv_mole() / 1000,
            "Hmn": ng.get_ncv_mass(t0) / 1000,
            "Hvn": ng.get_ncv_voln(20, 20) / 1000,
            "Hcn": ng.get_ncv_mole() / 1000,
            "Z": ng.get_z_gas(p, t),
            "D": ng.density
        }
        return res
    except:
        traceback.print_exc()
        logger.debug("error")
        return {"Success": True,
                "Info": "服务正常，请使用Action传入指定的操作！",
                "Example": example}


class PolyCurve:
    def __init__(self, x_list, y_list, deg=1):
        """
        多项式拟合曲线，根据x_list和y_list拟合多项式曲线

        :param x_list: 已知的x点列表
        :param y_list: 一致的y点列表
        :param deg: 多项式阶次
        """
        self.x = np.array(x_list)
        self.y = np.array(y_list)
        self.z = np.polyfit(self.x, self.y, deg)
        self.func = np.poly1d(self.z)

    def get_value(self, x):
        """
        获取曲线上x点上对应的y值

        :param x:
        :return:
        """
        return self.func(x)

    def plot(self, xlim=None, ylim=None):
        import matplotlib.pyplot as plt
        xp = np.linspace(min(self.x), max(self.x))
        _ = plt.plot(self.x, self.y, '.', xp, self.func(xp), '-')
        if xlim is not None:
            plt.xlim()
        if ylim is not None:
            plt.ylim()
        plt.show()


def fit_curve(type="", power=None, flow_gas=None, a=-0.0693, b=1.3388, c=0.4832, d=3.7897):
    if type == "燃气流量vs纯凝功率":
        f_gas = [9.31, 7.5, 5.92, 4.54]
        power = [68.443, 53.504, 39.202, 27.098]
        _ = PolyCurve(x_list=power, y_list=f_gas, deg=3)
        _.plot()
        return _.func
    elif type == "纯凝功率vs燃气流量":
        f_gas = [9.31, 7.5, 5.92, 4.54]
        power = [68.443, 53.504, 39.202, 27.098]
        _ = PolyCurve(x_list=f_gas, y_list=power, deg=3)
        _.plot()


def read_data(tag_des_read=None):
    if tag_des_read is None:
        tag_des_read = {
            "N1DCS.TCS110RCAOG_B120_01": "#1功率",
            "N1DCS.TCS110RCAOG_B120_02": "#2功率",
            "N1DCS.TCS110RCAOG_B120_03": "#3功率",
            "N1DCS.TCS110RCAOG_B120_04": "#1天然气流量",
            "N1DCS.TCS110RCAOG_B120_05": "#2天然气流量",
            "N1DCS.TCS110RCAOG_B120_06": "#3天然气流量",
        }
    dbp_api = init_dbp_api(ip="", port="", user="", password="")
    if dbp_api is not None:
        snapshot = dbp_api.get_snapshot(tags=list(tag_des_read.keys()),
                                        tag_description=list(tag_des_read.values()),
                                        need_detail=False)
    else:
        logger.warning("RDBP服务器连接失败")
        snapshot = {}
    power1 = float(get_tag_value(snapshot, "#2FGH进气温度") or 18)
    power2 = float(get_tag_value(snapshot, "#2FGH进气温度") or 18)
    power3 = float(get_tag_value(snapshot, "#2FGH进气温度") or 18)
    f_gas1 = float(get_tag_value(snapshot, "#2FGH进气温度") or 18)
    f_gas2 = float(get_tag_value(snapshot, "#2FGH进气温度") or 18)
    f_gas3 = float(get_tag_value(snapshot, "#2FGH进气温度") or 18)
    return power1, power2, power3, f_gas1, f_gas2, f_gas3


def heat_supply(args):
    try:
        price_gas = float(args.get("p_g") or 0.101325)
        price_heat = float(args.get("p_h") or 0.101325)
        price_power = float(args.get("p_p") or 0.101325)
        固定成本 = float(args.get("p1") or 0)
        折旧成本 = float(args.get("p2") or 0)
        power1, power2, power3, f_gas1, f_gas2, f_gas3 = read_data()
        get_f_by_power = fit_curve("燃气流量vs纯凝功率")
        get_power_by_f = fit_curve("纯凝功率vs燃气流量")
        f_gas_供电 = get_f_by_power(power1)
        f_gas_供热 = f_gas1 - f_gas_供电

    except:
        return {}


def start_server():
    # run()  # 启动定时执行
    heat_supply({})
    start_server_app(deal=deal, port=5000,
                     example_url=example)


if __name__ == "__main__":
    example = "http://127.0.0.1:5000/?Action=NaturalGas&CH4=0.98&N2=0.02&T=15&P=3.8&T0=20"
    start_server()
