from yangke.performance.tools.natural_gas import NaturalGas


def c_combustion_gas(flow_gas=10000, natural_gas=None):
    """
    根据天然气流量计算实时碳排放，参考《GB/T 32151》，如果不传入天然气对象，则使用《GB/T 32151》中的定值粗略计算，如果传入天然气对象，则如下：
    natural_gas = NaturalGas(compositions={"CH4": 99, "N2": 1})
    碳排放量 = c_combustion_gas(flow_gas=10, natural_gas=natural_gas)


    :param natural_gas: 天然气对象
    :param flow_gas: Nm3/h
    :return: 碳排放量，t/h
    """

    flow_gas = flow_gas / 10000  # 万Nm3
    碳氧化率_天然气 = 0.99
    if natural_gas is None:
        ncv = 38931
        单位热值含碳量 = 15.3e-3
    elif isinstance(natural_gas, NaturalGas):
        natural_gas.set_pt(0.101325, 15)
        # ncv_m = natural_gas.get_ncv_mass(15)  # kJ/kg
        # ncv = ncv_m * natural_gas.get_density()  # kJ/kg/(Nm3/kg) = kJ/Nm3
        # c_ratio = natural_gas.get_ratio_carbon()  # 单位质量天然气中碳元素的质量, kg/kg
        # 单位热值含碳量 = c_ratio / ncv_m  # kg/kJ = t/MJ
        # 单位热值含碳量 = 单位热值含碳量 * 1000  # t/GJ
        c_ratio = natural_gas.get_ratio_carbon()
        density = natural_gas.get_density()
        return flow_gas * 10000 * density * c_ratio / 12 * 44 / 1000  # Nm3/h*(kg/Nm3)

    ncv = ncv / 100  # GJ/万Nm3

    天然气活动数据 = ncv * flow_gas  # t GJ
    排放因子 = 单位热值含碳量 * 碳氧化率_天然气 * 44 / 12
    E_燃烧 = 天然气活动数据 * 排放因子

    return E_燃烧, 排放因子


print(c_combustion_gas(10000))
natural_gas = NaturalGas({"CH4": 100, "N2": 0})
natural_gas.set_pt(0.101325, 15)
print(c_combustion_gas(10000, natural_gas))
