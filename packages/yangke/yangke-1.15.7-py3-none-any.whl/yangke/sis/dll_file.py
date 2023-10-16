# -*- coding: utf-8 -*-
import ctypes
import math
import os.path
import time
from datetime import datetime, timedelta
from enum import Enum, EnumMeta
from typing import Optional
import numpy as np
import pandas as pd

from yangke.base import merge_two_dataframes, get_settings
from yangke.common.config import logger
from yangke.core import runCMD, str_in_list

标煤热值 = 29307.6  # kJ/kg


def ctypes_str2char_array(string: str):
    """
    python3中的字符串是以utf-8格式编码的，为了将字符串传递给C函数，需要将其解码为byte类型，对应C函数中的char*类型或char[]类型

    :param string:
    :return:
    """
    return string.encode("utf8")


def init_write_sis(ip=None, user=None, passwd_str=None, port=None):
    """
    使用dbp_api.write_snapshot_by_cmd()方法时需要先调用该方法设置相关SIS操作脚本的路径

    :return:
    """
    import sys
    import yangke.common.fileOperate as fo
    path = sys.executable
    write_sis_bat = os.path.join(os.path.dirname(__file__), "write_sis.bat")
    write_sis_py = os.path.join(os.path.dirname(__file__), "write_sis.py")
    temp_write_sis_bat = os.path.join(os.path.dirname(__file__), "temp_write_sis.bat")
    temp_write_sis_py = os.path.join(os.path.dirname(__file__), "temp_write_sis.py")
    lines = fo.read_lines(write_sis_bat)
    lines_new = []
    for line in lines:
        line = line.replace("%python_exec%", path)
        line = line.replace("%py_file%", os.path.abspath(temp_write_sis_py))
        lines_new.append(line)
    fo.write_lines(temp_write_sis_bat, lines_new)
    if ip is not None and user is not None and passwd_str is not None and port is not None:
        lines = fo.read_lines(write_sis_py)
        lines_new = []
        for line in lines:
            line = line.replace('@ip@', ip)
            line = line.replace('@user@', user)
            line = line.replace('@passwd@', passwd_str)
            line = line.replace('@port@', str(port))
            lines_new.append(line)

        fo.write_lines(temp_write_sis_py, lines_new)


def init_dbp_api(settings=None, ip=None, port=None, user=None, password=None):
    """
    初始化RDBP代理服务器连接，以settings中的配置为优先，如果需要覆盖代理配置，则可以手动传入settings={}

    :param settings:
    :param ip:
    :param port:
    :param user:
    :param password:
    :return:
    """
    from yangke.common.config import logger

    if settings is None:
        settings = get_settings()
    _ip = settings.get_settings("sis.ip")
    _ip = None if _ip == {} else _ip
    _port = settings.get_settings("sis.port")
    _port = None if _port == {} else _port
    _user = settings.get_settings("sis.user")
    _user = None if _user == {} else _user
    _password = settings.get_settings("sis.password")
    _password = None if _password == {} else _user

    ip = _ip if _ip is not None else ip
    port = _port if _port is not None else port
    user = _user if _user is not None else user
    password = _password if _password is not None else password

    try:
        dbp_api = DllMode(ip, user, password, port)
        return dbp_api
    except:
        logger.warning("RDB代理服务器连接失败")
        return None


def read_data_from_dcs(tag_des_read, url):
    """
    使用控制公司开放API读取数据
    访问地址：http://172.18.248.80:8080/nodiot/restful/redisValue


    :return:
    """
    import requests
    if not isinstance(tag_des_read, dict):
        描述 = tag_des_read.get_keys()
        标签 = tag_des_read.get_values()
        data = {
            "tagList": "CF159FD40MAG20FP002_XH54"
        }
        x = requests.post(url, data=data)
    return x


