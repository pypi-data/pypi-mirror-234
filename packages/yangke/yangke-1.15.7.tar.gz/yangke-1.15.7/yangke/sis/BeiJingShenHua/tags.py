from enum import Enum, unique
from yangke.base import get_key_value, is_number
from yangke.common.config import logger


@unique
@get_key_value
class TagsRead(Enum):
    热网加热器疏水流量1 = "10lcp40cf101"
    热网加热器疏水流量2 = "10lcp80cf101"
    主汽门前压力 = "13lba40cp101"
    主汽门前温度 = "13lba40ct601"
    高压蒸汽流量1号炉 = "11lba90cf101-sel"
    高压蒸汽流量2号炉 = "12lba90cf101-sel"
    高压蒸汽减温水流量1号炉 = "11lae90cf101-comp"
    高压蒸汽减温水流量2号炉 = "12lae90cf101-comp"
    高排压力 = "13lbc01cp101"
    高排温度 = "13lbc01ct601"
    中压主汽门前压力 = "13lbb40cp101"
    中压主汽门前温度 = "13lbb40ct601"
    中压给水流量1号炉 = "ldyh.11lab80cf101-comp"
    中压给水流量2号炉 = "ldyh.12lab80cf101-comp"
    FGH流量1号炉 = "gtc_11rcaome60410"
    FGH流量2号炉 = "gtc_12rcaome60410"
    再热减温水流量1 = "11laf80cf101-comp"  # 11laf80cf101-comp
    再热减温水流量2 = "12laf80cf101"
    低压蒸汽流量1 = "11lba70cf101-sel"
    低压蒸汽流量2 = "12lba70cf101-sel"
    低压蒸汽压力1 = "11lba60cp111-sel"
    低压蒸汽压力2 = "12lba60cp111-sel"
    低压蒸汽温度1 = "11lba60ct601"
    低压蒸汽温度2 = "12lba60ct601"
    供热热量 = "ldyh.rwjl1-17"
    热井出水压力 = "ldyh.13lca11cp101"
    热井出水温度 = "ldyh.13lca11ct601"
    凝结水流量1号炉 = "11lca51cf101-comp"
    凝结水流量2号炉 = "12lca51cf101-comp"
    燃机功率1 = "ldyh.gtc_11rcaogd00201"
    燃机功率2 = "ldyh.gtc_12rcaogd00201"
    发电机有功功率_steam = "13mka00ce011"
    全厂总功率 = "10cear214_03"
    大气压力 = "ldyh.gtc_11rcaogc00702"
    环境温度 = "gtc_11mbl01ct101"
    环境湿度 = "ldyh.gtc_11mbl01cm101"
    当前背压 = "10mag10cp101-sel"
    当前循泵运行方式 = "NPPC_Way_CirPump_cur"
    当前风机运行方式 = "NPPC_Way_CoolFan_cur"

    凝汽器循环水进水温度1 = "13mag01ct303"
    凝汽器循环水进水温度2 = "13mag01ct305"

    烟气热网加热器进水流量 = "10gck60cf101-cal"
    烟气热网加热器进水压力 = "10nda16cp111"
    烟气热网加热器进水温度1 = "11nda51ct311"
    烟气热网加热器供水温度1 = "11nda51ct312"
    烟气热网加热器进水温度2 = "12nda51ct311"
    烟气热网加热器供水温度2 = "12nda51ct312"

    计量单元天然气流量1 = "bdjl4"
    计量单元天然气流量2 = "bdjl204"
    计量单元天然气流量3 = "bdjl404"

    风机1电流 = "10pag11an001xq01"
    风机2电流 = "10pag11an002xq01"
    风机3电流 = "10pag11an003xq01"
    风机4电流 = "10pag11an004xq01"
    风机5电流 = "10pag11an005xq01"
    风机6电流 = "10pag11an006xq01"
    风机7电流 = "10pag11an007xq01"
    风机8电流 = "10pag11an008xq01"

    大泵1电流 = "ldyh.10pac11ap001xq01"
    大泵2电流 = "ldyh.10pac12ap001xq01"
    小高速3电流 = "ldyh.10pac13ap001xq01"
    小高速4电流 = "ldyh.10pac14ap001xq01"
    小低速3电流 = "ldyh.10pac13ap001xq02"
    小低速4电流 = "ldyh.10pac14ap001xq02"


@unique
@get_key_value
class TagsWrite(Enum):
    建议循泵运行方式 = "NPPC_P_NUM_OPT"
    建议风机运行方式 = "NPPC_FAN_NUM_OPT"
    最优运行方式下背压 = "NPPC_P_Best_Con"
    优化后机组节煤量 = "NPPC_Coal_Saving_Run"


