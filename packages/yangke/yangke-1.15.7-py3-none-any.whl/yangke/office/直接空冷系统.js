function 汽水状态(T, Ts) {

    if (T > Ts + 15)
        return "过热蒸汽"
    else if (T > Ts)
        return "微过热蒸汽"
    else
        return "湿蒸汽"
}

function 进口温差(凝汽器进汽温度, 进口空气温度) {
    return 凝汽器进汽温度 - 进口空气温度;
}

function 对数平均温差(进口空气温度, 出口空气温度, 凝汽器进汽温度) {
    let a = 出口空气温度 - 进口空气温度;
    let b = (凝汽器进汽温度 - 进口空气温度) / (凝汽器进汽温度 - 出口空气温度);
    let c = Math.log(b);
    let d = Math.log(Math.E);
    return a / (c / d);
}

function 对数平均温差2(散热量, 传热系数, 换热面积) {
    // 散热量单位：MW
    let a = 散热量 * 1000000;
    return a / 传热系数 / 换热面积;
}


function 传热系数(凝汽器热流量, 换热面积, 对数平均温差) {
    return 凝汽器热流量 / (换热面积 * 对数平均温差);
}

function 性能特性(进口空气温度, 出口空气温度, 凝汽器进汽温度) {
    let a = 进口温差(凝汽器进汽温度, 进口空气温度);
    return (出口空气温度 - 进口空气温度) / a;
}

function 传热单元数(进口空气温度, 出口空气温度, 凝汽器进汽温度) {
    return (出口空气温度 - 进口空气温度) / 对数平均温差(进口空气温度, 出口空气温度, 凝汽器进汽温度);
}

function 辅助值(设计传热单元数) {
    let a = 设计传热单元数;
    return a / (Math.exp(a) - 1);
}


function 修正系数1(排汽干度, 排汽干度设计值) {
    return 排汽干度 / 排汽干度设计值;
}

function 修正系数2(大气压力, 大气压力设计值, 辅助值, m_k_optional) {
    // 大气压力修正系数
    let a = 大气压力 / 大气压力设计值;
    let b = a * (1 - 辅助值);
    if (m_k_optional == undefined) {
        m_k_optional = 0.45;
    }
    let c = 辅助值 * Math.pow(a, m_k_optional);
    let d = 1 / (b + c);
    return d;
}

function 修正系数3(风机频率, 风机频率设计值, 辅助值, n_opt, mk_opt) {
    // 风机频率修正系数
    if (n_opt == undefined) {
        n_opt = 0.33;
    }
    if (mk_opt == undefined) {
        mk_opt = 0.45;
    }
    let a = 风机频率 / 风机频率设计值;
    let b = Math.pow(a, -3 / (3 - n_opt));
    let c = 1 - 辅助值;
    let d = Math.pow(a, (3 * mk_opt - 3) / (3 - n_opt));
    let e = c + 辅助值 * d;
    return b / e;
}

function 修正系数4(修正热负荷, 设计凝结热, 设计排汽流量) {
    // 排汽压力和进口空气温度修正
    // 修正热负荷，kW 是根据空冷系统性能图标查出来的，如果性能图标是排气流量的修正，则无需使用该函数
    // 设计凝结热 = 排汽焓 - 凝结水焓，单位kJ/kg
    let 修正到设计工况的排汽流量 = 修正热负荷 / 设计凝结热;
    return 设计排汽流量 / 修正到设计工况的排汽流量;
}

function 修正系数1不确定度() {
    return 0;
}

function 修正系数2不确定度(大气压力, 大气压力设计值, 辅助值, 大气压力不确定度, m_k_optional) {
    // 大气压力：kPa
    if (m_k_optional == undefined) {
        m_k_optional = 0.45;
    }
    let max = 修正系数2(大气压力 + 大气压力不确定度, 大气压力设计值, 辅助值, m_k_optional);
    let min = 修正系数2(大气压力 - 大气压力不确定度, 大气压力设计值, 辅助值, m_k_optional);
    return Math.abs(max - min) / 2;
}

function 修正系数3不确定度(风机频率, 风机频率不确定度, 风机频率设计值, 辅助值, n_opt, mk_opt) {
    if (n_opt == undefined) {
        n_opt = 0.33;
    }
    if (mk_opt == undefined) {
        mk_opt = 0.45;
    }
    let max = 修正系数3(风机频率 + 风机频率不确定度, 风机频率设计值, 辅助值, n_opt, mk_opt)
    let min = 修正系数3(风机频率 - 风机频率不确定度, 风机频率设计值, 辅助值, n_opt, mk_opt)
    return Math.abs(max - min) / 2;
}

function 修正后风机驱动功率不确定度(大气压力, 大气压力设计值, 进口空气温度,
                       进口空气温度设计值, 风机频率, 风机频率设计值, 风机功率不确定度, n_opt) {
    // 大气压力：kPa，本函数使用《DLT 244-2012》规程中示例算例中的不确定度计算方法，不考虑大气压力，温度，频率等不确定度带来的影响
    if (n_opt == undefined) {
        n_opt = 0.33;
    }
    return 修正后风机功率(风机功率不确定度, 大气压力, 大气压力设计值, 进口空气温度, 进口空气温度设计值, 风机频率, 风机频率设计值, n_opt);
}

