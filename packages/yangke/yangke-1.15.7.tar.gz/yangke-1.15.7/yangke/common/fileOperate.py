import traceback

import numpy as np
import pandas as pd
# import pickle
import dill as pickle
import re
import os
import time
import datetime

import pandas.errors

from yangke.base import add_sep_to_csv, get_encoding_of_file
from yangke.common.config import logger


def get_last_modified_time(file: str):
    last_change_time = os.stat(file).st_mtime
    last_change_time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_change_time))
    last_change_time = datetime.datetime.strptime(last_change_time_str, "%Y-%m-%d %H:%M:%S")
    return last_change_time


class re_common:
    """
    常见正则表达式的操作

    Example:
        1. 需要删除括号及括号中的内容，则使用以下语句：

        re = fo.re_common("前者多指对文章（书籍）中某一部分，但为了防止冗杂而把它放在段落之外（文末或页边）")
        result = re.del_char_in_brackets("（", "）")


    """

    def __init__(self, content):
        """
        用需要处理的目标字符串初始化re_common类对象

        :param content: 需要处理的目标字符串
        """
        self.content = content

    def del_char_in_brackets(self, left="(", right=")"):
        """
        如果content中包含括号，则删除括号及括号中的内容。

        :param left: 左括号的字符，如【、{、（、<、<-、《等
        :param right: 右括号的字符
        :return:
        """
        content_ = self.content
        result = re.match(f".*{left}.+{right}.*", content_)  # 判断content中是否存在（）
        while result:
            temp_list = list(re.findall(f"(.*){left}.+{right}(.*)", content_)[0])  # 正则中()中的内容会保留
            temp_list = [item for item in temp_list if item != ""]  # 删掉空字符串
            content_ = "".join(temp_list)  # 拼接起来
            result = re.match(f".*{left}.+{right}.*", content_)  # 判断content中是否存在（），存在就继续去除
        self.content = content_
        return self.content


def read_data(file, encoding="utf8"):
    """
    读取股票数据的csv文件内容到
    :param file:
    :param encoding:
    :return:
    """
    f = open(file)
    df = pd.read_csv(f, encoding=encoding)
    data_local = df.iloc[:, 1:6]
    return data_local.values


def write_line(file: str, line: str, encoding="utf8", append=False):
    """
    将字符串line内容写入文件，如果文件不存在则创建，如果文件存在，默认覆盖原文件，可以通过设置append=True实现追加文本
    """
    mode = 'a' if append else 'w'
    file = os.path.abspath(file)
    if not os.path.exists(os.path.dirname(file)):
        try:
            os.makedirs(os.path.dirname(file))
        except PermissionError:
            logger.error(f"权限不足，无法写入文件{file}")
    with open(file, encoding=encoding, mode=mode) as f:
        f.write(line)


def write_lines(file: str, lines: list, encoding="utf8", append=False):
    """
    将字符串列表写入文件，每个列表项为单独一行
    """
    import os
    mode = 'a' if append else 'w'
    file = os.path.abspath(file)
    if not os.path.exists(os.path.dirname(file)):
        try:
            os.makedirs(os.path.dirname(file))
        except PermissionError:
            logger.error(f"权限不足，无法写入文件{file}")
    # lines = os.linesep.join(lines)  # 列表项之间添加换行符，os.linesep会换两行
    lines = "\n".join(lines)
    with open(file, encoding=encoding, mode=mode) as f:
        f.writelines(lines)


def read_lines(file: str, dropna=False) -> list:
    """
    读取文件中的所有行至列表，可以自动识别文本的编码格式

    :param file:
    :param dropna: 是否丢弃空行，默认不丢弃
    :return:
    """
    encoding = get_encoding_of_file(file)
    with open(file, encoding=encoding, mode='r') as f:
        lines = f.readlines()

    result = []
    for line in lines:
        if line.strip():
            line = line.rstrip("\n").rstrip("\r")
            result.append(line)  # 删除行右侧的换行符

    return result


def read_points(file: str, split=',', return_type='[x][y][z]'):
    """
    从txt文件中读取点坐标

    :param file:
    :param split:
    :param return_type: '[x][y][z]'则返回x,y,z三个列表，如果是'[xyz]'则返回[x,y,z]形式的点坐标列表
    :return:
    """
    points = []
    x, y, z = [], [], []
    with open(file, mode='r') as f:
        for line in f.readlines():
            coor = line.split(split)
            px = float(coor[0])
            py = float(coor[1])
            pz = float(coor[2])
            points.append([px, py, pz])
            x.append(px)
            y.append(py)
            z.append(pz)

    if return_type == '[xyz]':
        return points
    else:
        return x, y, z