PumpType = {
    # 字符表示的循泵运行方式对应的数字表示的运行方式，三位数字表示法格式为：百位为大泵数量，十位为高速泵数量，个位为低速泵数量
    # A:2大1小(高速)    B:2大             C:1大2小(高速)  D:1大1小(高速)
    # E:2小(高速)       F:2小(1高1低)     G:1大          H:1小(高速)          I:1小(低速)
    # O:2大2小(高速)
    "A": "210",
    "B": "200",
    "C": "120",
    "D": "110",
    "E": "020",
    "F": "011",
    "G": "100",
    "H": "010",
    "I": "001",
    "X": "000",
    "O": "220",  # 历史数据中存在的工况
    "P": "101",  # 历史数据中存在的工况
    "Q": "021",  # 历史数据中存在的工况，按理来说该工况不应该存在
    "R": "002",  # 历史数据中存在的工况，两台低速泵
    "S": "111",
}

availableType = {
    # 当前运行方式对应的其他可选的运行方式
    # 实际上，随着凝汽器热负荷增加，泵和风机的运行台数是基本同步变大变小的，也就不存在风机全开而泵开的很少或泵全开而风机开的很少的情况，
    # 因此，A3、H7、H8这种理论上的运行方式现实中不存在，而A4的组合方式不常见，因为泵太大，风机太少不协调，尽量不选用A4
    # 王家东：存在G7运行方式，但比较少
    "A3": ["A3", "A4", "B3", "B4", "B5", "C4", "C5", "C6"],  # 实际上不可能存在A3的运行方式
    "A4": ["A4", "A5", "B4", "B5", "B6", "C5", "C6", "C7"],
    "A5": ["A4", "A5", "A6", "B5", "B6", "B7", "C6", "C7", "C8"],
    "A6": ["A5", "A6", "A7", "B6", "B7", "B8", "C7", "C8"],
    "A7": ["A6", "A7", "A8", "B7", "B8", "C7", "C8"],
    "A8": ["A8", "B8", "C8"],
    "B3": ["B3", "B4", "C3", "C4"],
    "B4": ["B3", "B4", "B5", "B6", "C4", "C5", "C6"],
    "B5": ["B4", "B5", "B6", "B7", "C5", "C6", "C7"],  # A4的组合方式不常见，因为泵太大，风机太少不协调，尽量不选用A4
    "B6": ["A5", "A6", "B5", "B6", "B7", "C6", "C7", "C8"],
    "B7": ["A6", "A7", "B6", "B7", "B8", "C7", "C8"],
    "B8": ["A7", "A8", "B7", "B8", "C8"],
    "C3": ["B3", "C2", "C3", "C4", "D3", "D4", "D5"],
    "C4": ["B3", "B4", "C3", "C4", "C5", "D4", "D5", "D6"],
    "C5": ["B4", "B5", "C4", "C5", "C6", "D5", "D6", "D7"],
    "C6": ["B4", "B5", "B6", "C5", "C6", "C7", "D6", "D7", "D8"],
    "C7": ["B5", "B6", "B7", "C6", "C7", "C8", "D7", "D8"],
    "C8": ["B6", "B7", "B8", "C7", "C8", "D8"],
    "D3": ["D3", "D4", "E3", "E4", "E5"],
    "D4": ["C4", "D3", "D4", "D5", "E4", "E5", "E6"],
    "D5": ["C4", "C5", "D4", "D5", "D6", "E5", "E6", "E7"],
    "D6": ["C4", "C5", "C6", "D5", "D6", "D7", "E6", "E7", "E8"],
    "D7": ["C5", "C6", "C7", "D6", "D7", "D8", "E7", "E8"],
    "D8": ["C6", "C7", "C8", "D7", "D8", "E8"],
    "E3": ["D3", "E3", "E4", "F3", "F4"],
    "E4": ["D3", "D4", "E3", "E4", "E5", ],
    "E5": ["D3", "D4", "D5", "E4", "E5", "E6", "F5", "F6", "F7"],
    "E6": ["D4", "D5", "D6", "E5", "E6", "E7", "F6", "F7", "F8"],
    "E7": ["D5", "D6", "D7", "E6", "E7", "E8", "F7", "F8"],
    "E8": ["D6", "D7", "D8", "E7", "E8", "F8"],
    "F1": ["F2", ],
    "F2": ["F3", ],
    "F3": ["E3", "E4", "F3", "F4", "G3", "G4", "G5"],
    "F4": ["E3", "E4", "F3", "F4", "F5", "G4", "G5", "G6"],
    "F5": ["E3", "E4", "E5", "F4", "F5", "F6", "G5", "G6", "G7"],
    "F6": ["E4", "E5", "E6", "F5", "F6", "F7", "G6", "G7"],
    "F7": ["E5", "E6", "E7", "F6", "F7", "F8", "G7"],
    "F8": ["E6", "E7", "E8", "F7", "F8"],
    "G0": ["G1"],
    "G1": ["G2"],
    "G2": ["G3"],
    "G3": ["G3", "G4", "F3", "H4", "H3"],
    "G4": ["G3", "G4", "G5", "F3", "F4", "H4", "H3"],
    "G5": ["G4", "G5", "G6", "F3", "F4", "F5"],
    "G6": ["G5", "G6", "G7", "F4", "F5", "F6"],
    "G7": ["G6", "G7", "F6", "F7", "F8"],
    "G8": ["G7", "G8", "F5", "F6", "F7", "F8"],
    "H0": ["H1", "H2", "I1", "I2"],
    "H1": ["H1", "H2", "H3", "I1", "I2"],
    "H2": ["H2", "H3", "I2", "I3", ],
    "H3": ["H3", "H4", "G3"],
    "H4": ["H4", "H5", "H3", "G3"],
    "H5": ["H4", "H5", "H6", "G3"],
    "H6": ["H5", "H6", "G3", "G4"],
    "H7": ["H6", "H7", "G3", "G4", "G5"],
    "H8": ["H6", "H7", "H8", "G3", "G4", "G5"],
    "I0": ["I1", "I2", "I0"],
    "I1": ["I0", "I1", "I2", "I3"],
    "I2": ["I1", "I2", "I3"],
    "I3": ["I2", "I3", "I4", "H2", "H3"],
    "I4": ["I3", "I4", "H2", "H3"],  # 稀有工况
    "I5": ["I4", "I5", "H3", "H4"],  # 稀有工况
    "I6": ["I5", "I6", "H3", "H4", "H5"],  # 极稀有工况
    "I7": ["I6", "I7", "H4", "H5", "H6"],  # 极稀有工况
    "I8": ["I6", "I7", "I8", "H5", "H6", "H7"]  # 极稀有工况
}

