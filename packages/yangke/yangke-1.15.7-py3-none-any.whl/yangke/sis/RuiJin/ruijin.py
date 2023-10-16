import math
from functools import partial

from yangke.common.config import logger
from yangke.sis.RuiJin.tags import TagsRead, TagsWrite, TagsReadDCS
from yangke.sis.cold_optimize_base import Condenser
from yangke.sis.dll_file import init_write_sis, init_dbp_api, read_data, get_tag_value, ColdResult, 标煤热值, \
    read_data_from_dcs
from yangke.base import execute_function_by_interval
from yangke.performance.iapws97 import get_h_by_px, get_h_by_pt, get_h_by_tx, get_t_by_ph, get_p_by_t, get_t_by_p

available_type = [(2, 2, 2), (2, 1, 2), (2, 2, 0), (0, 2, 2), (2, 0, 2), (2, 1, 0), (0, 1, 2)]
cold_result = ColdResult()
condenser = Condenser()

condenser.set_info(类型='双背压', 设计凝汽器热负荷=494.68 + 490.692, 有效长度=14, 管子外径=25, 管子壁厚=0.5,
                   t_cyc_in=22.3, bp=4.75, 有效换热面积=64000, 洁净度=0.85,
                   循环水体积流量=101000, 设计循环水流速=2.131
                   )


def get_power_cold(on_a3, on_b3, on_c3):
    """
    计算循环水泵耗功

    AC开，则功率为2000+2100=4100kW 4200
    ABC开，则功率为2200+2350+2250=6800

    :param on_a3:
    :param on_b3:
    :param on_c3:
    :return:
    """
    res = 0
    if on_a3 == 2 and on_b3 == 2 and on_c3 == 2:  # 三高
        res = 6800
    elif on_a3 == 2 and on_b3 == 2 and on_c3 == 0:  # 两高
        res = 4200
    elif on_a3 == 0 and on_b3 == 2 and on_c3 == 2:  # 两高
        res = 4200
    elif on_a3 == 2 and on_b3 == 0 and on_c3 == 2:  # 两高
        res = 4200  # ...  # 4100，B泵高速耗功比A、C泵高
    elif on_a3 == 2 and on_b3 == 1 and on_c3 == 2:  # 两高一低
        res = 2200 + 1650 + 2200
    elif on_a3 == 2 and on_b3 == 1 and on_c3 == 0:  # 一高一低
        res = 2200 + 1600
    elif on_a3 == 0 and on_b3 == 1 and on_c3 == 2:  # 一高一低
        res = 2200 + 1600
    return res


def get_flow(on_a3, on_b3, on_c3):
    """
    获取每种循泵运行方式下的循环水流量

    :param on_a3:
    :param on_b3:
    :param on_c3:
    :return:
    """
    flow_cycle = 0
    if on_a3 == 2 and on_b3 == 2 and on_c3 == 2:  # 三高
        flow_cycle = 101051
    elif on_a3 == 2 and on_b3 == 2 and on_c3 == 0:  # 两高
        flow_cycle = 79478
    elif on_a3 == 0 and on_b3 == 2 and on_c3 == 2:  # 两高
        flow_cycle = 79478
    elif on_a3 == 2 and on_b3 == 0 and on_c3 == 2:  # 两高
        flow_cycle = 79478
    elif on_a3 == 2 and on_b3 == 1 and on_c3 == 2:  # 两高一低
        flow_cycle = 93764
    elif on_a3 == 2 and on_b3 == 1 and on_c3 == 0:  # 一高一低
        flow_cycle = 69246  # AB低：69246，
    elif on_a3 == 0 and on_b3 == 1 and on_c3 == 2:  # 一高一低
        flow_cycle = 69246
    return flow_cycle