def write_as_pickle(file: str, obj: object):
    """
    保存任意对象到硬盘文件，obj是函数对象时，保存的是函数的名称和地址，无法在应用重启后加载原函数。
    如果需要保存函数，请使用write_func(file: str, func: object)

    :param file:
    :param obj:
    :return:
    """
    try:
        file = os.path.abspath(file)
        if not os.path.exists(os.path.dirname(file)):
            os.makedirs(os.path.dirname(file))
        with open(file, 'wb') as f:
            pickle.dump(obj, f)
    except OSError:
        traceback.print_exc()
        logger.error(f"保存对象时发生错误，保存路径为{file}，对象为{obj}")
    except:
        traceback.print_exc()
        logger.error(f"保存对象时发生错误，保存路径为{file}，对象为{obj}")


def read_from_pickle(file: str):
    """
    从硬盘文件加载pickle对象，obj是函数对象时，请使用read_func(file: str, func: object)，文件不存在时返回None

    :param file: 硬盘文件
    :return:
    """
    if file is None:
        return None
    if not os.path.exists(file):  # 文件不存在，返回None
        return None
    obj = None
    try:
        with open(file, 'rb') as f:
            obj = pickle.load(f)
    except:
        traceback.print_exc()
        logger.error(f"加载文件{f}时发生错误！")
    return obj


def write_func(file: str, func: object):
    """
    保存python函数或方法到硬盘，以便应用重启后直接加载

    :param file: 保存到的文件名
    :param func: 需要保存的函数名
    :return:
    """
    import dill
    write_as_pickle(file, dill.dumps(func))


def read_func(file: str):
    """
    从硬盘文件中加载函数对象

    :param file:
    :return:
    """
    import dill
    return dill.loads(read_from_pickle(file))


def read_from_yaml(file: str, encoding="utf8"):
    import yaml
    if not os.path.exists(file):  # 文件不存在，返回空字典
        return {}
    with open(file, 'r', encoding=encoding) as f:
        content = f.read()
    """
    Loader的几种加载方式 
    BaseLoader--仅加载最基本的YAML 
    SafeLoader--安全地加载YAML语言的子集。建议用于加载不受信任的输入。 
    FullLoader--加载完整的YAML语言。避免任意代码执行。这是当前（PyYAML 5.1）默认加载器调用 
            yaml.load(input)（发出警告后）。
    UnsafeLoader--（也称为Loader向后兼容性）原始的Loader代码，可以通过不受信任的数据输入轻松利用。"""
    obj = yaml.load(content, Loader=yaml.FullLoader)
    return obj


def write_as_yaml(file, obj):
    import yaml
    with open(file, 'w') as f:
        f.write(yaml.dump(obj, allow_unicode=True))


def write_excel(file, dataframe_dict: dict, index=False):
    with pd.ExcelWriter(file) as writer:
        for sheet, df in dataframe_dict.items():
            df.to_excel(writer, sheet_name=sheet, index=index)
    return


def read_excel(file, need_merge=False, index_col=True):
    """
    将excel文件中的所有sheet读取到dataframe_dict中

    :param need_merge: 是否合并各个sheet中的数据，默认不合并，且只有各个sheet中数据格式相同时才能合并
    :param file:
    :param index_col: 是否需要索引，也可以是数字
    :return:
    """
    if index_col:
        index_col = 0
    file = pd.ExcelFile(file)
    sheets = file.sheet_names
    if not need_merge:
        dataframe_dict = {}
        for sheet in sheets:
            df = pd.read_excel(file, sheet_name=sheet, index_col=index_col)
            dataframe_dict.update({sheet: df})
        return dataframe_dict
    else:
        from yangke.base import merge_two_dataframes, merge_dataframes_simple
        res = None
        for sheet in sheets:
            if res is None:
                res = pd.read_excel(file, sheet_name=sheet, index_col=index_col)
            else:
                res = merge_dataframes_simple([res, pd.read_excel(file, sheet_name=sheet, index_col=index_col)])

        return res


def read_csv_assist(file, sep=",", encoding="utf-8"):
    data = []
    with open(file, 'r', encoding=encoding) as f_input:
        for line in f_input:
            data.append(list(line.strip().split(sep)))
    return pd.DataFrame(data)