def read_data(tag_des_read, need_detail=False, ip=None, port=None, user=None, password=None):
    """
    读取标签数据，返回以描述为表头的dataframe对象，从settings.yaml中加载代理服务器信息

    当tag_des_read为字典时示例如下：
    tag_heat_supply_read = {"N1DCS.TOTALMW": "#1电功率", "N2DCS.TOTALMW": "#2电功率", "N3DCS.TOTALMW": "#3电功率"}
    snapshot = read_data(tag_des_read)

    当tag_des_read为Enum对象时示例如下：
    from enum import Enum, unique
    from yangke.base import get_key_value
    @unique
    @get_key_value
    class tag_des_read(Enum):
        电功率1 = "N1DCS.TOTALMW"
        电功率2 = "N2DCS.TOTALMW"
        电功率3 = "N3DCS.TOTALMW"

    snapshot = read_data(tag_des_read)

    :param password:
    :param user:
    :param port:
    :param ip:
    :param tag_des_read: {tag1: des1, tag2: des2}类型的数据，或@get_key_value修饰的Enum对象
    :param need_detail:
    :return:
    """
    dbp_api = init_dbp_api(ip=ip, port=port, user=user, password=password)
    if dbp_api is not None:
        if not isinstance(tag_des_read, dict):
            tags = tag_des_read.get_values()
            des = tag_des_read.get_keys()
            snapshot = dbp_api.get_snapshot(tags=tags, tag_description=des, need_detail=need_detail)
        else:
            snapshot = dbp_api.get_snapshot(tags=list(tag_des_read.values()),
                                            tag_description=list(tag_des_read.keys()),
                                            need_detail=need_detail)
    else:
        logger.warning("RDBP服务器连接失败")
        snapshot = {}
    return snapshot


