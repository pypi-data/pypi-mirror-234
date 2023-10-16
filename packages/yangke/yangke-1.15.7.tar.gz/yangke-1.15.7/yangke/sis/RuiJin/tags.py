from enum import Enum, unique
from yangke.base import get_key_value, is_number
from yangke.common.config import logger

from enum import Enum, unique
from yangke.base import get_key_value, is_number
from yangke.common.config import logger


@unique
@get_key_value
class TagsRead(Enum):
    # 优化目标 = "obj"  # 0表示煤耗，1表示收益
    # price_coal = "DCS.PRICE_COAL"  # 元/t
    # price_power = "DCS.PRICE_POWER"  # 元/kWh

    power3 = "N3DCS.MW"
    power4 = "N4DCS.MW"
    # bpl_a_3 = "N3DCS.30MAG10CP101"  # 低压凝汽器背压a
    # bpl_b_3 = "N3DCS.30MAG10CP102"  # 低压凝汽器背压b
    # bpl_c_3 = "N3DCS.30MAG10CP103"  # 低压凝汽器背压c
    # bph_a_3 = "N3DCS.30MAG20CP101"  # 高压凝汽器背压a
    # bph_b_3 = "N3DCS.30MAG20CP102"  # 高压凝汽器背压b
    # bph_c_3 = "N3DCS.30MAG20CP103"  # 高压凝汽器背压c
    #
    # bpl_a_4 = "N4DCS.40MAG10CP101"  # 低压凝汽器背压a
    # bpl_b_4 = "N4DCS.40MAG10CP102"  # 低压凝汽器背压b
    # bpl_c_4 = "N4DCS.40MAG10CP103"  # 低压凝汽器背压c
    # bph_a_4 = "N4DCS.40MAG20CP101"  # 高压凝汽器背压a
    # bph_b_4 = "N4DCS.40MAG20CP102"  # 高压凝汽器背压b
    # bph_c_4 = "N4DCS.40MAG20CP103"  # 高压凝汽器背压c
    #
    # 凝泵出口凝结水流量3 = "N3DCS.CNDFLW2"  #
    # 凝泵出口凝结水流量4 = "N4DCS.CNDFLW2"
    # 热井出水温度3 = "N3DCS.30LCA11CT101"
    # 热井出水温度4 = "N4DCS.40LCA11CT101"
    # 凝汽器运行补水流量3 = "N3DCS.30LCP10CF102_C"
    # 凝汽器补水温度3 = "N3DCS.30LCA20CT101"  # 压力取2.28MPa
    # 凝汽器运行补水流量4 = "N4DCS.40LCP10CF102_C"  # 98.25
    # 凝汽器补水温度4 = "N4DCS.40LCA20CT101"  # 24.68
    #
    # 大气压力 = "N3DCS.30HLA00CP101"  # 3号炉风烟系统画面
    # 环境温度 = "N3DCS.30HLA00CT101"  # 3号炉风烟系统画面
    # 环境湿度 = "ldyh.gtc_11mbl01cm101"
    #
    # 凝汽器1进口A循环水温度1_3 = "N3DCS.30PAB10CT101"  # 凝汽器1为低压凝汽器，循环水先进入低压凝汽器在进入高压凝汽器
    # 凝汽器1进口A循环水温度2_3 = "N3DCS.30PAB10CT102"
    # 凝汽器1进口B循环水温度1_3 = "N3DCS.30PAB20CT101"
    # 凝汽器1进口B循环水温度2_3 = "N3DCS.30PAB20CT102"
    #
    # 凝汽器2出口A循环水温度1_3 = "N3DCS.30PAB10CT103"  # 凝汽器2为高压凝汽器
    # 凝汽器2出口A循环水温度2_3 = "N3DCS.30PAB10CT104"
    # 凝汽器2出口B循环水温度1_3 = "N3DCS.30PAB20CT103"
    # 凝汽器2出口B循环水温度2_3 = "N3DCS.30PAB20CT104"
    #
    # 凝汽器1进口A循环水温度1_4 = "N4DCS.40PAB10CT101"
    # 凝汽器1进口A循环水温度2_4 = "N4DCS.40PAB10CT102"
    # 凝汽器1进口B循环水温度1_4 = "N4DCS.40PAB20CT101"
    # 凝汽器1进口B循环水温度2_4 = "N4DCS.40PAB20CT102"
    #
    # 凝汽器2出口A循环水温度1_4 = "N4DCS.30PAB10CT103"
    # 凝汽器2出口A循环水温度2_4 = "N4DCS.30PAB10CT104"
    # 凝汽器2出口B循环水温度1_4 = "N4DCS.30PAB20CT103"
    # 凝汽器2出口B循环水温度2_4 = "N4DCS.30PAB20CT104"
    #
    # 循泵A电流3 = "N3DCS.30PAC01AP001XQ01"
    # 循泵B电流3 = "N3DCS.30PAC01AP002XQ01"
    # 循泵C电流3 = "N3DCS.30PAC01AP003XQ01"
    # 循泵A电流4 = "N4DCS.40PAC01AP001XQ01"
    # 循泵B电流4 = "N4DCS.40PAC01AP002XQ01"
    # 循泵C电流4 = "N4DCS.40PAC01AP003XQ01"
    #
    # 循泵A转速3 = "N3DCS.30PAC01CS111"  # 典型转速372
    # 循泵B转速3 = "N3DCS.30PAC01CS112"  # 高速：转速>350:电流>150;典型转速372；低速:典型转速330
    # 循泵C转速3 = "N3DCS.30PAC01CS113"
    # 循泵A转速4 = "N4DCS.40PAC01CS111"
    # 循泵B转速4 = "N4DCS.40PAC01CS112"
    # 循泵C转速4 = "N4DCS.40PAC01CS113"

    # 入炉煤量 = ""


