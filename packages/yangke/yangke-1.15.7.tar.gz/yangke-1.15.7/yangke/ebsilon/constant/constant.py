import math
from abc import abstractmethod

from yangke.common.config import logger

背景图层id = -10
管线图层id = -5
组件图层id = 0  # 图层id越小的图元，越先绘制


class DefaultUnit:  # 默认单位类
    def __init__(self):
        self.P = "MPa"
        self.T = "℃"
        self.MassFlow = "t/h"
        self.Power = "kW"
        self.Density = "kg/m^3"
        self.Enthalpy = "kJ/kg"
        self.VolumeFlow = "m^3/h"
        self.SpecificVolume = "m^3/kg"
        self.Length = "m"
        self.Area = "m^2"
        self.AngleUnit = "°"
        self.Velocity = "m/s"

    def set(self, units: dict):
        """
        根据字典信息设置默认的单位

        :param units:
        :return:
        """
        for symbol, unit_str in units.items():
            if symbol == "P":
                self.P = Pressure(unit_str)
            elif symbol == "T":
                self.T = Temperature(unit_str)
            elif symbol == "MassFlow":
                self.MassFlow = MassFlow(unit_str)
            elif symbol == "Power":
                self.Power = Power(unit_str)
            elif symbol == "Density":
                self.Density = Density(unit_str)
            elif symbol == "Enthalpy":
                self.Enthalpy = Enthalpy(unit_str)
            elif symbol == "VolumeFlow":
                self.VolumeFlow = VolumeFlow(unit_str)
            elif symbol == "SpecificVolume":
                self.SpecificVolume = SpecificVolume(unit_str)
            elif symbol == "Length":
                self.Length = Length(unit_str)
            elif symbol == "Area":
                self.Area = Area(unit_str)


class Unit:  # 单位的父类
    def __init__(self):
        self.allowed_values = []
        self.sf = []  # 不同单位对应的缩放因子，如果可以通过缩放转换单位，则定义该参数即可
        self.unit = None

    def get_values_list(self):
        return self.allowed_values

    def get_selected_value(self):
        return self.unit

    def __str__(self):
        return self.unit

    def get_scale_factor(self, unit_str):
        """
        当前单位转换为指定单位时需要乘以的系数,即，如果当前单位为Pressure("MPa")，unit_str="kPa"，则scale_factor=1000

        :param unit_str:
        :return:
        """
        zip_factors = dict(zip(self.allowed_values, self.sf))
        sf = zip_factors.get(self.unit) / zip_factors.get(unit_str)
        return sf

    def transfer_to_unit(self, value: float, unit: str):
        """
        如果单位可以通过简单的乘以系数完成转换，则定义self.sf后调用该方法即可，否则，应自己实现单位的转换方法。
        简单的乘以系数的示例如下方的Pressure类。
        自定义单位转换方法的示例如下方的Temperature类。

        :param value:
        :param unit:
        :return:
        """
        try:
            value = float(value)
        except:
            logger.debug(f"{value=}无法转换单位为{unit}")
        destination_value = self.get_scale_factor(unit) * value
        return destination_value


class Pressure(Unit):
    def __init__(self, unit=None):
        super(Pressure, self).__init__()
        self.allowed_values = ["MPa", "kPa", "Pa", "bar", "hPa"]
        self.sf = [1000000, 1000, 1, 101325, 100]
        if unit is None:
            self.unit = default_unit.P
        elif unit in self.allowed_values:
            self.unit = unit
        else:
            logger.error(f"压力单位不允许为{unit}")
            self.unit = "MPa"


class Velocity(Unit):
    def __init__(self, unit=None):
        super(Velocity, self).__init__()
        self.allowed_values = ["m/s", "km/h"]
        self.sf = [1, 1 / 3.6]
        if unit is None:
            self.unit = default_unit.Velocity
        elif unit in self.allowed_values:
            self.unit = unit
        else:
            logger.error(f"速度单位不允许为{unit}")
            self.unit = "MPa"


class Temperature(Unit):

    def __init__(self, unit=None):
        super(Temperature, self).__init__()
        self.allowed_values = ["℃", "K"]
        if unit is None:
            self.unit = default_unit.T
        elif unit in self.allowed_values:
            self.unit = unit
        else:
            logger.error(f"温度单位不允许为{unit}")
            self.unit = "℃"

    def get_scale_factor(self, unit_str):
        logger.warning(f"温度单位不支持缩放系数转换单位")

    def transfer_to_unit(self, value: float, unit: str):
        try:
            value = float(value)
        except:
            logger.debug(f"{value=}无法转换单位为{unit}")
        if self.unit == unit:
            res = value
        elif self.unit == "℃" and unit == "K":
            res = value + 273.15
        elif self.unit == "K" and unit == "℃":
            res = value - 273.15
        return res