function 修正后风机驱动功率不确定度2(大气压力, 大气压力不确定度, 大气压力设计值, 进口空气温度, 进口空气温度不确定度,
                        进口空气温度设计值, 风机频率, 风机频率不确定度, 风机频率设计值, 风机功率, 风机功率不确定度, n_opt) {
    // 大气压力：kPa，本函数考虑风机功率修正方程中所有参数的不确定度带来的影响
    if (n_opt == undefined) {
        n_opt = 0.33;
    }
    let max_p = 大气压力 + 大气压力不确定度;
    let min_p = 大气压力 - 大气压力不确定度;
    let max_t = 进口空气温度 + 进口空气温度不确定度;
    let min_t = 进口空气温度 - 进口空气温度不确定度;
    let max_f = 风机频率 + 风机频率不确定度;
    let min_f = 风机频率 - 风机频率不确定度;
    let max_power = 风机功率 + 风机功率不确定度;
    let min_power = 风机功率 - 风机功率不确定度;
    let max = 修正后风机功率(max_power, min_p, 大气压力设计值, max_t, 进口空气温度设计值, min_f, 风机频率设计值, n_opt);
    let min = 修正后风机功率(min_power, max_p, 大气压力设计值, min_t, 进口空气温度设计值, max_f, 风机频率设计值, n_opt);
    return Math.abs(max - min) / 2;
}

function 修正后风机功率(风机功率, 大气压力, 大气压力设计值, 进口空气温度, 进口空气温度设计值, 风机频率, 风机频率设计值, n_opt) {
    // 大气压力：kPa
    if (n_opt == undefined) {
        n_opt = 0.33;
    }
    let a = 大气压力设计值 / 大气压力;
    let b = (273.15 + 进口空气温度) / (273.15 + 进口空气温度设计值);
    let c = a * b;
    let d = Math.pow(c, 1 - n_opt);
    let e = Math.pow(风机频率设计值 / 风机频率, 3);
    return d * e * 风机功率;
}

function 修正后排汽流量不确定度(修正系数1, 修正系数2, 修正系数3, 修正系数4, Delta修正系数1, Delta修正系数2, Delta修正系数3, Delta修正系数4, 排汽流量, 排汽流量不确定度) {
    // 排汽流量单位：t/h
    修正系数1 = 修正系数1 + 0;  // 将变量转为数值类型，传入的变量直接无法输出，但是可以正常计算
    let q = 排汽流量 / 3.6;
    let dq = 排汽流量不确定度 / 3.6;
    let a = 修正系数1 * 修正系数2 * 修正系数3 * 修正系数4;
    let b = q * 修正系数2 * 修正系数3 * 修正系数4;
    let c = 修正系数1 * q * 修正系数3 * 修正系数4;
    let d = 修正系数1 * 修正系数2 * q * 修正系数4;
    let e = 修正系数1 * 修正系数2 * 修正系数3 * q;
    let a1 = (a * dq) * (a * dq);
    let b1 = Math.pow((b * Delta修正系数1), 2);
    let c1 = Math.pow((c * Delta修正系数2), 2);
    let d1 = Math.pow((d * Delta修正系数3), 2);
    let e1 = Math.pow((e * Delta修正系数4), 2);
    /*return e;*/
    return Math.sqrt(a1 + b1 + c1 + d1 + e1) * 3.6;
}

function 排汽压力比较值(修正后排汽流量, 排汽流量设计值, 排汽压力设计值, 进口空气温度设计值, 出口空气温度设计值, 对数平均温差设计值, 凝汽器进口压力设计值_opt) {
    // 流量单位t/h
    let theta_2 = 出口空气温度设计值;
    let theta_1 = 进口空气温度设计值;
    let NTU_G = (theta_2 - theta_1) / 对数平均温差设计值;
    let phi_g = 1 - Math.exp(-NTU_G);
    let theta_D = theta_1 + (theta_2 - theta_1) / phi_g;
    let index = 23.308417 - 3888.11 / (theta_D + 229.95);
    let p_D = Math.exp(index) / 1000;  // 计算的凝汽器进口压力，该值进行了大量假设，会引入误差
    if (凝汽器进口压力设计值_opt != undefined) {
        // 如果直接给定了凝汽器进口压力设计值，则直接使用该值，避免假设条件引入的偏差
        p_D = 凝汽器进口压力设计值_opt;
    }
    let omega = 排汽压力设计值 / p_D;
    let numerator = Math.pow(theta_D + 229.95, 2);
    let denominator = 3888.11 * (theta_D - theta_1);
    let chi = numerator / denominator;
    let temp1 = omega * omega + 2 * omega - 1;
    let temp2 = 排汽流量设计值 / 修正后排汽流量;
    let temp3 = temp2 - 1 + chi;
    let part1 = omega / temp1 * temp3 / chi;
    let part2 = Math.sqrt(Math.pow(part1, 2) - temp2 * temp2 * (1 - omega * omega) / temp1);
    return (part1 + part2) * 排汽压力设计值;
}

function 基本传热系数K0_胡洪华(凝汽器管子内径_mm, 管内平均流速_m_s) {
    // 参考胡洪华《大型机组凝汽器性能的试验和修正方法》
    let d = 凝汽器管子内径_mm;
    let v = 管内平均流速_m_s;
    let c1;
    if (d >= 16 && d <= 19) {
        c1 = 2747;
    } else if (d >= 22 && d <= 25) {
        c1 = 2705;
    } else if (d >= 28 && d <= 32) {
        c1 = 2664;
    } else if (d >= 35 && d <= 38) {
        c1 = 2623;
    } else if (d >= 41 && d <= 45) {
        c1 = 2582;
    } else if (d >= 48 && d <= 51) {
        c1 = 2541;
    }
    return c1 * Math.sqrt(v);
}

function 凝汽器管子内平均流速(循环水流量_m3_h, 管子外径_mm, 管子壁厚_mm, 管子数量) {
    let f = 循环水流量_m3_h / 3600;
    let d = (管子外径_mm - 2 * 管子壁厚_mm) / 1000;
    let area = Math.PI * d * d / 4 * 管子数量;
    return f / area;
}

