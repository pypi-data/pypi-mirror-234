import math
from yangke.performance.tools.const import const
from yangke.common.config import logger


# class Air:
#     """
#     空气物性计算
#
#     """
#
#     def __init__(self, pressure=101.325, rh=None, t_dry=None, t_wet=None):
#         """
#
#         :param pressure: kPa
#         :param rh: 0~1
#         :param t_dry: ℃
#         :param t_wet: ℃
#         """
#         if rh is None and t_dry is None:
#             logger.error("参数不全")
#         elif t_dry is None and t_wet is None:
#             logger.error("参数不全")
#         self.pressure = pressure
#         self.rh = rh
#         self.t_dry = t_dry
#         self.t_wet = t_wet
#         if rh is None:
#             self.分压力 = self.get_分压_水()
#             self.干球饱和压力 = self.get_饱和压力_水(self.t_dry)
#             self.rh = self.get_relative_humidity()
#             self.干空气分数 = self.get_干空气分数()
#         elif t_wet is None:
#             self.分压力 = self.get_分压_水()
#             self.干球饱和压力 = self.get_饱和压力_水(self.t_dry)
#             self.干空气分数 = self.get_干空气分数()
#
#         self.mole_weight = self.摩尔质量 = self.湿空气分子量 = self.get_mole_weight()
#         self.含湿量 = self.get_含湿量()
#
#     def get_relative_humidity(self):
#         """
#         根据干湿球温度求相对湿度
#
#         :return:
#         """
#         return self.分压力 / self.干球饱和压力
#
#     def get_干空气分数(self):
#         t_dry = self.t_dry
#         干球饱和压力 = self.get_饱和压力_水(t_dry) * 1000
#         p_water = self.get_分压_水()
#         return 1 - p_water / self.pressure
#
#     def get_分压_水(self):
#         """
#          参考PTC 4.4-2008联合循环余热锅炉性能试验规程，第36页，第2步
#          干球饱和压力，kPa
#          相对湿度, 0~100
#          @return 分压：kPa
#         :return:
#         """
#         if self.rh > 1:
#             rh = self.rh / 100
#         else:
#             rh = self.rh
#         return rh * self.get_饱和压力_水(t=self.t_dry)
#
#     def get_含湿量(self):
#         """
#         一般所指的含湿量就是质量表示的含湿量
#         湿空气的含湿量定义为是湿空气中水的质量/干空气的质量，也就是常说的含湿量
#         湿空气的湿度系数，质量表示的绝对湿度Humid ratio by mass
#
#         :param t_dry:
#         :param t_wet:
#         :return: 湿度系数： kg/kg
#         """
#         if self.t_wet is not None:
#             t_dry = self.t_dry
#             t_wet = self.t_wet
#             p = self.pressure / 1000  # MPa
#             湿球饱和压力 = self.get_饱和压力_水(t_wet)
#             hr_sat = 0.62198 * (1.0039 * 湿球饱和压力) / (p - 1.0039 * 湿球饱和压力)  # 饱和湿空气的绝对湿度humid ratio
#             hr = (1075.208 - 1.0008 * t_wet) * hr_sat - 0.432 * (t_dry - t_wet)
#             hr = hr / (1075.208 + 0.7992 * t_dry - 1.8 * t_wet)  # 湿空气的绝对湿度，质量表示的绝对湿度Humid ratio by mass
#         else:
#             if self.rh > 1:
#                 rh = self.rh / 100
#             Psd = self.get_饱和压力_水(self.t_dry)
#             hr = 0.622 * rh * Psd * 1000 / (self.pressure * 1000 - rh * Psd * 1000)
#         return hr
#
#     def get_饱和压力_水(self, t=None):
#         """
#         根据温度求水蒸汽饱和压力，参考余热锅炉规程
#
#         :param t:
#         :return: 饱和压力, kPa
#         """
#         if t is None:
#             t = self.t_dry
#         if t < -100:
#             logger.warning(f"干球温度超下限，饱和压力错误，{t=}")
#             return -1
#         elif t > 200:
#             logger.warning(f"干球温度超上限，饱和压力错误，{t=}")
#             return -1
#         if t < 0:
#             c1 = -1.0214165e4
#             c2 = -9.8702328
#             c3 = -5.3765794e-3
#             c4 = -1.9202377e-7
#             c5 = -3.5575832e-10
#             c6 = -9.0344688e-14
#             c7 = -4.1635019
#         else:
#             c1 = -1.0440397e4
#             c2 = -16.27164
#             c3 = -2.7022355e-2
#             c4 = 1.289036e-5
#             c5 = -2.4780681e-9
#             c6 = 0
#             c7 = 6.5459673
#
#         tr = 1.8 * t + 491.67
#         ln_p = c1 / tr + c2 + c3 * tr + c4 * tr * tr + c5 * math.pow(tr, 3) + c6 * math.pow(tr, 4) + c7 * math.log(tr)
#         return math.pow(math.e, ln_p) * 1000
#
#     def get_mole_weight(self):
#         """
#         求湿空气摩尔质量
#
#         :return:
#         """
#         干空气分数 = self.干空气分数
#         frac_mole_N2_dry = 0.78084
#         frac_mole_O2_dry = 0.2094760
#         frac_mole_CO2_dry = 0.0003190
#         frac_mole_H2O_dry = 0
#         frac_mole_Ar_dry = 0.009365
#
#         # 湿空气摩尔分数
#         frac_mole_N2_wet = frac_mole_N2_dry * 干空气分数
#         frac_mole_O2_wet = frac_mole_O2_dry * 干空气分数
#         frac_mole_CO2_wet = frac_mole_CO2_dry * 干空气分数
#         frac_mole_H2O_wet = 1 - 干空气分数
#         frac_mole_Ar_wet = frac_mole_Ar_dry * 干空气分数
#
#         # 摩尔质量
#         mass_mole_N2 = 28.01348
#         mass_mole_O2 = 31.9988
#         mass_mole_CO2 = 44.0098
#         mass_mole_H2O = 18.01528
#         mass_mole_Ar = 39.948
#
#         N2 = frac_mole_N2_wet * mass_mole_N2
#         O2 = frac_mole_O2_wet * mass_mole_O2
#         CO2 = frac_mole_CO2_wet * mass_mole_CO2
#         H2O = frac_mole_H2O_wet * mass_mole_H2O
#         Ar = frac_mole_Ar_wet * mass_mole_Ar
#
#         return N2 + O2 + CO2 + H2O + Ar
#
#     def get_h_component(self, comp, t, t_refer=15):
#         """
#
#         :param comp: 组分名，可取["N2", "O2", "CO2", "H2O", "Ar"]
#         :param t: 空气温度
#         :param t_refer: 参考温度，基准温度
#         :return:
#         """
#         R = 8.31451
#         f = [0] * 11
#         温度_K = t + 273.15
#         基准温度_K = t_refer + 273.15
#
#         组分名 = comp
#         if 组分名 == "N2":
#             f[1] = 22103.715
#             f[2] = -381.84618
#             f[3] = 6.08273836
#             f[4] = -0.008530914
#             f[5] = 0.0000138465
#             f[6] = -0.00000000962579
#             f[7] = 2.51971E-12
#             f[8] = 710.846086
#             f[9] = 0
#             f[10] = 28.0134
#         elif 组分名 == "O2":
#             f[1] = -34255.6342
#             f[2] = 484.700097
#             f[3] = 1.11901096
#             f[4] = 0.004293889
#             f[5] = -0.00000068363
#             f[6] = -0.00000000202337
#             f[7] = 1.03904E-12
#             f[8] = -3391.4549
#             f[9] = 0
#             f[10] = 31.9988
#         elif 组分名 == "CO2":
#             f[1] = 49436.5054
#             f[2] = -626.411601
#             f[3] = 5.30172524
#             f[4] = 0.002503814
#             f[5] = -0.00000021273
#             f[6] = -0.000000000768999
#             f[7] = 2.84968E-13
#             f[8] = -45281.9846
#             f[9] = -393510
#             f[10] = 44.0095
#         elif 组分名 == "H2O":
#             f[1] = -39479.6083
#             f[2] = 575.573102
#             f[3] = 0.931782653
#             f[4] = 0.007222713
#             f[5] = -0.00000734256
#             f[6] = 0.00000000495504
#             f[7] = -1.33693E-12
#             f[8] = -33039.7431
#             f[9] = -241826
#             f[10] = 18.0153
#         elif 组分名 == "Ar":
#             f[1] = 0
#             f[2] = 0
#             f[3] = 2.5
#             f[4] = 0
#             f[5] = 0
#             f[6] = 0
#             f[7] = 0
#             f[8] = -745.375
#             f[9] = 0
#             f[10] = 39.948
#         elif 组分名 == "SO2":
#             f[1] = -53108.4214
#             f[2] = 909.031167
#             f[3] = -2.356891244
#             f[4] = 0.0220445
#             f[5] = -0.0000251078
#             f[6] = 0.000000014463
#             f[7] = -3.36907E-12
#             f[8] = -41137.5212
#             f[9] = -296810
#             f[10] = 64.0638
#         elif 组分名 == "CO":
#             f[1] = 14890.45326
#             f[2] = -292.2285939
#             f[3] = 5.72452717
#             f[4] = -0.008176235
#             f[5] = 0.000014569
#             f[6] = -0.0000000108775
#             f[7] = 3.02794E-12
#             f[8] = -13031.31878
#             f[9] = -110535.196
#             f[10] = 28.0101
#         elif 组分名 == "H2S":
#             f[1] = 9543.80881
#             f[2] = -68.7517508
#             f[3] = 4.05492196
#             f[4] = -0.000301456
#             f[5] = 0.0000037685
#             f[6] = -0.00000000223936
#             f[7] = 3.08686E-13
#             f[8] = -3278.45728
#             f[9] = -20600
#             f[10] = 34.0809
#         elif 组分名 == "H2":
#             f[1] = 40783.2321
#             f[2] = -800.918604
#             f[3] = 8.21470201
#             f[4] = -0.012697145
#             f[5] = 0.0000175361
#             f[6] = -0.0000000120286
#             f[7] = 3.36809E-12
#             f[8] = 2682.484665
#             f[9] = 0
#             f[10] = 2.0159
#         elif 组分名 == "He":
#             f[1] = 0
#             f[2] = 0
#             f[3] = 2.5
#             f[4] = 0
#             f[5] = 0
#             f[6] = 0
#             f[7] = 0
#             f[8] = 745.375
#             f[9] = 0
#             f[10] = 4.0026
#         elif 组分名 == "CH4":
#             f[1] = -176685.0998
#             f[2] = 2786.18102
#             f[3] = -12.0257785
#             f[4] = 0.039176193
#             f[5] = -0.0000361905
#             f[6] = 0.0000000202685
#             f[7] = -4.97671E-12
#             f[8] = -23313.1436
#             f[9] = -74600
#             f[10] = 16.0425
#         elif 组分名 == "C2H6":
#             f[1] = -186204.4161
#             f[2] = 3406.19186
#             f[3] = -19.51705092
#             f[4] = 0.075658356
#             f[5] = -0.0000820417
#             f[6] = 0.0000000506114
#             f[7] = -1.31928E-11
#             f[8] = -27029.3289
#             f[9] = -83851.544
#             f[10] = 30.069
#         elif 组分名 == "C3H8":
#             f[1] = -243314.4337
#             f[2] = 4656.27081
#             f[3] = -29.39466091
#             f[4] = 0.118895275
#             f[5] = -0.000137631
#             f[6] = 0.0000000881482
#             f[7] = -2.34299E-11
#             f[8] = -35403.3527
#             f[9] = -104680
#             f[10] = 44.0956
#         elif 组分名 == "C4H10iso":
#             f[1] = -383446.933
#             f[2] = 7000.03964
#             f[3] = -44.400269
#             f[4] = 0.174618345
#             f[5] = -0.00020782
#             f[6] = 0.000000133979
#             f[7] = -3.55168E-11
#             f[8] = -50340.1889
#             f[9] = -134990
#             f[10] = 58.1222
#         elif 组分名 == "C4H10n":
#             f[1] = -317587.254
#             f[2] = 6176.33182
#             f[3] = -38.9156212
#             f[4] = 0.158465428
#             f[5] = -0.000186005
#             f[6] = 0.000000119968
#             f[7] = -3.20167E-11
#             f[8] = -45403.6339
#             f[9] = -125790
#             f[10] = 58.1222
#         elif 组分名 == "C5H12iso":
#             f[1] = -423190.339
#             f[2] = 6497.1891
#             f[3] = -36.8112697
#             f[4] = 0.153242473
#             f[5] = -0.000154879
#             f[6] = 0.000000087499
#             f[7] = -2.07055E-11
#             f[8] = -51554.1659
#             f[9] = -153700
#             f[10] = 72.1488
#         elif 组分名 == "C5H12n":
#             f[1] = -276889.4625
#             f[2] = 5834.28347
#             f[3] = -36.1754148
#             f[4] = 0.153333971
#             f[5] = -0.00015284
#             f[6] = 0.0000000819109
#             f[7] = -1.79233E-11
#             f[8] = -46653.7525
#             f[9] = -146760
#             f[10] = 72.1488
#         elif 组分名 == "C6H14n":
#             f[1] = -581592.67
#             f[2] = 10790.97724
#             f[3] = -66.3394703
#             f[4] = 0.252371516
#             f[5] = -0.000290434
#             f[6] = 0.00000018022
#             f[7] = -4.61722E-11
#             f[8] = -72715.4457
#             f[9] = -166920
#             f[10] = 86.1754
#         h = ((-f[1] / 温度_K + f[2] * math.log(温度_K) + f[3] * 温度_K + f[4] * 温度_K * 温度_K / 2 +
#               f[5] * math.pow(温度_K, 3) / 3 + f[6] * math.pow(温度_K, 4) / 4
#               + f[7] * math.pow(温度_K, 5) / 5 + f[8]) * R - f[9]) / f[10] / 2.326
#         hr = ((-f[1] / 基准温度_K + f[2] * math.log(基准温度_K) + f[3] * 基准温度_K + f[4] * 基准温度_K * 基准温度_K / 2
#                + f[5] * math.pow(基准温度_K, 3) / 3 + f[6] * math.pow(基准温度_K, 4) / 4
#                + f[7] * math.pow(基准温度_K, 5) / 5 + f[8]) * R - f[9]) / f[10] / 2.326
#         return 2.326 * (h - hr)
#
#     def get_xv_component(self, comp):
#         干空气分数 = self.干空气分数
#         result = const.get("干空气组分").get("摩尔分数")[comp]
#         if result:
#             result = result * 干空气分数
#         else:
#             return 0
#         return result
#
#     def get_xm_component(self, comp):
#         """
#         // 参考ASME PTC4.4-2008英文版45页第10步，中文版37页第10步
#         // 湿空气质量分数
#
#         :param comp:
#         :return:
#         """
#         组分名 = comp
#         frac_mole_N2_wet = self.get_xv_component("N2")
#         frac_mole_O2_wet = self.get_xv_component("O2")
#         frac_mole_CO2_wet = self.get_xv_component("CO2")
#         frac_mole_H2O_wet = self.get_xv_component("H2O")
#         frac_mole_Ar_wet = self.get_xv_component("Ar")
#
#         mass_N2 = frac_mole_N2_wet * 28.0135
#         mass_O2 = frac_mole_O2_wet * 31.9988
#         mass_CO2 = frac_mole_CO2_wet * 44.01
#         mass_H2O = frac_mole_H2O_wet * 18.0153
#         mass_Ar = frac_mole_Ar_wet * 39.948
#         mass = mass_N2 + mass_O2 + mass_CO2 + mass_H2O + mass_Ar
#
#         if 组分名 == "N2":
#             return mass_N2 / mass
#         elif 组分名 == "O2":
#             return mass_O2 / mass
#         elif 组分名 == "CO2":
#             return mass_CO2 / mass
#         elif 组分名 == "H2O":
#             return mass_H2O / mass
#         elif 组分名 == "Ar":
#             return mass_Ar / mass
#         elif 组分名 == "SO2":
#             return 0
#         else:
#             return "组分名错误"
#
#     def get_h(self, t=None, t_refer=15):
#         """
#         求湿空气焓值
#         :return:
#         """
#         if t is None:
#             空气温度 = self.t_dry
#         else:
#             空气温度 = t
#         基准温度_opt = t_refer
#         干空气分数 = self.干空气分数
#         # 组分焓
#         h_N2 = self.get_h_component("N2", 空气温度, 基准温度_opt)
#         h_O2 = self.get_h_component("O2", 空气温度, 基准温度_opt)
#         h_CO2 = self.get_h_component("CO2", 空气温度, 基准温度_opt)
#         h_H2O = self.get_h_component("H2O", 空气温度, 基准温度_opt)
#         h_Ar = self.get_h_component("Ar", 空气温度, 基准温度_opt)
#
#         # 质量分数
#         frac_mass_N2 = self.get_xm_component("N2")
#         frac_mass_O2 = self.get_xm_component("O2")
#         frac_mass_CO2 = self.get_xm_component("CO2")
#         frac_mass_H2O = self.get_xm_component("H2O")
#         frac_mass_Ar = self.get_xm_component("Ar")
#
#         return frac_mass_N2 * h_N2 + frac_mass_O2 * h_O2 + frac_mass_CO2 * h_CO2 + frac_mass_H2O * h_H2O + frac_mass_Ar * h_Ar
#
#     def get_enthalpy(self, t, t_refer=15):
#         return self.get_h(t, t_refer)


