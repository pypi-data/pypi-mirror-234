"""
本模块使用iapws-97水及水蒸汽参数计算公式计算
"""
import traceback
from yangke.ebsilon.values import Value
import iapws
from iapws.iapws97 import IAPWS97
from iapws.iapws95 import IAPWS95
from yangke.common.config import logger

"""
iapws模块中各物理量的字母及单位如下：
P       MPa         压力                              
T       K           温度                              
s       kJ/kgK      熵                               
h       kJ/kg       焓           
v       m3/kg       比容       
rho     kg/m3       密度
nu      m2/s        运动粘度
Hvap    kJ/kg       汽化热
k       W/mK        导热系数   
cp      kJ/kgK      定压比热容     
cv      kJ/kgK      定容比热容
w       m/s         声速          
alfav   1/K         等压膨胀系数Cubic expansion coefficient
其他参见：https://blog.csdn.net/weixin_30608131/article/details/95455984
"""


def water(p=None, t=None, h=None, x=None):
    """
    定义水或水蒸汽状态

    :param p: MPa
    :param t: ℃
    :param h: kJ/kg
    :param x: 干度0~1
    :return:
    """
    if p is not None and t is not None:
        if isinstance(p, Value):
            p = p.get_value_with_unit("MPa")
        if isinstance(t, Value):
            t = t.get_value_with_unit("℃")
        h2o = IAPWS97(P=p, T=t + 273.15)
    elif p is not None and h is not None:
        if isinstance(p, Value):
            p = p.get_value_with_unit("MPa")
        if isinstance(h, Value):
            h = h.get_value_with_unit("kJ/kg")
        h2o = iapws.iapws97.IAPWS97_Ph(P=p, h=h)
    elif p is not None and x is not None:
        h2o = iapws.iapws97.IAPWS97_Px(P=p, x=x)
    elif t is not None and x is not None:
        h2o = iapws.iapws97.IAPWS97_Tx(T=t + 273.15, x=x)
    elif t is not None and h is not None:
        h2o = iapws.iapws97.IAPWS97(P=p, T=t + 273.15)
    return h2o


def get_p_by_th(t, h):
    """
    根据h和t求p

    :param h: 焓，单位为 kJ/kg
    :param t: 温度，单位为 ℃
    :return: 压力，单位为 MPa
    """
    if isinstance(h, Value):
        h = h.get_value_with_unit("kJ/kg")
    if isinstance(t, Value):
        t = t.get_value_with_unit("℃")
    t_K = t + 273.15
    # 因为IAPWS97不能根据 焓 和 温度 求 压力，这里借助IAPWS95进行查找求解
    # 即多次计算 get_h_by_pt，对比计算的焓值与给定焓值相等则返回对应的p
    p = IAPWS95(h=h, T=t_K).P  # 该函数有时候结果很离谱，如焓值为763.9，温度为177.4℃时
    h_1 = get_h_by_pt(p=p, t=t)
    if h_1 > h:  # 温度不变时，压力越大，焓越低，考虑绝热管道的蒸汽流动，等焓，pt都降低
        # 说明估计的p偏小
        p_min = p
        p_max = p + 0.01
        while get_h_by_pt(p=p_max, t=t) > h:
            p_max = p_max + 0.01

    else:
        # 说明估计的p偏大
        p_max = p
        p_min = p - 0.01
        while get_h_by_pt(p=p_min, t=t) < h:
            p_min = p_min - 0.01
    # 真实的压力值位于p_min和p_max之间，二分法求解
    p_ave = (p_min + p_max) / 2
    h0 = get_h_by_pt(p=p_ave, t=t)
    while abs(h0 - h) > 0.000000001 and p_max - p_min > 0.000000001:
        if h0 > h:
            p_min = p_ave
        else:
            p_max = p_ave
        p_ave = (p_min + p_max) / 2
        h0 = get_h_by_pt(p=p_ave, t=t)

    return p_ave