class DllMode:
    def __init__(self, ip=None, user=None, passwd_str=None, port=None, dll_file=None):
        self.ip = ip
        self.user = user
        self.passwd = passwd_str
        self.port = port
        if dll_file is None:
            path = os.path.join(os.path.dirname(__file__), "resource/dbpapi_x64.dll")
        else:
            path = dll_file
        try:
            self.handle: Optional[ctypes.c_uint64] = None
            self.dll = ctypes.cdll.LoadLibrary(path)
        except OSError:
            logger.warning(f"找不到指定的动态链接库！请检查路径{path}")
            raise OSError(f"找不到指定的动态链接库！请检查路径{path}")
        if ip is not None and user is not None and passwd_str is not None and port is not None:
            self.connect(ip, user, passwd_str, port)
        else:
            logger.debug(f"RDBProxy连接信息不全！")

    def __del__(self):
        self.close()

    def connect(self, ip, user, passwd_str, port):
        self.dll.DBPCreate2.restype = ctypes.c_uint64
        ip = ctypes_str2char_array(ip)
        user = ctypes_str2char_array(user)
        passwd = ctypes_str2char_array(passwd_str)
        port = int(port)
        self.handle = ctypes.c_uint64(self.dll.DBPCreate2(ip, user, passwd, port, 0))
        if self.handle is None:
            print("连接创建失败")
            return False
        ret = self.dll.DBP_Connect(self.handle)
        if 0 == ret:
            return True
        else:
            print("服务器连接失败")
            return False

    def close(self):
        if self.handle is not None and self.handle.value > 0:
            self.dll.DBP_Close(self.handle)
            self.handle = None

    def is_connect(self):
        ret = self.dll.DBP_IsConnect(self.handle)
        if 0 == ret:
            return True
        return False

    def dis_connect(self):
        """
        断开连接

        :return:
        """
        ret = self.dll.DBP_DisConnect(self.handle)
        if 0 == ret:
            return True
        return False

    def get_his_value(self, tags: list or str, tags_description=None, start_time: datetime = None,
                      end_time: datetime = None,
                      time_interval=10, use_description=True):
        """
        待验证

        :param tags:
        :param tags_description: 参考get_snapshot中的同名参数
        :param start_time: datetime.datetime类型，默认为两小时前的时间
        :param end_time: datetime.datetime类型，默认为当前时间
        :param time_interval: 时间间隔，单位s
        :param use_description: 参考get_snapshot中的同名参数
        :return:
        """
        now = datetime.now()
        start_time = start_time or now - timedelta(days=0, hours=2)  # 默认两小时前的时间为读数起始时间
        end_time = end_time or now - timedelta(days=0, hours=0)  # 默认一小时前的时间为读数结束时间
        start_time_long = int(time.mktime(start_time.timetuple()))  # 将时间转为UNIX时间
        end_time_long = int(time.mktime(end_time.timetuple()))
        start_time_c = ctypes.c_long(start_time_long)  # c_long和c_ulong貌似都可以
        end_time_c = ctypes.c_long(end_time_long)
        insert_time = ctypes.c_long(time_interval)  # 插值时间，只有下方flag为1是才有效
        flag = ctypes.c_long(1)  # 标记，为0时取样本值，插值时间参数无效，为1时使插值时间参数生效
        # 预留的点数，如果读取的时间段内点数超过这个数，结果会被裁剪，如果读取的点数少于这个数，会补零
        data_num = math.ceil((end_time_long - start_time_long) / time_interval)
        a = ctypes.c_int(10)
        b = ctypes.c_int(10)
        value_type = ctypes.pointer(a)  # 指针和数组在python传递时有所区别
        data_size_actual = ctypes.pointer(b)  # 返回实际读到的数据个数
        value_double_arr = (ctypes.c_double * data_num)()
        value2_arr = (ctypes.c_long * data_num)()
        time_long_arr = (ctypes.c_long * data_num)()
        qas_short_arr = (ctypes.c_short * data_num)()
        if isinstance(tags, str):  # 读取单个参数的历史数据，tags为数据库标签名
            tag_name = ctypes_str2char_array(tags)  # 名字
            self.dll.DBPGetHisVal(self.handle, tag_name, start_time_c, end_time_c, insert_time, flag,
                                  value_double_arr, value2_arr, time_long_arr, qas_short_arr,
                                  ctypes.c_int(data_num), value_type, data_size_actual)
            return self._assemble_dataframe(tags, time_long_arr, qas_short_arr, value_double_arr, value2_arr,
                                            value_type, None, False)
        else:  # 读取多个数据的历史数据，tags为数据库标签名组成的列表
            df = None
            if tags_description is not None and use_description:
                kks_des = dict(zip(tags, tags_description))
            else:
                kks_des = dict(zip(tags, tags))
            for tag in tags:
                tag_name = kks_des.get(tag)
                tag_c = ctypes_str2char_array(tag)
                self.dll.DBPGetHisVal(self.handle, tag_c, start_time_c, end_time_c, insert_time, flag,
                                      value_double_arr, value2_arr, time_long_arr, qas_short_arr,
                                      ctypes.c_int(data_num), value_type, data_size_actual)
                _ = self._assemble_dataframe(tag_name, time_long_arr, qas_short_arr, value_double_arr, value2_arr,
                                             value_type, None, False)
                if df is None:
                    df = _
                else:
                    df = merge_two_dataframes(df, _)[0]
            return df

    def get_snapshot(self, tags, tag_description=None, need_detail=False, use_description=True):
        """
        获取给定标签列表的快照数据

        :param tags: 标签名
        :param need_detail:是否需要数据的详细信息，默认不需要，如果为True,则会返回数据质量、错误码等详细信息
        :param tag_description: 标签点的描述
        :param use_description: 当给定点描述时，数据列的标题是否使用点描述代替标签名
        :return:
        """

        n_size = len(tags)
        tag_names = (ctypes.c_char_p * n_size)()  # 名字
        for i in range(n_size):
            tag_names[i] = ctypes_str2char_array(tags[i])

        time_long_arr = (ctypes.c_uint32 * n_size)()  # 时间，系统里的时间应该比当前时间早8小时

        qas_short_arr = (ctypes.c_short * n_size)()  # 质量

        value_double_arr = (ctypes.c_double * n_size)()  # 浮点数类型的值
        value2_arr = (ctypes.c_int32 * n_size)()  # 整形类型的值
        value2_type = (ctypes.c_int32 * n_size)()  # 数据类型
        error_code_arr = (ctypes.c_short * n_size)()  # 数据错误码
        self.dll.DBPGetSnapshot(
            self.handle,  # 句柄
            tag_names,  # char* sTagNames[],  //in,标签名字符串指针数组  //apistring
            time_long_arr,  # long ltimes[],   //in, 时标
            qas_short_arr,  # short snqas[],   //in, 质量
            value_double_arr,  # double  dblvals[],   //in, 存放double值,DT_FLOAT32,DT_FLOAT64存放区
            value2_arr,  # long lvals[],   //in, 存放Long值,DT_DIGITAL,DT_INT32,DT_INT64存放区
            value2_type,  # int  ntypes[],   //in, 数据类型,DT_INT32,DT_FLOAT32等。
            error_code_arr,  # short errs[],    //in/out, 错误码
            n_size  # int  nsize    //in, 个数
        )
        if tag_description is not None and use_description:  # 如果使用描述，且描述不为空
            return self._assemble_dataframe(tag_description, time_long_arr,
                                            qas_short_arr, value_double_arr, value2_arr,
                                            value2_type,
                                            error_code_arr, need_detail=need_detail)
        else:
            return self._assemble_dataframe(tags, time_long_arr, qas_short_arr,
                                            value_double_arr, value2_arr,
                                            value2_type,
                                            error_code_arr, need_detail=need_detail)

    @staticmethod
    def _assemble_dataframe(tags, time_long_arr, qas_short_arr, value_double_arr, value2_arr, value2_type,
                            error_code_arr, need_detail=False):
        """
        将代理服务器返回的数据组装成dataframe格式的对象

        :param tags: 数据标签
        :param time_long_arr:
        :param qas_short_arr:
        :param value_double_arr:
        :param value2_arr:
        :param value2_type:
        :param error_code_arr:
        :param need_detail: 是否需要数据的详细信息，默认不需要，如果为True,则会返回数据质量、错误码等详细信息
        :return:
        """
        n_size = len(time_long_arr)  # 标签个数
        if not need_detail:
            columns = ["DateTime"]
            if isinstance(tags, str):  # 说明是读历史数据，只有一个变量标签，但有多个时间标签
                columns = ["DateTime", tags]
                data_list = []
                for i in range(n_size):
                    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time_long_arr[i]))
                    if value2_type[0] == 3:
                        data_list.append([time_str, value_double_arr[i]])
                    else:
                        data_list.append([time_str, value2_arr[i]])
                result = pd.DataFrame(columns=columns, data=data_list)
            else:
                columns.extend(tags)
                time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time_long_arr[0]))
                data_list = [time_str]
                for i in range(n_size):
                    if value2_type[i] == 3:  # 如果数据类型==3，则说明读到的是double类型数据
                        data_list.append(value_double_arr[i])
                    else:
                        data_list.append(value2_arr[i])
                result = pd.DataFrame(columns=columns, data=[data_list])
        else:
            result = {}
            for i in range(n_size):
                if isinstance(tags, str):
                    ...
                else:
                    tag = tags[i]
                    columns = ["DateTime", "值", "质量", "数据类型", "错误码"]
                    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time_long_arr[i]))
                    qas = qas_short_arr[i]
                    value_type = value2_type[i]
                    if value_type == 3:
                        value = value_double_arr[i]
                    else:
                        value = value2_arr[i]
                    error_code = error_code_arr[i]
                    data_list = [time_str, value, qas, value_type, error_code]
                    dataframe = pd.DataFrame(columns=columns, data=[data_list])
                    result.update({tag: dataframe})
        return result

    def write_snapshot_by_cmd(self, tags, values):
        """
        该方法功能和self.write_snapshot_double()完全相同，但是将写入操作重启一个进程进行，这样写入操作报错时，不会影响主程序崩溃。
        如果出现“Python已停止工作”错误，请检查RDBProxy代理和数据库中是否存在相关的测点。

        :param tags:
        :param values:
        :return:
        """
        from yangke.common.config import logger

        for k in tags:
            if k is None:
                logger.error("标签列表中存在空标签，请检查测点名")
                logger.error("写入SIS失败！")
                return None
        tags_values = {k: v for k, v in zip(tags, values)}
        path = os.path.join(os.path.dirname(__file__), "temp_write_sis.bat")
        if not os.path.exists(path):
            if self.ip is not None and self.user is not None and self.passwd is not None and self.port is not None:
                init_write_sis(ip=self.ip, user=self.user, passwd_str=self.passwd, port=self.port)
            else:
                settings = get_settings()  # 说明没有初始化写SIS脚本文件，这里初始化一下
                _ip = settings.get_settings("sis.ip")
                _port = settings.get_settings("sis.port")
                _user = settings.get_settings("sis.user")
                _password = settings.get_settings("sis.password")
                if _ip is not None and _port is not None and _user is not None and _password is not None:
                    init_write_sis(ip=_ip, user=_user, passwd_str=_password, port=_port)
                else:
                    logger.error("请先初始化写快照脚本，init_write_sis(ip, user, port, passwd)")
                    exit()

        cmd = f'"{path}" "{tags_values}"'
        runCMD(command=cmd, wait_for_result=False, output_type="REALTIME_NORETURN")

    def write_snapshot_double(self, tags, values):
        """
        写double类型数据到数据库，该方法可能会导致程序异常退出，建议使用第三方exe独立调用该接口。
        如果出现“Python已停止工作”错误，请检查RDBProxy代理和数据库中是否存在相关的测点。

        :param tags: 标签名列表
        :param values: 数值列表
        :return:
        """
        n_size = len(tags)
        tag_names = (ctypes.c_char_p * n_size)()  # 名字
        time_long_arr = (ctypes.c_uint32 * n_size)()  # 时间
        qas_short_array = (ctypes.c_short * n_size)()  # 质量
        value_double_arr = (ctypes.c_double * n_size)()  # 浮点数类型的值
        value2_arr = (ctypes.c_int32 * n_size)()  # 整形类型的值
        value_type = (ctypes.c_int32 * n_size)()  # 数据类型
        time_long = int(time.time())  # 保证写入的数据点都具有同一个时标
        for i in range(n_size):
            tag_names[i] = ctypes_str2char_array(tags[i])
            time_long_arr[i] = time_long
            qas_short_array[i] = 0
            value_double_arr[i] = values[i]
            value2_arr[i] = 0
            value_type[i] = 3  # 3表示通过value_double_arr传输数据，其他表示通过value2_arr传输数据

        error_code_arr = (ctypes.c_short * 2)()  # 数据错误码，输出信息
        try:
            self.dll.DBPWriteSnapshot(
                self.handle,  # 句柄
                tag_names,  # char* sTagNames[],  //in,标签名字符串指针数组  //apistring
                time_long_arr,  # long ltimes[],   //in, 时标
                qas_short_array,  # short snqas[],   //in, 质量
                value_double_arr,  # double  dblvals[],   //in, 存放double值,DT_FLOAT32,DT_FLOAT64存放区
                value2_arr,  # long lvals[],   //in, 存放Long值,DT_DIGITAL,DT_INT32,DT_INT64存放区
                value_type,  # int  ntypes[],   //in, 数据类型,DT_INT32,DT_FLOAT32等。
                error_code_arr,  # short errs[],    //in/out, 错误码
                n_size  # int  nsize    //in, 个数
            )
        except:
            pass