rare_type = ["A0", "A1", "A2", "A3", "A4", "A5",
             "B0", "B1", "B2", "B3", "B4",
             "C0", "C1", "C2", "C3", "C4",
             "D0", "D1", "D2", "D3",
             "F3",
             "H7", "H8",
             "I6", "I7", "I8"
             ]  # 稀有工况，即实际上几乎不可能运行的工况，如风机很大，泵很小或风机很小泵很大

power_cold = {
    "A": 5989.7,
    "B": 5174.7,
    "C": 4303.5,
    "D": 3450.5,
    "E": 2762.6,
    "F": 2040.5,
    "G": 1904.0,
    "H": 1500,  # 836.7,  # 1500
    "I": 836.7,
    "0": 0,
    "1": 670 / 3,
    "2": 670 / 3 * 2,
    "3": 670.7,
    "4": 890.8,
    "5": 1115.8,
    "6": 1324.7,
    "7": 1525.1,
    "8": 1730.1
}
for 循泵方式 in ["A", "B", "C", "D", "E", "F", "G", "H"]:
    for 风机数量 in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        state = f"{循泵方式}{风机数量}"
        power_cold.update({state: power_cold[循泵方式] + power_cold[str(风机数量)]})


def get_available_type(cur_state, child_opt=None):
    if child_opt is None:
        return availableType[cur_state]
    elif child_opt in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
        res = []
        for t in availableType[cur_state]:
            if t.startswith(child_opt):
                res.append(t)
        return res


def get_pump_type_by_int(t: str):
    """
    将循泵运行方式的数字表示法转换为字符表示法
    """
    revert_pump_type = {v: k for (k, v) in PumpType.items()}
    if is_number(t):
        t = str(int(t))
        if len(t) == 1:
            t = f"00{t}"
        elif len(t) == 2:
            t = f"0{t}"
    else:
        logger.warning(f"循泵运行方式{t}无法转换为字符表示")
        return 'A'
    return revert_pump_type[t]


def get_less_cold(t: str):
    """
    获取比指定运行方式冷端耗功更低的工况，且尽量剔除稀有工况
    """
    avail = availableType.get(t)
    cur_cold = power_cold[t]
    avail_cold = []
    for _t in avail:
        if power_cold[_t] < cur_cold:
            avail_cold.append(_t)
    res_v = 0
    res_t = t
    res_t1 = t
    for _t in avail_cold:
        if power_cold[_t] > res_v:
            res_v = power_cold[_t]
            res_t = _t
            if _t not in rare_type:
                res_t1 = power_cold[_t]
    if res_t == t:
        res_t = res_t1
    return res_t


def get_larger_cold(t: str):
    """
    获取比指定运行方式冷端耗功更大的工况，且尽量剔除稀有工况
    """
    avail = availableType.get(t)
    cur_cold = power_cold[t]
    avail_cold = []
    for _t in avail:
        if power_cold[_t] > cur_cold:
            avail_cold.append(_t)
    res_v = 10000
    res_t = t
    res_t1 = t
    for _t in avail_cold:
        if power_cold[_t] < res_v:
            res_v = power_cold[_t]
            res_t = _t
            if _t not in rare_type:
                res_t1 = power_cold[_t]
    if res_t == t:
        res_t = res_t1
    return res_t


def get_pump_type_by_char(t: str):
    res = PumpType.get(t)
    if res is not None:
        return res
    else:
        logger.warning(f"循泵运行方式{t}无法转换为数值表示")
        return '000'