def get_rho_by_pt(p, t) -> float:
    """
    返回介质的密度，单位为kg/m3
    """
    h2o = water(p, t)
    try:
        return h2o.rho
    except AttributeError:
        logger.error(f"焓值计算错误，计算参数：{p=}MPa, {t=}℃")
        traceback.print_exc()


def get_h_by_pt(p, t):
    """
    根据p和t求h

    :param p: 压力，单位为 MPa
    :param t: 温度，单位为 ℃
    :return: 焓，单位为 kJ/kg
    """
    h2o = water(p, t)
    try:
        return h2o.h
    except AttributeError:
        logger.error(f"焓值计算错误，计算参数：{p=}MPa, {t=}℃")
        traceback.print_exc()


def get_s_by_pt(p, t):
    """
    根据p和t求熵

    :param p: 压力，单位为 MPa
    :param t: 温度，单位为 ℃
    :return: 焓，单位为 kJ/kg
    """
    h2o = water(p, t)
    return h2o.s


def get_t_by_hp(h, p):
    """
    根据h和p求t

    :param h: 焓，单位为 kJ/kg
    :param p: 压力，单位为 MPa
    :return: 温度，单位为 ℃
    """
    h2o = water(h=h, p=p)
    return h2o.T - 273.15


def get_t_by_ph(p, h):
    """
    根据h和p求t

    :param h: 焓，单位为 kJ/kg
    :param p: 压力，单位为 MPa
    :return: 温度，单位为 ℃
    """
    h2o = water(h=h, p=p)
    return h2o.T - 273.15


def get_h_by_px(p, x):
    """
    根据p和x求h，x=0为饱和水，x=1为饱和蒸汽

    :param p: 压力，单位为 MPa
    :param x: 蒸汽干度
    :return: 焓，单位为 kJ/kg
    """
    h2o = water(p=p, x=x)
    return h2o.h


def get_h_by_tx(t, x):
    """
    根据t和x求h，x=0为饱和水，x=1为饱和蒸汽

    :param t: 温度，单位为℃
    :param x: 蒸汽干度
    :return: 焓，单位为 kJ/kg
    """
    h2o = water(t=t, x=x)
    return h2o.h


def get_t_by_p(p):
    """
    根据压力求对应的饱和温度

    :param p: MPa
    :return:
    """
    return iapws.iapws97._TSat_P(p) - 273.15


def get_p_by_t(t):
    """
        根据温度求对应的饱和压力

        :param t: ℃
        :return:
        """
    return iapws.iapws97._PSat_T(t + 273.15)


def validate_water_parameters(p=None, t=None, h=None, exclude=None):
    """
    验证给定的参数是否可以唯一确定水及水蒸气状态。返回True或False表示参数是否合理，msg表示错误原因

    :param p:
    :param t:
    :param h:
    :param exclude: 排除某种类型的错误，all：排除过定义，less:排除欠定义
    :return:
    """
    res, msg = True, "ok"
    if (p is None and t is None) or (p is None and h is None) or (t is None and h is None):
        if exclude == "less":
            res, msg = True, "ok"
        else:
            res, msg = False, "焓值欠定义"
    elif p is None and t is None and h is None:
        res, msg = False, "焓值欠定义"
    return res, msg


H_PT = get_h_by_pt
S_PT = get_s_by_pt
P_T = get_p_by_t
T_P = get_t_by_p
P_TH = get_p_by_th

if __name__ == "__main__":
    # print(f"{H_PT(10, 500)=}")
    # print(f"{S_PT(10, 500)=}")
    # print(f"{T_P(1)=}")
    # print(f"{P_T(200)=}")
    # print(f"{P_TH(500, 3300)=}")
    # for t in range(100, 360, 10):
    #     for p in [8, 9]:
    #         water = IAPWS97(P=p, T=t + 273.15)
    #         print(str(water.w) + ",", end="")
    #     print("")
    # water = IAPWS97(H=763.9, T=117.4 + 273.15)
    # print(str(water.P) + ",", end="")
    print(P_TH(177.4, 763.9))