def get_power_by_bp(bp, bp_iter, power):
    """
    获取背压变化后，机组的功率，使用设计的背压曲线

    :param bp:
    :param bp_iter:
    :param power:
    :return:
    """
    x = bp
    percent = 0.005457 * x ** 4 - 0.166231 * x ** 3 + 1.893091 * x ** 2 - 8.552442 * x + 12.976042
    percent = 1 - percent / 100
    x = bp_iter
    percent_iter = 0.005457 * x ** 4 - 0.166231 * x ** 3 + 1.893091 * x ** 2 - 8.552442 * x + 12.976042
    percent_iter = 1 - percent_iter / 100
    power_init = power / percent
    power_iter = power_init * percent_iter
    return power_iter


def get_coal_by_bp(bp, bp_iter, coal):
    """
    获取背压变化后，机组的热耗或煤耗，使用设计的背压曲线，煤耗和热耗的变化率是相同的，因此可以使用同一条曲线

    :param
    bp:
    :param
    bp_iter:
    :param
    power:
    :return:
    """
    x = bp
    percent = -0.005199 * x ** 4 + 0.160356 * x ** 3 - 1.840626 * x ** 2 + 8.346903 * x - 12.678426
    percent = 1 - percent / 100
    x = bp_iter
    percent_iter = -0.005199 * x ** 4 + 0.160356 * x ** 3 - 1.840626 * x ** 2 + 8.346903 * x - 12.678426
    percent_iter = 1 - percent_iter / 100
    coal_init = coal / percent
    coal_iter = coal_init * percent_iter
    return coal_iter


def output_res(dis_res):
    """
    返回计算结果至前端画面

    :param dis_res:
    :return:
    """
    pass