@unique
@get_key_value
class TagsReadDCS(Enum):
    # 优化目标 = "obj"  # 0表示煤耗，1表示收益
    # price_coal = "DCS.PRICE_COAL"  # 元/t
    # price_power = "DCS.PRICE_POWER"  # 元/kWh

    power3 = "CF159F30MKA01CE001"
    power4 = "CF159FD40XKA01CE903_XQ01"  # CF159FD40CBA25CBA25R101
    bpl_a_3 = "CF159FCNSRVCM"  # 低压凝汽器背压a
    # bpl_b_3 = "N3DCS.30MAG10CP102"  # 低压凝汽器背压b
    # bpl_c_3 = "N3DCS.30MAG10CP103"  # 低压凝汽器背压c
    # bph_a_3 = "N3DCS.30MAG20CP101"  # 高压凝汽器背压a
    # bph_b_3 = "N3DCS.30MAG20CP102"  # 高压凝汽器背压b
    # bph_c_3 = "N3DCS.30MAG20CP103"  # 高压凝汽器背压c
    #
    # bpl_a_4 = "N4DCS.40MAG10CP101"  # 低压凝汽器背压a
    # bpl_b_4 = "N4DCS.40MAG10CP102"  # 低压凝汽器背压b
    # bpl_c_4 = "N4DCS.40MAG10CP103"  # 低压凝汽器背压c
    # bph_a_4 = "N4DCS.40MAG20CP101"  # 高压凝汽器背压a
    # bph_b_4 = "N4DCS.40MAG20CP102"  # 高压凝汽器背压b
    # bph_c_4 = "N4DCS.40MAG20CP103"  # 高压凝汽器背压c
    #
    # 凝泵出口凝结水流量3 = "N3DCS.CNDFLW2"  #
    # 凝泵出口凝结水流量4 = "N4DCS.CNDFLW2"
    # 热井出水温度3 = "N3DCS.30LCA11CT101"
    # 热井出水温度4 = "N4DCS.40LCA11CT101"
    # 凝汽器运行补水流量3 = "N3DCS.30LCP10CF102_C"
    # 凝汽器补水温度3 = "N3DCS.30LCA20CT101"  # 压力取2.28MPa
    # 凝汽器运行补水流量4 = "N4DCS.40LCP10CF102_C"  # 98.25
    # 凝汽器补水温度4 = "N4DCS.40LCA20CT101"  # 24.68
    #
    # 大气压力 = "N3DCS.30HLA00CP101"  # 3号炉风烟系统画面
    # 环境温度 = "N3DCS.30HLA00CT101"  # 3号炉风烟系统画面
    # 环境湿度 = "ldyh.gtc_11mbl01cm101"
    #
    # 凝汽器1进口A循环水温度1_3 = "N3DCS.30PAB10CT101"  # 凝汽器1为低压凝汽器，循环水先进入低压凝汽器在进入高压凝汽器
    # 凝汽器1进口A循环水温度2_3 = "N3DCS.30PAB10CT102"
    # 凝汽器1进口B循环水温度1_3 = "N3DCS.30PAB20CT101"
    # 凝汽器1进口B循环水温度2_3 = "N3DCS.30PAB20CT102"
    #
    # 凝汽器2出口A循环水温度1_3 = "N3DCS.30PAB10CT103"  # 凝汽器2为高压凝汽器
    # 凝汽器2出口A循环水温度2_3 = "N3DCS.30PAB10CT104"
    # 凝汽器2出口B循环水温度1_3 = "N3DCS.30PAB20CT103"
    # 凝汽器2出口B循环水温度2_3 = "N3DCS.30PAB20CT104"
    #
    # 凝汽器1进口A循环水温度1_4 = "N4DCS.40PAB10CT101"
    # 凝汽器1进口A循环水温度2_4 = "N4DCS.40PAB10CT102"
    # 凝汽器1进口B循环水温度1_4 = "N4DCS.40PAB20CT101"
    # 凝汽器1进口B循环水温度2_4 = "N4DCS.40PAB20CT102"
    #
    # 凝汽器2出口A循环水温度1_4 = "N4DCS.30PAB10CT103"
    # 凝汽器2出口A循环水温度2_4 = "N4DCS.30PAB10CT104"
    # 凝汽器2出口B循环水温度1_4 = "N4DCS.30PAB20CT103"
    # 凝汽器2出口B循环水温度2_4 = "N4DCS.30PAB20CT104"
    #
    # 循泵A电流3 = "N3DCS.30PAC01AP001XQ01"
    # 循泵B电流3 = "N3DCS.30PAC01AP002XQ01"
    # 循泵C电流3 = "N3DCS.30PAC01AP003XQ01"
    # 循泵A电流4 = "N4DCS.40PAC01AP001XQ01"
    # 循泵B电流4 = "N4DCS.40PAC01AP002XQ01"
    # 循泵C电流4 = "N4DCS.40PAC01AP003XQ01"
    #
    # 循泵A转速3 = "N3DCS.30PAC01CS111"  # 典型转速372
    # 循泵B转速3 = "N3DCS.30PAC01CS112"  # 高速：转速>350:电流>150;典型转速372；低速:典型转速330
    # 循泵C转速3 = "N3DCS.30PAC01CS113"
    # 循泵A转速4 = "N4DCS.40PAC01CS111"
    # 循泵B转速4 = "N4DCS.40PAC01CS112"
    # 循泵C转速4 = "N4DCS.40PAC01CS113"

    # 入炉煤量 = ""