def get_tag_value(snapshot, tag_description, optional_value=0):
    """
    根据标签描述获取快照中的数据

    :param snapshot:
    :param tag_description:
    :param optional_value: 标签不存在时的替代值，也就是默认值
    :return:
    """
    if isinstance(tag_description, Enum):  # 枚举类的对象
        tag_description = tag_description.name

    if isinstance(snapshot, dict):
        result = snapshot.get(tag_description)
    else:
        try:
            result = snapshot[tag_description][0]
            if isinstance(result, np.int64):
                result = None
            else:
                result = float(snapshot[tag_description][0])
        except KeyError:
            print(f"快照中不包括名为[{tag_description}]的变量，返回None")
            result = None
    if result is None:
        result = optional_value
    return result


class ColdResult:
    def __init__(self):
        """
        冷端优化的结果类，使用方法实力：
        # 初始化设置，只需执行一次
        cold_result = ColdResult()
        cold_result.设置允许的运行参数波动范围(allowed_range)
        cold_result.设置背压标签(["背压1", "背压2"])
        cold_result.设置冷端功率标签(["冷端总功率1", "冷端总功率2"])
        cold_result.设置状态参数标签()

        # 每次优化结果更新时
        cold_result.pass_result(result_opt)
        cold_result.平抑波动()
        result_opt = cold_result.opt_result

        其中，pass_result方法中传入的参数一般应包括：循泵、风机等最佳运行方式，当前实际的发电机功率、背压、环境温度、湿度、大气压力等
        """
        self.allowed_range = None  # 允许的参数波动范围，当机组运行状态在该范围内波动时，冷端优化结果不更新，该值示例如下，只与对象有关
        # [("电功率1", "±2"), ("供热流量", "±4"),("环境温度", "±4"), ("大气压力", "±10")]
        self.allowed_range_dict = {}  # {"电功率": [34, 38], "供热流量": [54, 62], ...}该值是变量，随时间变化
        self.last_state = None
        self.now_state = {}  # 当前时刻机组的实际运行参数
        self.opt_result = {}  # 当前时刻机组的优化后冷端优化结果
        self.bp_label = []  # 背压参数在数据集中的列标签名，一般就是"背压"，但对于全厂优化，可能有多个背压参数，以列表方式传入
        self.state_labels = []  # 状态参数在数据集中的列表签名，一般为["电功率", "供热量", "环境温度"]
        self.p_cold_label = None  # 冷端总功率在数据集中的列标签名
        self.last_opt_result = None  # 最后一个状态中的优化结果值
        self.last_true_state = None  # 最后一个状态中的实际状态值

    def 设置允许的运行参数波动范围(self, range=[]):  # todo
        """
        设置允许的参数波动范围，示例：
        cold_result = ColdResult()
        allowed_range = [("电功率1", "±2"), ("供热流量", "±4"),("环境温度", "±4"), ("大气压力", "±10")]
        cold_result.设置允许的运行参数波动范围(allowed_range)
        allowed_range中的键必须存在于self.pass_result()方法的true_state字典中。即allowed_range中有“电功率1”，则true_state参数也
        必须有"电功率1"。

        :param range:
        :return:
        """
        self.allowed_range = range

    def 设置背压标签(self, label):
        if isinstance(label, list):
            self.bp_label = label
        else:
            self.bp_label = [label]

    def 设置冷端功率标签(self, label):
        self.p_cold_label = label

    def 设置状态参数标签(self, labels):
        if isinstance(labels, list):
            self.state_labels = labels
        else:
            self.state_labels = [labels]

    def pass_result(self, opt_result=None, true_state=None):
        """
        传入新的冷端优化结果，并根据冷端功率大小调节背压大小以符合客观规律。如果某台机组停机，可以传入true_state="stop"或
        true_state={"1": "stop", "2": "run"}

        :param opt_result: 当前时刻的原始优化结果
        :param true_state: 当前时刻的运行值，至少包含电功率、供热、环境以及冷端运行方式等参数
        :return:
        """
        if true_state is None:
            true_state = {}
        if opt_result is None:
            opt_result = {}
        if isinstance(true_state, str):
            if true_state == "stop":
                # 说明是停机状态
                self.last_opt_result = {}
                self.last_true_state = {}
        else:
            group_nums = list(true_state.keys())
            for _gn in group_nums:
                if true_state.get(_gn) == "stop":
                    # 停机时，将_gn号机组的所有参数设置为0
                    ks = list(opt_result.keys())
                    for k in ks:
                        if k.endswith(str(_gn)):
                            self.last_opt_result.update({k: 0})

                    ks = list(true_state.keys())
                    for k in ks:
                        if k.endswith(str(_gn)):
                            self.last_true_state.update({k: 0})
                else:
                    # 将运行的机组的数据设置为传入的数据
                    self.update_group_data(group_num=_gn, opt_result=opt_result, true_state=true_state)
                self.now_state = true_state  # 当前时刻的运行值
                self.opt_result = opt_result

    def update_group_data(self, group_num, opt_result: dict = None, true_state: dict = None):
        """
        更新优化结果和真实结果，只更新指定的机组，机组号必须是标签名的最后一位，如power1表示1号机组的功率。

        :param group_num:
        :param opt_result:
        :param true_state:
        :return:
        """
        ks = list(opt_result.keys())
        for k in ks:
            if k.endswith(str(group_num)):
                self.last_opt_result.update({k: opt_result[k]})

        ks = list(true_state.keys())
        for k in ks:
            if k.endswith(str(group_num)):
                self.last_true_state.update({k: true_state[k]})

    def 背压合理化调整(self):
        def cal_dp(凝汽器热负荷, 冷端电功率变化, 环境温度):
            """
            计算背压变化值，背压变化与机组负荷、供热流量以及冷端设备运行方式有关

            :param power:
            :param heat:
            :param dpower:
            :return:
            """
            ...

        opt_result = self.opt_result
        true_state = self.now_state
        for bpl in self.bp_label:
            if opt_result[bpl] == 0:  # 如果停机状态
                continue
            else:
                _ = true_state[bpl] * (true_state[self.p_cold_label] / opt_result[self.p_cold_label])
                背压差 = abs(_ - true_state[bpl])
            if opt_result[bpl] < true_state[bpl]:
                opt_result[bpl] = true_state[bpl] + 背压差
            else:
                opt_result[bpl] = true_state[bpl] - 背压差
        self.opt_result = opt_result

    # def _get_allowed_range(self):

    def _get_allowed_range_str(self, title):
        for item in self.allowed_range:
            if item[0] == title:
                return item[1]

    def 平抑波动(self, unit=None):
        """
        当机组参数波动较小时，不改变冷端运行方式。

        参数判断分机组进行还是全厂一起进行，当unit值为None时，全厂整体平抑波动，如果需要分机组平抑波动，通过该值传入机组标号，如[1,2]。
        如果是分机组平抑波动，则self.opt_result中变量的最后一个字符需要与机组编号对应，如"power1"表示1号机组的参数。

        :param unit: 参数判断分机组进行还是全厂一起进行
        :return:
        """

        def get_min_max_value(val, range_str):
            # 根据当前值和表示范围的字符串，计算允许的参数的上下限的值
            if range_str.startswith("±"):
                _r = float(range_str[1:])
                min_val = val - _r
                max_val = val + _r
            elif range_str.endswith("%"):
                pass
            return min_val, max_val

        need_update = False  # 是否需要更新画面上的优化结果，如果参数波动小，则不更新，否则，更新
        if unit is None:
            for item in self.allowed_range:
                title, range = item
                if self.last_true_state.get(title) is None:  # 历史数据不存在，则认为满足小幅波动范围，直接更新优化结果为当前计算结果
                    need_update = True
                    break
                if not self.allowed_range_dict[title][0] <= self.now_state[title] <= self.allowed_range_dict[title][1]:
                    need_update = True
                    break

            if need_update:  # 如果需要更新优化结果，更新新的允许的参数波动范围
                for item in self.allowed_range:
                    title, range = item
                    val = self.now_state[title]
                    min_val, max_val = get_min_max_value(val, range)
                    self.allowed_range_dict.update({title: [min_val, max_val]})
            else:  # 如果波动幅度小，则不需要更新优化结果，直接返回上一次优化结果
                self.opt_result = self.last_opt_result
        else:
            for u in unit:
                for item in self.allowed_range:
                    title, _range = item
                    if title.endswith(str(u)):
                        if self.last_true_state.get(title) is None:
                            need_update = True
                            break
                        if not self.allowed_range_dict[title][0] <= self.now_state[title] <= \
                               self.allowed_range_dict[title][1]:
                            need_update = True
                            break
                if need_update:
                    for item in self.allowed_range:
                        title, _range = item
                        if title.endswith(str(u)):  # 只限制运行方式，不限制背压
                            val = self.now_state[title]
                            min_val, max_val = get_min_max_value(val, _range)
                            self.allowed_range_dict.update({title: [min_val, max_val]})
                        # 如果需要更新，则维持现有的opt_result结果不变
                else:
                    for k, v in self.opt_result.items():
                        if k.endswith(str(u)) and not str_in_list(k, self.bp_label):  # 优化后背压仍取实时值
                            self.opt_result.update({k: self.last_opt_result.get(k)})

    def get_result(self):
        return self.opt_result