def optimize_coal(snapshot, group_num=3):
    """
    以煤耗为目标对循环水泵运行方式进行优化；优化假设条件：1、优化前后凝汽器运行补水流量不变；

    :param snapshot:
    :param group_num: 机组编号
    :return:
    """
    opt_result = {}
    get_value = partial(get_tag_value, snapshot)
    if group_num == 3:
        power = get_value(TagsRead.power3, 903.28)
        t_env = get_value(TagsRead.环境温度, 14.55)
        f_condense = get_value(TagsRead.凝泵出口凝结水流量3, 1555.46)
        f_makeup = get_value(TagsRead.凝汽器运行补水流量3, 20.13)
        bp1 = get_value(TagsRead.bph_a_3, 4.33)  # 高压凝汽器压力
        bp2 = get_value(TagsRead.bph_b_3, 4.33)  # 高压凝汽器压力
        bp3 = get_value(TagsRead.bph_c_3, 4.33)  # 高压凝汽器压力
        bp4 = get_value(TagsRead.bpl_a_3, 4.33)  # 低压凝汽器压力
        bp5 = get_value(TagsRead.bpl_b_3, 4.33)  # 低压凝汽器压力
        bp6 = get_value(TagsRead.bpl_c_3, 4.33)  # 低压凝汽器压力
        t_well = get_value(TagsRead.热井出水温度3, 30.88)  # 按出水温度计算焓
        t_makeup = get_value(TagsRead.凝汽器补水温度3, 30.92)
        t_cyc_cold1_3 = get_value(TagsRead.凝汽器1进口A循环水温度1_3, 15.75)
        t_cyc_cold2_3 = get_value(TagsRead.凝汽器1进口A循环水温度2_3, 15.91)
        t_cyc_cold3_3 = get_value(TagsRead.凝汽器1进口B循环水温度1_3, 15.85)
        t_cyc_cold4_3 = get_value(TagsRead.凝汽器1进口B循环水温度2_3, 15.74)
        t_cyc_hot1 = get_value(TagsRead.凝汽器2出口A循环水温度1_3, 27.38)
        t_cyc_hot2 = get_value(TagsRead.凝汽器2出口A循环水温度2_3, 27.42)
        t_cyc_hot3 = get_value(TagsRead.凝汽器2出口B循环水温度1_3, 27.69)
        t_cyc_hot4 = get_value(TagsRead.凝汽器2出口B循环水温度2_3, 27.54)
    else:
        power = get_value(TagsRead.power4, 903.28)
        t_env = get_value(TagsRead.环境温度, 14.55)
        f_condense = get_value(TagsRead.凝泵出口凝结水流量4, 1555.46)
        f_makeup = get_value(TagsRead.凝汽器运行补水流量4, 20.13)
        bp1 = get_value(TagsRead.bph_a_4, 4.33)  # 高压凝汽器压力
        bp2 = get_value(TagsRead.bph_b_4, 4.33)  # 高压凝汽器压力
        bp3 = get_value(TagsRead.bph_c_4, 4.33)  # 高压凝汽器压力
        bp4 = get_value(TagsRead.bpl_a_4, 4.33)  # 低压凝汽器压力
        bp5 = get_value(TagsRead.bpl_b_4, 4.33)  # 低压凝汽器压力
        bp6 = get_value(TagsRead.bpl_c_4, 4.33)  # 低压凝汽器压力
        t_well = get_value(TagsRead.热井出水温度4, 30.88)  # 按出水温度计算焓
        t_makeup = get_value(TagsRead.凝汽器补水温度4, 30.92)
        t_cyc_cold1_3 = get_value(TagsRead.凝汽器1进口A循环水温度1_4, 15.75)
        t_cyc_cold2_3 = get_value(TagsRead.凝汽器1进口A循环水温度2_4, 15.91)
        t_cyc_cold3_3 = get_value(TagsRead.凝汽器1进口B循环水温度1_4, 15.85)
        t_cyc_cold4_3 = get_value(TagsRead.凝汽器1进口B循环水温度2_4, 15.74)
        t_cyc_hot1 = get_value(TagsRead.凝汽器2出口A循环水温度1_4, 27.38)
        t_cyc_hot2 = get_value(TagsRead.凝汽器2出口A循环水温度2_4, 27.42)
        t_cyc_hot3 = get_value(TagsRead.凝汽器2出口B循环水温度1_4, 27.69)
        t_cyc_hot4 = get_value(TagsRead.凝汽器2出口B循环水温度2_4, 27.54)

    if power < 10:  # 停机状态
        opt_result.update({"3": "stop"})
    else:
        f_out_lp = f_condense - f_makeup  # 0.7583 * f_condense3 + 32.22  # 低压缸排汽流量
        heat_dispatch = 3484097.04 * power + 333917622.65  # 近似认为凝汽器排汽能量只与功率相关

        bp = (bp1 + bp2 + bp3 + bp4 + bp5 + bp6) / 6
        del bp1, bp2, bp3, bp4, bp5, bp6
        # h_well3 = get_h_by_px(bp / 1000, 0)  # 凝汽器压力对应的饱和水的焓
        h_well = get_h_by_tx(t_well, 0)
        h_makeup = get_h_by_pt(2.28, t_makeup)

        # MJ/h = 3.6 * kW
        heat_load = heat_dispatch / 1000 - f_out_lp * h_well - f_makeup * h_makeup  # 热负荷=排汽能量-凝结水能量-补水
        heat_load_kW = heat_load / 3.6  # kW
        del t_makeup, h_makeup, f_makeup

        t_cyc_cold = (t_cyc_cold1_3 + t_cyc_cold2_3 + t_cyc_cold3_3 + t_cyc_cold4_3) / 4
        t_cyc_hot = (t_cyc_hot1 + t_cyc_hot2 + t_cyc_hot3 + t_cyc_hot4) / 4
        del t_cyc_cold1_3, t_cyc_cold2_3, t_cyc_cold3_3, t_cyc_cold4_3, t_cyc_hot1, t_cyc_hot2, t_cyc_hot3, t_cyc_hot4
        h_cyc_cold = get_h_by_pt(0.3, t_cyc_cold)
        h_cyc_hot = get_h_by_pt(0.24, t_cyc_hot)

        t_sat_bp = get_t_by_p(bp / 1000)  # 凝汽器压力对应的饱和温度
        凝汽器端差 = t_sat_bp - t_cyc_hot
        凝汽器过冷度 = t_sat_bp - t_well
        热井出水温度与循环水进水温度差 = t_well - t_cyc_cold
        delta_t_cyc = t_cyc_hot - t_cyc_cold  # 循环水温升
        delta_h_cyc = h_cyc_hot - h_cyc_cold  # 循环水焓升
        环境温度与冷却塔出水温度差 = t_cyc_cold - t_env
        实际循环水流量 = heat_load / (h_cyc_hot - h_cyc_cold)

        rpm_a3 = get_value(TagsRead.循泵A转速3, 372.85)
        rpm_b3 = get_value(TagsRead.循泵B转速3, 330.6)
        rpm_c3 = get_value(TagsRead.循泵C转速3, 0)
        on_a3 = 2 if rpm_a3 > 350 else 0
        on_b3 = 1 if rpm_b3 > 300 else 0
        on_b3 = 2 if rpm_b3 > 350 else on_b3
        on_c3 = 2 if rpm_c3 > 350 else 0
        del rpm_a3, rpm_b3, rpm_c3

        power_cold = get_power_cold(on_a3, on_b3, on_c3)  # 当前运行方式下的功率
        flow_cycle = get_flow(on_a3, on_b3, on_c3)

        coal_rate_roll10 = get_value(TagsRead.入炉煤量)  # t/h，取10min的平均值
        power_roll10 = get_value(TagsRead.power3)
        if power_roll10 <= 100:
            logger.debug(f"机组处于停机或启动状态，无法计算煤耗")
            当前煤耗 = 0
        else:
            当前煤耗 = 1000 * coal_rate_roll10 / power_roll10

        # 调试
        当前煤耗 = 287  # g/kWh
        coal_exclude_pump = 当前煤耗 * power / (power - power_cold / 1000)  # 扣除冷端耗功后的发电煤耗

        price_coal = get_value(TagsRead.price_coal, 1200)
        price_power = get_value(TagsRead.price_power, 0.5)
        benefit = coal_exclude_pump / 1000 / 1000 * price_coal * (power - power_cold) * 1000  # g/kWh->t/kWh->元/kWh->元/h

        cond_list = []
        for a, b, c in available_type:
            if (a, b, c) == (on_a3, on_b3, on_c3) or (c, b, a) == (on_a3, on_b3, on_c3):
                flow_cycle_iter = 实际循环水流量
            else:
                flow_cycle_iter = get_flow(a, b, c)

            power_cold_iter = get_power_cold(a, b, c)

            # ---------------------------- 计算当前运行方式下的背压 ------------------------------------
            # 认为循环水流量增大对凝汽器和冷却塔换热性能的影响是相同的
            delta_h_iter = heat_load / flow_cycle_iter
            h_cyc_cold_iter = h_cyc_cold + (delta_h_cyc - delta_h_iter) * 1.5 / 3
            h_cyc_hot_iter = h_cyc_cold_iter + delta_h_iter
            t_cyc_cold_iter = get_t_by_ph(0.3, h_cyc_cold_iter)  # 当前运行方式下循环水冷侧温度
            t_cyc_hot_iter = get_t_by_ph(0.24, h_cyc_hot_iter)
            t_sat_bp_iter = t_sat_bp + (t_cyc_hot_iter - t_cyc_hot)  # 认为循环水温度变化=热井水温度变化=凝汽器饱和温度变化

            bp_iter = get_p_by_t(t_sat_bp_iter) * 1000  # kPa
            # ---------------------------- 计算当前运行方式下的背压 ------------------------------------

            # ---------------------------- 计算背压变化导致的功率变化 -----------------------------------
            delta_bp_iter = bp_iter - bp
            power_iter = get_power_by_bp(bp, bp_iter, power)
            coal_iter = get_coal_by_bp(bp, bp_iter, 当前煤耗)  # 当前迭代步的十分钟平均煤耗
            coal_exclude_pump_iter = coal_iter * power_iter / (power_iter - power_cold_iter / 1000)  # 扣除冷端耗功后的煤耗
            delta_power_gen = (power_iter - power) * 1000  # kW,发电机多发的电量
            delta_power_cold = power_cold_iter - power_cold  # kW，循泵多耗的电量
            delta_power_net = delta_power_gen - delta_power_cold  # 净功率变化
            benefit_iter = coal_exclude_pump_iter / 1000 * price_coal * (power_iter - power_cold_iter)  # 元/h

            cond_list.append({"循泵运行方式": [a, b, c],
                              "净功率": power_iter - power_cold_iter / 1000,
                              "净功率增加": delta_power_net,
                              "发电机功率": power_iter,
                              "发电机功率增加": delta_power_gen,
                              "冷端耗功": power_cold_iter,
                              "冷端耗功增加": delta_power_cold,
                              "煤耗": coal_exclude_pump_iter,
                              "煤耗降低": coal_exclude_pump - coal_exclude_pump_iter,
                              "背压": bp_iter,
                              "发电收益": benefit_iter,
                              })
            # ---------------------------- 计算背压变化导致的功率变化 -----------------------------------

        obj = get_tag_value(snapshot, TagsRead.优化目标, 0)  # 0表示煤耗，1表示收益
        if obj == 0:
            cond_list.sort(key=lambda x: x["净功率增加"])
        else:
            cond_list.sort(key=lambda x: x["发电收益"])

        # 写出优化结果
        res = cond_list[0]
        if group_num == 3:
            dis_res = {
                TagsWrite.循泵A启停3: res["循泵运行方式"][0],
                TagsWrite.循泵B启停3: res["循泵运行方式"][1],
                TagsWrite.循泵C启停3: res["循泵运行方式"][2],
                TagsWrite.凝汽器热负荷3: heat_load,
                TagsWrite.凝汽器端差3: 凝汽器端差,
                TagsWrite.凝汽器过冷度3: 凝汽器过冷度,
                TagsWrite.循环水流量3: 实际循环水流量,
                TagsWrite.冷端耗功3: power_cold,
                TagsWrite.冷端耗功优化值3: res["冷端耗功"],
                TagsWrite.发电功率优化值3: res["发电机功率"],
                TagsWrite.净功率3: power - power_cold / 1000,
                TagsWrite.净功率优化值3: res["净功率"],
                TagsWrite.煤耗3: coal_exclude_pump,  # 扣除冷端耗功的发电煤耗
                TagsWrite.煤耗优化值3: res["煤耗"],
                TagsWrite.发电收益3: benefit,
                TagsWrite.发电收益优化值3: res["发电收益"],
            }
        else:
            dis_res = {
                TagsWrite.循泵A启停4: res["循泵运行方式"][0],
                TagsWrite.循泵B启停4: res["循泵运行方式"][1],
                TagsWrite.循泵C启停4: res["循泵运行方式"][2],
                TagsWrite.凝汽器热负荷4: heat_load,
                TagsWrite.凝汽器端差4: 凝汽器端差,
                TagsWrite.凝汽器过冷度4: 凝汽器过冷度,
                TagsWrite.循环水流量4: 实际循环水流量,
                TagsWrite.冷端耗功4: power_cold,
                TagsWrite.冷端耗功优化值4: res["冷端耗功"],
                TagsWrite.发电功率优化值4: res["发电机功率"],
                TagsWrite.净功率4: power - power_cold / 1000,
                TagsWrite.净功率优化值4: res["净功率"],
                TagsWrite.煤耗4: coal_exclude_pump,  # 扣除冷端耗功的发电煤耗
                TagsWrite.煤耗优化值4: res["煤耗"],
                TagsWrite.发电收益4: benefit,
                TagsWrite.发电收益优化值4: res["发电收益"],
            }

        db_res = {"环境温度": t_env, "凝汽器热负荷": heat_load, "循泵运行方式": res["循泵运行方式"],
                  "循环水冷侧温度": t_cyc_cold}
        output_res(dis_res)


def optimize():
    snapshot = read_data(TagsRead, ip="172.18.240.191", port='12084', user="admin", password="admin")  # 未知原因读不到数据
    snapshot = read_data_from_dcs(TagsReadDCS, url='http://172.18.248.80:8080/nodiot/restful/redisValue')
    optimize_coal(snapshot, 3)
    optimize_coal(snapshot, 4)


init_write_sis(ip="172.18.240.191", port='12084', user="admin", passwd_str="admin")
execute_function_by_interval(optimize, minute=0, second=10)
