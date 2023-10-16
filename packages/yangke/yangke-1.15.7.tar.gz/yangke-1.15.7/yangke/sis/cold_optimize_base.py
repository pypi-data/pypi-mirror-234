import math
from yangke.base import find_nearest_points, interpolate_value_complex, interpolate_nd, interpolate_value_simple

from yangke.common.config import logger
from yangke.performance.iapws97 import get_h_by_pt, get_t_by_p, get_p_by_t, get_rho_by_pt
import pandas as pd


class Condenser:
    def __init__(self):
        self.类型 = "单背压"
        self.设计凝汽器热负荷 = None  # 凝汽器热负荷，设计工况
        self.管子材料 = None
        self.管子数量 = None  # 管子数量
        self.管子热导率 = None  # 管子热导率
        self.管子外径 = None  # 管子外径
        self.管子壁厚 = None  # 管子壁厚
        self.管子内径 = None  # 管子内径
        self.有效长度 = None  # 有效长度，m
        self.有效换热面积 = None  # 管子外表面积，m^2，也就是冷却面积
        self.冷却水流通面积 = None  # 冷却水流通面积
        self.设计总体换热系数 = None  # W/(m^2.℃)
        self.t_cyc_in_d = None  # 冷却水进口温度，设计工况
        self.t_cyc_out_d = None  # 冷却水出口温度，设计工况
        self.设计循环水温升 = None  # 冷却水温升，设计工况
        self.设计循环水流量_t_h = None  # 冷却水流量，设计工况，t/h
        self.设计循环水流量_m3_h = None  # 冷却水流量，设计工况，m^3/h
        self.设计循环水流速 = None  # m/s
        self.设计洁净度 = None  # 洁净度，设计工况
        self.设计背压 = None  # 凝汽器压力，设计工况
        self.设计端差 = None  # 凝汽器端差，设计工况
        self.设计水阻 = None  # 水阻，设计工况
        self.设计凝结水流量 = None  # 凝结水流量，设计工况
        self.设计循环水密度 = None

    def set_info(self, 类型=None, 设计凝汽器热负荷=None, 管子材料=None, 管子数量=None, 有效长度=None, 管子外径=None,
                 管子壁厚=None, 设计总体换热系数=None,
                 t_cyc_in=None, 循环水温升=None,
                 循环水体积流量=None, 循环水质量流量=None, 设计循环水流速=None,
                 bp=None, 有效换热面积=None, 洁净度=None,
                 ):
        """
        :param 类型: 凝汽器类型，可以取值为：'单背压', '双倍压'
        :param 设计凝汽器热负荷：MW
        :param 管子材料: 可以取值：TP304L
        :param 管子数量: 管子数量，包括：管束顶部外围部分数量、管束主凝汽器区数量和管束抽出空气区数量
        :param 管子外径: mm
        :param 管子壁厚: mm
        :param 设计总体换热系数: W/(m^2.℃)，注意不是换热系数，设计文件中给的换热系数可能是基本换热系数
        :param 设计循环水流速: m/s
        :param 有效换热面积: 凝汽器中所有管子的外表面积之和
        :
        """
        self.类型 = 类型
        self.设计凝汽器热负荷 = 设计凝汽器热负荷
        self.管子材料 = 管子材料
        self.管子数量 = 管子数量
        self.有效长度 = 有效长度
        self.管子外径 = 管子外径
        self.管子壁厚 = 管子壁厚
        self.有效换热面积 = 有效换热面积
        self.设计总体换热系数 = 设计总体换热系数
        self.t_cyc_in_d = t_cyc_in
        self.设计循环水温升 = 循环水温升
        self.设计背压 = bp
        self.设计洁净度 = 洁净度
        self.设计循环水流量_t_h = 循环水质量流量
        self.设计循环水流量_m3_h = 循环水体积流量
        self.设计循环水流速 = 设计循环水流速

        if self.t_cyc_in_d is not None and self.t_cyc_out_d is not None:
            self.设计循环水密度 = get_rho_by_pt(0.35, (self.t_cyc_in_d + self.t_cyc_out_d) / 2)
        if self.t_cyc_in_d is not None:
            self.设计循环水密度 = get_rho_by_pt(0.4, self.t_cyc_in_d)
        elif self.t_cyc_out_d is not None:
            self.设计循环水密度 = get_rho_by_pt(0.3, self.t_cyc_out_d)
        else:
            self.设计循环水密度 = 998  # 0.35MPa,20℃时水的密度

        # 因为大部分情况下，凝汽器内各个换热区域，管子内外径不相同，因此，尽量不使用管子内外径计算冷却水流通面积
        if self.管子外径 is not None and self.管子壁厚 is not None:
            self.管子内径 = self.管子外径 - self.管子壁厚 * 2
        elif self.管子内径 is not None and self.管子壁厚 is not None:
            self.管子外径 = self.管子内径 + self.管子壁厚 * 2

        if self.有效换热面积 is None:
            if self.管子数量 is not None:
                _area = math.pi * (self.管子外径 ** 2 / 4) / 1000 / 1000  # m^2
                self.有效换热面积 = _area * self.管子数量
            else:
                logger.warning(f"缺少凝汽器有效换热面积或管子数量")

        if self.设计循环水流量_t_h is not None and self.设计循环水流量_m3_h is None:
            self.设计循环水流量_m3_h = self.设计循环水流量_t_h / (self.设计循环水密度 / 1000)
        elif self.设计循环水流量_m3_h is not None and self.设计循环水流量_t_h is None:
            self.设计循环水流量_t_h = self.设计循环水流量_m3_h * (self.设计循环水密度 / 1000)
        if self.设计循环水流速 is not None:
            self.冷却水流通面积 = self.设计循环水流量_m3_h / (self.设计循环水流速 * 3600)  # m3/h/m/h
        else:
            if self.冷却水流通面积 is None:
                if self.管子数量 is not None:
                    _area = math.pi * (self.管子内径 ** 2 / 4) / 1000 / 1000  # m^2
                    # 不理解冷却水流通面积为什么要除以2，但除以2的结果确实能对上其他数据，可能是因为管子在凝汽器中流程为2，导致管子数量计算时
                    # 1根管子被计算了两次
                    self.冷却水流通面积 = _area * self.管子数量 / 2
                else:
                    logger.warning("缺少冷却水流通面积")

        if self.设计循环水温升 is not None and self.t_cyc_in_d is not None:
            self.t_cyc_out_d = self.t_cyc_in_d + self.设计循环水温升
        elif self.设计循环水温升 is not None and self.t_cyc_out_d is not None:
            self.t_cyc_in_d = self.t_cyc_out_d - self.设计循环水温升
        elif self.t_cyc_out_d is not None and self.t_cyc_in_d is not None:
            self.设计循环水温升 = self.t_cyc_out_d - self.t_cyc_in_d
        else:
            if self.设计凝汽器热负荷 is not None and self.设计循环水流量_t_h is not None:
                self.设计循环水温升 = self.设计凝汽器热负荷 * 1000 / 4200 / (self.设计循环水流量_t_h / 3600)
            if self.设计循环水温升 is not None and self.t_cyc_in_d is not None:
                self.t_cyc_out_d = self.t_cyc_in_d + self.设计循环水温升
            elif self.设计循环水温升 is not None and self.t_cyc_out_d is not None:
                self.t_cyc_in_d = self.t_cyc_out_d - self.设计循环水温升

        if self.设计凝汽器热负荷 is None:
            if self.设计循环水流量_t_h is not None and self.t_cyc_out_d is not None and self.t_cyc_in_d is not None:
                self.设计凝汽器热负荷 = self.设计循环水流量_t_h * (
                        get_h_by_pt(0.4, self.t_cyc_out_d) - get_h_by_pt(0.24, self.t_cyc_in_d)) / 3600  # MW

        if self.设计循环水流速 is None:
            self.设计循环水流速 = self.设计循环水流量_m3_h / self.冷却水流通面积 * 3600  # m/s

        if self.设计总体换热系数 is None:
            _ln_t = self.cal_对流平均温差(self.t_cyc_out_d, self.t_cyc_in_d, self.设计背压)
            self.设计总体换热系数 = self.设计凝汽器热负荷 / _ln_t / self.有效换热面积 * 1000000

    @staticmethod
    def cal_冷却水进口温度修正系数(t_cyc_cold):
        """
        计算冷却水进口温度修正系数，参照：DL/T 932 凝汽器与真空系统运行维护导则，附录C

        :param t_cyc_cold:
        :return:
        """
        table_c2 = [[0.0, 0.669], [16.5, 0.938], [33.0, 1.079],
                    [0.5, 0.677], [17.0, 0.946], [33.5, 1.081],
                    [1.0, 0.685], [17.5, 0.955], [34.0, 1.083],
                    [1.5, 0.693], [18.0, 0.963], [34.5, 1.085],
                    [2.0, 0.702], [18.5, 0.970], [35.0, 1.088],
                    [2.5, 0.711], [19.0, 0.976], [35.5, 1.090],
                    [3.0, 0.719], [19.5, 0.983], [36.0, 1.092],
                    [3.5, 0.727], [20.0, 0.989], [36.5, 1.094],
                    [4.0, 0.735], [20.5, 0.994], [37.0, 1.096],
                    [4.5, 0.744], [21.0, 0.999], [37.5, 1.099],
                    [5.0, 0.752], [21.5, 1.004], [38.0, 1.101],
                    [5.5, 0.760], [22.0, 1.008], [38.5, 1.104],
                    [6.0, 0.768], [22.5, 1.013], [39.0, 1.106],
                    [6.5, 0.777], [23.0, 1.017], [39.5, 1.108],
                    [7.0, 0.785], [23.5, 1.022], [40.0, 1.110],
                    [7.5, 0.794], [24.0, 1.026], [40.5, 1.113],
                    [8.0, 0.802], [24.5, 1.029], [41.0, 1.115],
                    [8.5, 0.810], [25.0, 1.033], [41.5, 1.116],
                    [9.0, 0.818], [25.5, 1.037], [42.0, 1.118],
                    [9.5, 0.826], [26.0, 1.040], [42.5, 1.120],
                    [10.0, 0.834], [26.5, 1.044], [43.0, 1.122],
                    [10.5, 0.842], [27.0, 1.047], [43.5, 1.124],
                    [11.0, 0.850], [27.5, 1.050], [44.0, 1.125],
                    [11.5, 0.858], [28.0, 1.052], [44.5, 1.127],
                    [12.0, 0.866], [28.5, 1.055], [45.0, 1.129],
                    [12.5, 0.875], [29.0, 1.058], [45.5, 1.131],
                    [13.0, 0.883], [29.5, 1.060], [46.0, 1.133],
                    [13.5, 0.891], [30.0, 1.063], [46.5, 1.134],
                    [14.0, 0.899], [30.5, 1.066], [47.0, 1.136],
                    [14.5, 0.906], [31.0, 1.068], [47.5, 1.138],
                    [15.0, 0.914], [31.5, 1.071], [48.0, 1.140],
                    [15.5, 0.922], [32.0, 1.074], [48.5, 1.142],
                    [16.0, 0.930], [32.5, 1.077]]
        x_list = [x[0] for x in table_c2]
        y_list = [x[1] for x in table_c2]
        return interpolate_value_complex(t_cyc_cold, x_list=x_list, y_list=y_list)

    @staticmethod
    def cal_基本传热系数K0(管内平均流速, 管子外径):
        """
        计算基本传热系数，参照：DL/T 932 凝汽器与真空系统运行维护导则，附录C

        :param 管内平均流速: m/s
        :param 管子外径: mm
        :return: 基本传热系数，单位为W/(m^2.℃)
        """

        # 表C.1的数据记录在sample中
        sample = pd.DataFrame(
            data=[
                [2743.0, 3004.8, 3245.6, 3469.7, 3576.4, 3680.1,
                 3781.0, 3879.2, 3975.0, 4068.5, 4160.0, 4249.4,
                 4405.0, 4550.1, 4686.1, 4814.0, 4933.8, 5047.0],
                [2717.0, 2976.3, 3214.8, 3436.8, 3542.5, 3645.2,
                 3745.1, 3842.4, 3937.3, 4030.0, 4120.5, 4209.2,
                 4363.1, 4506.0, 4640.1, 4766.0, 4884.0, 4995.2],
                [2691.0, 2947.8, 3184.0, 3403.9, 3508.6, 3610.4,
                 3709.3, 3805.6, 3899.6, 3991.4, 4081.1, 4168.9,
                 4320.9, 4461.2, 4592.9, 4716.7, 4832.4, 4941.5],
                [2665.0, 2919.4, 3153.3, 3371.0, 3474.7, 3575.5,
                 3673.4, 3768.9, 3862.0, 3952.8, 4041.7, 4128.6,
                 4278.5, 4415.9, 4544.8, 4666.4, 4779.3, 4886.1],
                [2639.0, 2890.9, 3122.5, 3338.1, 3440.8, 3540.6,
                 3637.6, 3732.1, 3824.3, 3914.3, 4002.2, 4088.3,
                 4236.6, 4372.2, 4499.4, 4619.0, 4730.1, 4835.4],
                [2613.0, 2862.4, 3091.7, 3305.2, 3406.9, 3505.7,
                 3601.8, 3695.3, 3786.6, 3875.7, 3962.8, 4048.0,
                 4193.6, 4327.4, 4452.8, 4570.6, 4680.1, 4783.9],
            ],
            columns=[1.0, 1.2, 1.4, 1.6, 1.7, 1.8,
                     1.9, 2.0, 2.1, 2.2, 2.3, 2.4,
                     2.6, 2.8, 3.0, 3.2, 3.4, 3.6],
            index=[18, 22, 26, 30, 34, 38]
        )
        # 获取与管子外径最接近的外径
        if 管子外径 < 18 or 管子外径 > 38:
            logger.warning(f"冷却管外径超范围，允许的外径范围为18~38mm，指定的凝汽器管子外径为{管子外径}mm")
        if 管内平均流速 < 1.0 or 管内平均流速 > 3.6:
            logger.warning(f"冷却管内流速超范围，允许的流速范围为1.0~3.6m/s，当前流速为{管内平均流速}m/s")
        d1, d2 = find_nearest_points(管子外径, x_list=list(sample.index))
        list1 = sample.loc[d1]
        if isinstance(d2, str):
            res = interpolate_value_complex(管内平均流速, x_list=list(list1.index), y_list=list(list1.values))
        else:
            list2 = sample.loc[d2]
            y1 = interpolate_value_complex(管内平均流速, x_list=list(list1.index), y_list=list(list1.values))
            y2 = interpolate_value_complex(管内平均流速, x_list=list(list2.index), y_list=list(list2.values))
            res = interpolate_value_simple(管子外径, d1, y1, d2, y2)
        return res

    def cal_管材和壁厚修正系数(self):
        thick_list = [0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.2, 1.5, 2.0]
        if self.管子材料 is None or self.管子材料 in ["TP304", "TP304L", "TP316", "TP317"]:
            c3 = [0.912, 0.889, 0.863, 0.840, 0.818, 0.798, 0.759, 0.712, 0.637]
        elif self.管子材料 in ["HSn70-1"]:
            c3 = [1.030, 1.025, 1.020, 1.015, 1.009, 1.007, 1.001, 0.987, 0.965]
        elif self.管子材料 in ["HA177-2"]:
            c3 = [1.032, 1.020, 1.020, 1.015, 1.009, 1.004, 0.993, 0.977, 0.955]
        elif self.管子材料 in ["BFe30-1-1"]:
            c3 = [1.002, 0.990, 0.981, 0.970, 0.959, 0.951, 0.934, 0.905, 0.859]
        elif self.管子材料 in ["BFe10-1-1"]:
            c3 = [0.970, 0.965, 0.951, 0.935, 0.918, 0.908, 0.885, 0.849, 0.792]
        elif self.管子材料 in ["碳钢"]:
            c3 = [1.000, 0.995, 0.981, 0.975, 0.969, 0.958, 0.935, 0.905, 0.859]
        elif self.管子材料 in ["TA1", "TA2"]:
            c3 = [0.952, 0.929, 0.911, 0.895, 0.878, 0.861, 0.828, 0.789, 0.724]
        else:
            logger.warning(f"未查询到指定的管材（{self.管子材料}）的壁厚修正系数，默认去碳钢的壁厚修正系数")
            c3 = [1.000, 0.995, 0.981, 0.975, 0.969, 0.958, 0.935, 0.905, 0.859]

        k = interpolate_value_complex(self.管子壁厚, x_list=thick_list, y_list=c3)
        return k

    @staticmethod
    def cal_对流平均温差(t_cyc_hot, t_cyc_cold, bp):
        """
        计算对流平均换热温差

        :param t_cyc_hot: 出凝汽器循环水温度，℃
        :param t_cyc_cold: 进凝汽器循环水温度，℃
        :param bp: 凝汽器压力, kPa
        """
        t_sat_bp = get_t_by_p(bp / 1000)
        delta_t_ln = (t_cyc_hot - t_cyc_cold) / math.log((t_sat_bp - t_cyc_cold) / (t_sat_bp - t_cyc_hot))
        return delta_t_ln

    @staticmethod
    def cal_端差(t_cyc_hot, bp):
        t_sat_bp = get_t_by_p(bp / 1000)
        return t_sat_bp - t_cyc_hot

    def cal_kc(self, beta_t, beta_td, flow_d):
        """
        计算修正到设计条件下的凝汽器传热系数

        :param beta_t: 凝汽器运行清洁度
        :param beta_td: 设计冷却水进口温度修正系数
        :param flow_d: 设计冷却水流量
        """
        kc = kt * beta_c / beta_t * beta_td / beta_t1 * math.sqrt(flow_d / flow)
        return kc

    def cal_管内平均流速(self, 循环水体积流量=None, 循环水质量流量=None):
        """

        :param 循环水体积流量: t/h
        :param 循环水质量流量: t/h
        :return:  m/s
        """
        if 循环水体积流量 is None and 循环水质量流量 is None:
            logger.error("请传入循环水流量以计算流速")
        elif 循环水体积流量 is None:
            循环水体积流量 = 循环水质量流量 / (self.设计循环水密度 / 1000)
        v = 循环水体积流量 / self.冷却水流通面积  # m3/h /m2 = m/h
        return v / 3600  # m/s

    def cal_运行清洁度系数(self, 凝汽器热负荷, t_cyc_hot, t_cyc_cold, bp, 循环水流量, 冷却管管材和壁厚修正系数,
                    ):
        """
        计算凝汽器运行清洁度，即运行清洁系数、

        :param 凝汽器热负荷: MW
        :param t_cyc_hot: 出凝汽器循环水温度，℃
        :param t_cyc_cold: 进凝汽器循环水温度，℃
        :param bp: 背压，kPa
        :param 循环水流量: t/h
        """
        总体换热系数 = 凝汽器热负荷 / self.有效换热面积 / self.cal_对流平均温差(t_cyc_hot, t_cyc_cold, bp)
        基本传热系数 = self.设计总体换热系数 / math.sqrt(self.cal_管内平均流速(循环水质量流量=循环水流量))
        冷却水进口温度修正系数 = self.cal_冷却水进口温度修正系数(t_cyc_cold)
        冷却管管材和壁厚修正系数 = self.cal_管材和壁厚修正系数()
        清洁度系数 = 总体换热系数 / 基本传热系数 / 冷却管管材和壁厚修正系数 / 冷却水进口温度修正系数 / 1000

    def cal_t_sc(self, t_1d, flow_d):
        """
        计算修正到设计冷却水进口温度和流量下的凝汽器饱和温度

        :param t_1d: 设计冷却水进口温度
        :param flow_d: 设计冷却水流量
        """
        t_sc = t_1d + Q / (flow_d * c_p * (1 - math.exp(kc * a / flow_d / c_p)))
        return t_sc

    def cal_p_sc(self, t_1d, flow_d):
        """
        计算修正到设计冷却水进口温度和流量下的凝汽器压力

        :param t_1d: 设计冷却水进口温度
        :param flow_d: 设计冷却水流量
        """
        t_sc = self.cal_t_sc(t_1d, flow_d)
        return get_p_by_t(t_sc)