@unique
@get_key_value
class TagsWrite(Enum):
    循泵A启停3 = "N3DCS.PUMP_A_OPT_3"
    循泵B启停3 = "N3DCS.PUMP_B_OPT_3"
    循泵C启停3 = "N3DCS.PUMP_C_OPT_3"
    循泵A启停4 = "N4DCS.PUMP_A_OPT_4"
    循泵B启停4 = "N4DCS.PUMP_B_OPT_4"
    循泵C启停4 = "N4DCS.PUMP_C_OPT_4"

    凝汽器热负荷3 = "N3DCS.HEAT_LOAD_COND_3"
    凝汽器热负荷4 = "N3DCS.HEAT_LOAD_COND_4"
    凝汽器端差3 = 'N3DCS.DC_CONDENSER_3'
    凝汽器端差4 = 'N3DCS.DC_CONDENSER_4'
    凝汽器过冷度3 = 'N3DCS.SUPERCOOL_CONDENSER_3'
    凝汽器过冷度4 = 'N3DCS.SUPERCOOL_CONDENSER_4'
    循环水流量3 = 'N3DCS.FLOW_CYC_3'
    循环水流量4 = 'N3DCS.FLOW_CYC_4'

    冷端耗功3 = 'N3DCS.POWER_COLD_3'
    冷端耗功优化值3 = 'N3DCS.POWER_COLD_OPT_3'
    发电功率优化值3 = 'N3DCS.POWER_OPT_3'
    净功率3 = 'N3DCS.POWER_NET_3'
    净功率优化值3 = 'N3DCS.POWER_NET_OPT_3'
    煤耗3 = 'N3DCS.COAL_CON_3'
    煤耗优化值3 = 'N3DCS.COAL_CON_OPT_3'
    发电收益3 = 'N3DCS.BENEFIT_GEN_3'
    发电收益优化值3 = 'N3DCS.BENEFIT_GEN_OPT_3'

    冷端耗功4 = 'N3DCS.POWER_COLD_4'
    冷端耗功优化值4 = 'N3DCS.POWER_COLD_OPT_4'
    发电功率优化值4 = 'N3DCS.POWER_OPT_4'
    净功率4 = 'N3DCS.POWER_NET_4'
    净功率优化值4 = 'N3DCS.POWER_NET_OPT_4'
    煤耗4 = 'N3DCS.COAL_CON_4'
    煤耗优化值4 = 'N3DCS.COAL_CON_OPT_4'
    发电收益4 = 'N3DCS.BENEFIT_GEN_4'
    发电收益优化值4 = 'N3DCS.BENEFIT_GEN_OPT_4'