class Enthalpy(Unit):

    def __init__(self, unit="kJ/kg"):
        super(Enthalpy, self).__init__()
        self.allowed_values = ["kJ/kg", "J/g"]
        self.sf = [1, 1]
        if unit is None:
            self.unit = default_unit.Enthalpy
        elif unit in self.allowed_values:
            self.unit = unit
        else:
            logger.error(f"焓单位不允许为{unit}")
            self.unit = "kJ/kg"


class MassFlow(Unit):

    def __init__(self, unit=None):
        super(MassFlow, self).__init__()
        self.allowed_values = ["t/h", "t/s", "kg/s"]
        self.sf = [1 / 3.6, 1000, 1]
        if unit is None:
            self.unit = default_unit.MassFlow
        elif unit in self.allowed_values:
            self.unit = unit
        else:
            logger.error(f"质量流量单位不允许为{unit}")
            self.unit = "t/h"


class VolumeFlow(Unit):
    def __init__(self, unit=None):
        super(VolumeFlow, self).__init__()
        self.allowed_values = ["m^3/h", "m^3/s"]
        self.sf = [1 / 3600, 1]
        if unit is None:
            self.unit = default_unit.VolumeFlow
        elif unit in self.allowed_values:
            self.unit = unit
        else:
            logger.error(f"体积流量单位不允许为{unit}")
            self.unit = "m^3/h"


class SpecificVolume(Unit):
    def __init__(self, unit=None):
        super(SpecificVolume, self).__init__()
        self.allowed_values = ["m^3/kg", ]
        self.sf = [1]
        if unit is None:
            self.unit = default_unit.SpecificVolume
        elif unit in self.allowed_values:
            self.unit = unit
        else:
            logger.error(f"比容单位不允许为{unit}")
            self.unit = "m^3/kg"


class Density(Unit):

    def __init__(self, unit=None):
        super(Density, self).__init__()
        self.allowed_values = ["kg/m^3", ]
        self.sf = [1]
        if unit is None:
            self.unit = default_unit.Density
        elif unit in self.allowed_values:
            self.unit = unit
        else:
            logger.error(f"密度单位不允许为{unit}")
            self.unit = "kg/m^3"


class Power(Unit):

    def __init__(self, unit=None):
        super(Power, self).__init__()
        self.allowed_values = ["MW", "kW", "W"]
        self.sf = [1000000, 1000, 1]
        if unit is None:
            self.unit = default_unit.Power
        elif unit in self.allowed_values:
            self.unit = unit
        else:
            logger.error(f"功率单位不允许为{unit}")
            self.unit = "MW"


class Length(Unit):
    def __init__(self, unit=None):
        super(Length, self).__init__()
        self.allowed_values = ["m", "mm", "km"]
        self.sf = [1, 0.001, 1000]
        if unit is None:
            self.unit = default_unit.Length
        elif unit in self.allowed_values:
            self.unit = unit
        else:
            logger.error(f"长度单位不允许为{unit}")
            self.unit = "m"


class Area(Unit):
    def __init__(self, unit=None):
        super(Area, self).__init__()
        self.allowed_values = ["m^2", "mm^2", "km^2"]
        self.sf = [1, 0.000001, 1000000]
        if unit is None:
            self.unit = default_unit.Area
        elif unit in self.allowed_values:
            self.unit = unit
        else:
            logger.error(f"长度单位不允许为{unit}")
            self.unit = "m^2"


class AngleUnit(Unit):
    def __init__(self, unit=None):
        """
        角度的单位，包括°和rad
        :param unit:
        """
        super(AngleUnit, self).__init__()
        self.allowed_values = ["°", "rad"]
        self.sf = [math.pi / 180, 1]  # 1° = 180/pi rad <== 180° = pi rad
        if unit is None:
            self.unit = default_unit.AngleUnit
        elif unit in self.allowed_values:
            self.unit = unit
        else:
            logger.error(f"角度单位不允许为{unit}")
            self.unit = None


class One(Unit):
    def __int__(self, unit=None):
        """
        无单位的单位，即单位1

        :param unit:
        :return:
        """
        super(One, self).__init__()
        self.allowed_values = ["%", "1", "‰"]  # 不能为None，没有单位，单位就是1，而None表示参数不是数值型，如类型等，这种才是真正的没有单位
        self.sf = [0.01, 1, 0.001, 1]
        if unit in self.allowed_values:
            self.unit = unit
        else:
            self.unit = "1"


class Other(Unit):
    def __init__(self, unit):
        super(Other, self).__init__()
        self.unit = unit


default_unit = DefaultUnit()  # 放到最后初始化，因为该参数的初始化必须等所有的类都加载后才能进行