def read_csv_ex(file, sep=None, header="infer", skiprows=None, on_bad_lines='skip', nrows=None, index_col=None,
                low_memory=None, na_values=" ") -> pd.DataFrame:
    """
    pandas增强版的read_csv()方法，可以自动匹配任何文件编码，自动补全数据列不全的行

    :param skiprows:
    :param low_memory:
    :param index_col:
    :param nrows:
    :param file:
    :param sep:
    :param header:
    :param on_bad_lines:
    :param na_values: 设置na_values=" "，则pandas在读取到" "时，会替换为数值类型的np.nan，如果不设置，则缺失数据的列会被视为object，导致无法进行数学计算
    :return:
    """
    encoding_csv = get_encoding_of_file(file)
    to_file1 = os.path.join(os.path.dirname(file), f"{os.path.basename(file)[:-4]}_temp_修正.csv")
    if file[-3:].lower() == "txt" and sep is None:  # txt文件默认以空格作为分隔符
        sep = "\s+"
    to_file1 = add_sep_to_csv(file, sep, to_file=to_file1, encoding=encoding_csv)
    if file[-3:].lower() == "txt" and sep == "\s+":  # 如果该条件满足，则add_sep_to_csv已经将分隔符替换为"\t"
        sep = "\t"
    if sep is None:
        sep = ","
    try:
        data = pd.read_csv(to_file1, sep=sep, header=header, on_bad_lines=on_bad_lines,
                           encoding=encoding_csv, skiprows=skiprows, nrows=nrows, index_col=index_col,
                           low_memory=low_memory, na_values=na_values)
    except pandas.errors.ParserError:  # 有可能是双引号导致的错误，删除双引号重新尝试一次
        to_file1 = add_sep_to_csv(file, sep, to_file=to_file1, encoding=encoding_csv, delete_quote=True)
        data = pd.read_csv(to_file1, sep=sep, header=header, error_bad_lines=on_bad_lines,
                           encoding=encoding_csv, skiprows=skiprows, nrows=nrows, index_col=index_col,
                           low_memory=low_memory, na_values=na_values)
    if os.path.exists(to_file1):
        os.remove(to_file1)
    return data


def pd_set_na(df, conditions, expand=False, axis=0):
    """
    将dataframe中满足指定条件的行的元素置为np.nan
    示例：
    pd_set_na(df, {"大气压力": {"<": 0.03}}, expand=True, axis=0)
    pd_set_na(df, {"大气压力": {"<": 0.03, ">": "0.2"}}, expand=True, axis=0)
    pd_set_na(df, {"大气压力": "大气压力<0.03 and 环境温度<0.2", expand=True, axis=0)
    pd_set_na(df, {"大气压力": "大气压力<0.03 or 大气压力>0.2", expand=True, axis=0)

    :param df:
    :param conditions:
    :param expand:
    :param axis:
    :return:
    """
    for title, cond in conditions.items():
        cond: dict = cond
        for op, val in cond.items():
            if op == "<":
                if expand:
                    for col in df.columns:
                        if col != title:
                            df.loc[df[title] < val, col] = np.nan
                    df.loc[df[title] < val, title] = np.nan  # 最后处理title列对应的行，防止数据改变导致条件失效
                else:
                    df.loc[df[title] < val, title] = np.nan
            elif op == ">":
                if expand:
                    for col in df.columns:
                        if col != title:
                            df.loc[df[title] > val, col] = np.nan
                    df.loc[df[title] > val, title] = np.nan  # 最后处理title列对应的行，防止数据改变导致条件失效
                else:
                    df.loc[df[title] > val, title] = np.nan


def fill_excel_cell(file, sheet: int | str = 0, row=1, col: int | str = 1, cell=None, value=None, visible=True,
                    close=True, res=None):
    """
    在excel文件中动态填入参数，并自动计算一次excel。使用示例：
    fill_excel_cell('test.xlsx", "Sheet1", row=1, col="C", value="hello world")

    入股需要多次填充同一个excel文件，为了避免反复打开关闭文件，可以设置close和res参数。示例如下：
    res = fill_excel_cell('test.xlsx", "Sheet1", cell="A1", value="hello world", close=False)  # 第一次close=False
    res = fill_excel_cell('test.xlsx", "Sheet1", cell="A2", value="value A2", close=False, res=res) #第二次res传入第一次的结果
    ...
    res = fill_excel_cell('test.xlsx", "Sheet1", cell="A3", value="value A3", close=True, res=res) # 最后一次close=True

    :param file: 需要填入参数的Excel文件路径
    :param sheet: Excel中的sheet名或索引
    :param row:
    :param col:
    :param cell: 以"A1"形式标记的单元格坐标
    :param value:
    :param visible:
    :param close: 填充后是否关闭excel文件
    :param res: 如果上次未关闭excel文件，则通过该参数传入上次打开的文件信息
    :return:
    """
    if res is None:
        import xlwings as xw
        if not os.path.exists(os.path.abspath(file)):
            logger.error(f"操作的excel文件不存在 : {os.path.abspath(file)}")

        app = xw.App(visible=visible, add_book=False)
        app.display_alerts = False
        app.screen_updating = visible
        # app.calculation = "manual"
        wb = app.books.open(file)
    else:
        app, wb = res
    sht = wb.sheets[sheet]
    if cell is not None:
        sht.range(cell).value = value
    else:
        sht.range(f"{col}{row}").value = value

    if close:
        app.calculate()
        wb.save()
        app.quit()
    else:
        return app, wb


if __name__ == "__main__":
    fill_excel_cell(file=r'C:\Users\YangKe\Desktop\碳排放量计算.xlsx', sheet='附表 C.3 化石燃料燃烧排放表', row=3,
                    value=23,
                    col='E')