class Air:
    """
    空气物性计算

    """

    def __init__(self, pressure=101.325, rh=None, t_dry=None, t_wet=None):
        """
        本方法
        :param pressure: kPa
        :param rh: 0~1
        :param t_dry: ℃
        :param t_wet: ℃
        """
        if rh is None and t_dry is None:
            logger.error("参数不全")
        elif t_dry is None and t_wet is None:
            logger.error("参数不全")
        self.pressure = pressure
        self.rh = rh
        self.t_dry = t_dry
        self.t_wet = t_wet
        if rh is None:
            self.分压力 = self.get_分压_水()
            self.干球饱和压力 = self.get_饱和压力_水(self.t_dry)
            self.rh = self.get_relative_humidity()
            self.干空气分数 = self.get_干空气分数()
        elif t_wet is None:
            self.分压力 = self.get_分压_水()  # 同时设置了self.干球饱和压力
            self.干空气分数 = self.get_干空气分数()

        self.mole_weight = self.摩尔质量 = self.湿空气分子量 = self.get_mole_weight()
        self.含湿量 = self.get_含湿量()

    def get_relative_humidity(self):
        """
        根据干湿球温度求相对湿度

        :return:
        """
        return self.分压力 / self.干球饱和压力

    def get_干空气分数(self):
        t_dry = self.t_dry
        p_water = self.get_分压_水()
        if p_water is not None:
            干球饱和压力 = self.干球饱和压力 * 1000
            return 1 - p_water / self.pressure
        else:
            return None

    def get_分压_水(self):
        """
         参考PTC 4.4-2008联合循环余热锅炉性能试验规程，第36页，第2步
         干球饱和压力，kPa
         相对湿度, 0~100
         @return 分压：kPa
        :return:
        """
        if self.rh > 1:
            rh = self.rh / 100
        else:
            rh = self.rh
        self.干球饱和压力 = self.get_饱和压力_水(t=self.t_dry)
        if self.干球饱和压力 is None:
            return None
        else:
            return rh * self.干球饱和压力

    def get_含湿量(self):
        """
        一般所指的含湿量就是质量表示的含湿量
        湿空气的含湿量定义为是湿空气中水的质量/干空气的质量，也就是常说的含湿量
        湿空气的湿度系数，质量表示的绝对湿度Humid ratio by mass

        :param t_dry:
        :param t_wet:
        :return: 湿度系数： kg/kg
        """
        if self.t_wet is not None:
            t_dry = self.t_dry
            t_wet = self.t_wet
            p = self.pressure / 1000  # MPa
            湿球饱和压力 = self.get_饱和压力_水(t_wet)
            hr_sat = 0.62198 * (1.0039 * 湿球饱和压力) / (p - 1.0039 * 湿球饱和压力)  # 饱和湿空气的绝对湿度humid ratio
            hr = (1075.208 - 1.0008 * t_wet) * hr_sat - 0.432 * (t_dry - t_wet)
            hr = hr / (1075.208 + 0.7992 * t_dry - 1.8 * t_wet)  # 湿空气的绝对湿度，质量表示的绝对湿度Humid ratio by mass
        else:
            if self.rh > 1:
                rh = self.rh / 100
            Psd = self.get_饱和压力_水(self.t_dry)
            if Psd is None:
                return None
            hr = 0.622 * rh * Psd * 1000 / (self.pressure * 1000 - rh * Psd * 1000)
        return hr

    def get_饱和压力_水(self, t=None):
        """
        根据温度求水蒸汽饱和压力，参考余热锅炉规程
        :param t:
        :return: 饱和压力, kPa
        """
        if t is None:
            t = self.t_dry
        if t < -100:
            logger.debug(f"干球温度超下限（-100℃），饱和压力为None，{t=}")
            return None
        elif t > 200:
            logger.debug(f"干球温度超上限（200℃），饱和压力为None，{t=}")
            return None
        if t < 0:
            c1 = -1.0214165e4
            c2 = -9.8702328
            c3 = -5.3765794e-3
            c4 = -1.9202377e-7
            c5 = -3.5575832e-10
            c6 = -9.0344688e-14
            c7 = -4.1635019
        else:
            c1 = -1.0440397e4
            c2 = -16.27164
            c3 = -2.7022355e-2
            c4 = 1.289036e-5
            c5 = -2.4780681e-9
            c6 = 0
            c7 = 6.5459673

        tr = 1.8 * t + 491.67
        ln_p = c1 / tr + c2 + c3 * tr + c4 * tr * tr + c5 * math.pow(tr, 3) + c6 * math.pow(tr, 4) + c7 * math.log(tr)
        return math.pow(math.e, ln_p) * 1000

    def get_mole_weight(self):
        """
        求湿空气摩尔质量

        :return:
        """
        干空气分数 = self.干空气分数
        if 干空气分数 is None:
            return None
        frac_mole_N2_dry = 0.78084
        frac_mole_O2_dry = 0.2094760
        frac_mole_CO2_dry = 0.0003190
        frac_mole_H2O_dry = 0
        frac_mole_Ar_dry = 0.009365

        # 湿空气摩尔分数
        frac_mole_N2_wet = frac_mole_N2_dry * 干空气分数
        frac_mole_O2_wet = frac_mole_O2_dry * 干空气分数
        frac_mole_CO2_wet = frac_mole_CO2_dry * 干空气分数
        frac_mole_H2O_wet = 1 - 干空气分数
        frac_mole_Ar_wet = frac_mole_Ar_dry * 干空气分数

        # 摩尔质量
        mass_mole_N2 = 28.01348
        mass_mole_O2 = 31.9988
        mass_mole_CO2 = 44.0098
        mass_mole_H2O = 18.01528
        mass_mole_Ar = 39.948

        N2 = frac_mole_N2_wet * mass_mole_N2
        O2 = frac_mole_O2_wet * mass_mole_O2
        CO2 = frac_mole_CO2_wet * mass_mole_CO2
        H2O = frac_mole_H2O_wet * mass_mole_H2O
        Ar = frac_mole_Ar_wet * mass_mole_Ar

        return N2 + O2 + CO2 + H2O + Ar

    def get_h_component(self, comp, t, t_refer=15):
        """

        :param comp: 组分名，可取["N2", "O2", "CO2", "H2O", "Ar"]
        :param t: 空气温度
        :param t_refer: 参考温度，基准温度
        :return:
        """
        R = 8.31451
        f = [0] * 11
        温度_K = t + 273.15
        基准温度_K = t_refer + 273.15

        组分名 = comp
        if 组分名 == "N2":
            f[1] = 22103.715
            f[2] = -381.84618
            f[3] = 6.08273836
            f[4] = -0.008530914
            f[5] = 0.0000138465
            f[6] = -0.00000000962579
            f[7] = 2.51971E-12
            f[8] = 710.846086
            f[9] = 0
            f[10] = 28.0134
        elif 组分名 == "O2":
            f[1] = -34255.6342
            f[2] = 484.700097
            f[3] = 1.11901096
            f[4] = 0.004293889
            f[5] = -0.00000068363
            f[6] = -0.00000000202337
            f[7] = 1.03904E-12
            f[8] = -3391.4549
            f[9] = 0
            f[10] = 31.9988
        elif 组分名 == "CO2":
            f[1] = 49436.5054
            f[2] = -626.411601
            f[3] = 5.30172524
            f[4] = 0.002503814
            f[5] = -0.00000021273
            f[6] = -0.000000000768999
            f[7] = 2.84968E-13
            f[8] = -45281.9846
            f[9] = -393510
            f[10] = 44.0095
        elif 组分名 == "H2O":
            f[1] = -39479.6083
            f[2] = 575.573102
            f[3] = 0.931782653
            f[4] = 0.007222713
            f[5] = -0.00000734256
            f[6] = 0.00000000495504
            f[7] = -1.33693E-12
            f[8] = -33039.7431
            f[9] = -241826
            f[10] = 18.0153
        elif 组分名 == "Ar":
            f[1] = 0
            f[2] = 0
            f[3] = 2.5
            f[4] = 0
            f[5] = 0
            f[6] = 0
            f[7] = 0
            f[8] = -745.375
            f[9] = 0
            f[10] = 39.948
        elif 组分名 == "SO2":
            f[1] = -53108.4214
            f[2] = 909.031167
            f[3] = -2.356891244
            f[4] = 0.0220445
            f[5] = -0.0000251078
            f[6] = 0.000000014463
            f[7] = -3.36907E-12
            f[8] = -41137.5212
            f[9] = -296810
            f[10] = 64.0638
        elif 组分名 == "CO":
            f[1] = 14890.45326
            f[2] = -292.2285939
            f[3] = 5.72452717
            f[4] = -0.008176235
            f[5] = 0.000014569
            f[6] = -0.0000000108775
            f[7] = 3.02794E-12
            f[8] = -13031.31878
            f[9] = -110535.196
            f[10] = 28.0101
        elif 组分名 == "H2S":
            f[1] = 9543.80881
            f[2] = -68.7517508
            f[3] = 4.05492196
            f[4] = -0.000301456
            f[5] = 0.0000037685
            f[6] = -0.00000000223936
            f[7] = 3.08686E-13
            f[8] = -3278.45728
            f[9] = -20600
            f[10] = 34.0809
        elif 组分名 == "H2":
            f[1] = 40783.2321
            f[2] = -800.918604
            f[3] = 8.21470201
            f[4] = -0.012697145
            f[5] = 0.0000175361
            f[6] = -0.0000000120286
            f[7] = 3.36809E-12
            f[8] = 2682.484665
            f[9] = 0
            f[10] = 2.0159
        elif 组分名 == "He":
            f[1] = 0
            f[2] = 0
            f[3] = 2.5
            f[4] = 0
            f[5] = 0
            f[6] = 0
            f[7] = 0
            f[8] = 745.375
            f[9] = 0
            f[10] = 4.0026
        elif 组分名 == "CH4":
            f[1] = -176685.0998
            f[2] = 2786.18102
            f[3] = -12.0257785
            f[4] = 0.039176193
            f[5] = -0.0000361905
            f[6] = 0.0000000202685
            f[7] = -4.97671E-12
            f[8] = -23313.1436
            f[9] = -74600
            f[10] = 16.0425
        elif 组分名 == "C2H6":
            f[1] = -186204.4161
            f[2] = 3406.19186
            f[3] = -19.51705092
            f[4] = 0.075658356
            f[5] = -0.0000820417
            f[6] = 0.0000000506114
            f[7] = -1.31928E-11
            f[8] = -27029.3289
            f[9] = -83851.544
            f[10] = 30.069
        elif 组分名 == "C3H8":
            f[1] = -243314.4337
            f[2] = 4656.27081
            f[3] = -29.39466091
            f[4] = 0.118895275
            f[5] = -0.000137631
            f[6] = 0.0000000881482
            f[7] = -2.34299E-11
            f[8] = -35403.3527
            f[9] = -104680
            f[10] = 44.0956
        elif 组分名 == "C4H10iso":
            f[1] = -383446.933
            f[2] = 7000.03964
            f[3] = -44.400269
            f[4] = 0.174618345
            f[5] = -0.00020782
            f[6] = 0.000000133979
            f[7] = -3.55168E-11
            f[8] = -50340.1889
            f[9] = -134990
            f[10] = 58.1222
        elif 组分名 == "C4H10n":
            f[1] = -317587.254
            f[2] = 6176.33182
            f[3] = -38.9156212
            f[4] = 0.158465428
            f[5] = -0.000186005
            f[6] = 0.000000119968
            f[7] = -3.20167E-11
            f[8] = -45403.6339
            f[9] = -125790
            f[10] = 58.1222
        elif 组分名 == "C5H12iso":
            f[1] = -423190.339
            f[2] = 6497.1891
            f[3] = -36.8112697
            f[4] = 0.153242473
            f[5] = -0.000154879
            f[6] = 0.000000087499
            f[7] = -2.07055E-11
            f[8] = -51554.1659
            f[9] = -153700
            f[10] = 72.1488
        elif 组分名 == "C5H12n":
            f[1] = -276889.4625
            f[2] = 5834.28347
            f[3] = -36.1754148
            f[4] = 0.153333971
            f[5] = -0.00015284
            f[6] = 0.0000000819109
            f[7] = -1.79233E-11
            f[8] = -46653.7525
            f[9] = -146760
            f[10] = 72.1488
        elif 组分名 == "C6H14n":
            f[1] = -581592.67
            f[2] = 10790.97724
            f[3] = -66.3394703
            f[4] = 0.252371516
            f[5] = -0.000290434
            f[6] = 0.00000018022
            f[7] = -4.61722E-11
            f[8] = -72715.4457
            f[9] = -166920
            f[10] = 86.1754
        h = ((-f[1] / 温度_K + f[2] * math.log(温度_K) + f[3] * 温度_K + f[4] * 温度_K * 温度_K / 2 +
              f[5] * math.pow(温度_K, 3) / 3 + f[6] * math.pow(温度_K, 4) / 4
              + f[7] * math.pow(温度_K, 5) / 5 + f[8]) * R - f[9]) / f[10] / 2.326
        hr = ((-f[1] / 基准温度_K + f[2] * math.log(基准温度_K) + f[3] * 基准温度_K + f[4] * 基准温度_K * 基准温度_K / 2
               + f[5] * math.pow(基准温度_K, 3) / 3 + f[6] * math.pow(基准温度_K, 4) / 4
               + f[7] * math.pow(基准温度_K, 5) / 5 + f[8]) * R - f[9]) / f[10] / 2.326
        return 2.326 * (h - hr)

    def get_xv_component(self, comp):
        """
        获取空气中组分的体积分数

        :param comp:
        :return:
        """
        干空气分数 = self.干空气分数
        if 干空气分数 is None:
            return None
        result = const.get("干空气组分").get("摩尔分数")[comp]
        if result:
            result = result * 干空气分数
        else:
            return 0
        return result

    def get_xm_component(self, comp):
        """
        // 参考ASME PTC4.4-2008英文版45页第10步，中文版37页第10步
        // 湿空气质量分数

        :param comp:
        :return:
        """
        组分名 = comp
        if self.干空气分数 is None:
            return None
        frac_mole_N2_wet = self.get_xv_component("N2")
        frac_mole_O2_wet = self.get_xv_component("O2")
        frac_mole_CO2_wet = self.get_xv_component("CO2")
        frac_mole_H2O_wet = self.get_xv_component("H2O")
        frac_mole_Ar_wet = self.get_xv_component("Ar")

        mass_N2 = frac_mole_N2_wet * 28.0135
        mass_O2 = frac_mole_O2_wet * 31.9988
        mass_CO2 = frac_mole_CO2_wet * 44.01
        mass_H2O = frac_mole_H2O_wet * 18.0153
        mass_Ar = frac_mole_Ar_wet * 39.948
        mass = mass_N2 + mass_O2 + mass_CO2 + mass_H2O + mass_Ar

        if 组分名 == "N2":
            return mass_N2 / mass
        elif 组分名 == "O2":
            return mass_O2 / mass
        elif 组分名 == "CO2":
            return mass_CO2 / mass
        elif 组分名 == "H2O":
            return mass_H2O / mass
        elif 组分名 == "Ar":
            return mass_Ar / mass
        elif 组分名 == "SO2":
            return 0
        else:
            return "组分名错误"

    def get_h(self, t=None, t_refer=15):
        """
        求湿空气焓值
        :return:
        """
        if t is None:
            空气温度 = self.t_dry
        else:
            空气温度 = t
        基准温度_opt = t_refer
        干空气分数 = self.干空气分数
        if 干空气分数 is None:
            return None
        # 组分焓
        h_N2 = self.get_h_component("N2", 空气温度, 基准温度_opt)
        h_O2 = self.get_h_component("O2", 空气温度, 基准温度_opt)
        h_CO2 = self.get_h_component("CO2", 空气温度, 基准温度_opt)
        h_H2O = self.get_h_component("H2O", 空气温度, 基准温度_opt)
        h_Ar = self.get_h_component("Ar", 空气温度, 基准温度_opt)

        # 质量分数
        frac_mass_N2 = self.get_xm_component("N2")
        frac_mass_O2 = self.get_xm_component("O2")
        frac_mass_CO2 = self.get_xm_component("CO2")
        frac_mass_H2O = self.get_xm_component("H2O")
        frac_mass_Ar = self.get_xm_component("Ar")

        return frac_mass_N2 * h_N2 + frac_mass_O2 * h_O2 + frac_mass_CO2 * h_CO2 + frac_mass_H2O * h_H2O + frac_mass_Ar * h_Ar

    def get_enthalpy(self, t, t_refer=15):
        return self.get_h(t, t_refer)


if __name__ == "__main__":
    air = Air(pressure=98.31, t_dry=200.58, rh=67.73)
    print(air.get_h(t_refer=15))
