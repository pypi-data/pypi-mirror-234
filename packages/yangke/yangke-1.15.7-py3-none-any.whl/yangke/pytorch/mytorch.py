import copy
import random
import re
from collections import OrderedDict
from typing import Optional

import numpy as np
import optuna
import pandas as pd
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from torch.utils.tensorboard import SummaryWriter

from yangke.base import get_settings, YkDict, is_number
from yangke.common.config import logger
from yangke.common.fileOperate import read_csv_ex
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class PriorLoss(nn.Module):
    """
    自定义的损失函数，可以使用已有的先验知识
    """

    def __init__(self, input_titles, net):
        self.input_titles = input_titles
        super(PriorLoss, self).__init__()
        self.rules = []
        self.reg_rules = []  # [("der>0, '电功率'")]  # 表示输出对电功率的导数大于0
        self.net = net  # 损失函数所属的神经网络
        self.punish = 1000  # 当预测结果违背先验知识时的损失函数惩罚因子

    def forward(self, pred, target, input):
        """
        损失函数返回的参数是0-dim的tensor

        :param pred: 输出参数预测值
        :param target: 输出参数实际值
        :param input: 输入参数
        :return:  2866343884064  2866343893200
        """
        x = input
        x.requires_grad = True
        if x.grad is not None:
            x.grad = x.grad - x.grad  # 清空以前的梯度
        predict = self.net(x)
        # y对x求导
        _y = predict.mean()
        _y.backward()  # 只是计算梯度，不进行权值更新
        grad = x.grad  # 则此处x.grad就是y对x的导数
        x.requires_grad = False

        correction = self.apply_rules(x, grad)  # 先验知识的修正项

        ret = torch.abs(pred - target).squeeze()
        ret = torch.pow(ret, 2) + correction
        loss = ret.mean()
        return loss

    def apply_rules(self, input, grad):
        """
        在【输入参数】和【输出对输入参数的梯度】上求解先验知识的修正项
        :param input: Tensor:(32,2)当batch_size=32，input_dims=2
        :param grad: Tensor:(32,2)
        :return:
        """
        correction = torch.zeros_like(grad[:, 0])  # 无论输入有多少个，损失函数值只有一个，因此只取grad的第一个为维度
        for rr in self.reg_rules:
            if rr[0] == "der>0":
                idx = self.input_titles.index(rr[1])
                _cor = grad[:, idx]  # 所有输入对x的导数，该数应该大于0才符合先验知识
                _cor = -_cor * self.punish  # 如果导数小于0，则correction为大于0的数，即损失增大
                _cor = torch.clamp(_cor, 0, None)  # 将所有小于0的数用0代替，即导数大于0时，损失修正值为0
                correction = correction + _cor
            elif rr[0] == "der<0":
                idx = self.input_titles.index(rr[1])
                _cor = grad[:, idx]
                _cor = _cor * self.punish  # 如果导数大于0，则correction为大于0的数，即损失增大
                _cor = torch.clamp(_cor, 0, None)
                correction = correction + _cor
            else:
                logger.error(f"暂不支持其他条件！{rr}")
                return
        return correction

    def translate_rules(self):
        for rule in self.rules:
            if rule.get("isChecked"):
                expression = rule.get("expression")

            else:
                op = rule.get("op")
                if op == "任何条件":
                    expression = rule.get("expression")
                else:
                    logger.error(f"暂不支持带条件的先验知识")
                    expression = None
            res = re.findall('\[(.+?)\]', expression)  # 加一个?则是最小匹配，否则时贪婪匹配
            plus = re.findall('.*单调递(.+)', expression)
            if len(res) == 2 and len(plus) == 1:
                if plus[0] == "增":
                    self.reg_rules.append(['der>0', res[1]])
                else:
                    self.reg_rules.append(['der<0', res[1]])
            else:
                logger.error(f"未知的条件格式")

    def add_knowledge(self, rule):
        """
        添加已有的先验知识规则。示例：
        1. 任何条件下，背压都随电功率单调递增
        {'isChecked': False, 'op': '任何条件', 'expression': '[背压]随[电功率]单调递增'}

        2. 电功率小于100时，背压随电功率单调递增
        {'isChecked': False, 'var1': '电功率', 'op': '小于', 'var2': '100', 'expression': '[背压]随[电功率]单调递增'}

        3. 同时传入多个先验知识的规则，使用列表表示，如下：
        [{'isChecked': False, 'var1': '电功率', 'op': '任何条件', 'var2': '电功率', 'expression': '[背压]随[电功率]单调递增'}, {'isChecked': False, 'var1': '电功率', 'op': '任何条件', 'var2': '电功率', 'expression': '[背压]随[环境温度]单调递增'}]

        4. 使用表达式表示规则，则isChecked设置为True
        {'isChecked': True, "expression": "[背压]随[电功率]单调递增 if [电功率]>100 or [电功率]<500"}

        y随着输入1的增加而增加，则
        rule = 'x(1).grad>0' 或 rule = 'x(电功率).grad>0'  其中第一个输入参数名为电功率

        :param rule:
        :return:
        """
        if isinstance(rule, list):
            self.rules = rule
        else:
            self.rules.append(rule)

        self.translate_rules()

    def clear_knowledge(self):
        self.rules = []


def standard_reverse(out, mean, std):
    """
    将预测结果反标准化

    :param out:
    :return:
    """
    if isinstance(std, pd.Series):
        std = std.item()  # Series.values是ndarray, item()返回的是数值float型
    if isinstance(mean, pd.Series):
        mean = mean.item()

    if isinstance(out, torch.Tensor):
        out = out.detach().numpy()
    return out * std + mean


def all_number(row: pd.Series):
    """
    判断row中的值是否都是数值

    :param row:
    :return:
    """
    res = True
    for v in list(row.to_numpy()):
        if not is_number(v):
            res = False
            break
    return res


class DataSetFitting(Dataset):
    def __init__(self, data_source, x_title=None, y_title=None, mean=None, std=None, proportion_train=0.8,
                 proportion_test=0.2, classify=False):
        """
        构建数据集。
        用法示例：
        # 1. 构建数据集
        dataset = DataSetFitting(df, ["x1", "x2"], ["y"])
        # 2. 数据集归一化
        dataset.set_standard(normal_method="min-max")

        :param data_source: 数据源，可以为settings.yaml文件配置，也可以是pd.DataFrame对象
        :param x_title: 输入参数的列标题，如果从配置文件加载，则可以为None
        :param y_title: 输出参数的列标题，如果从配置文件加载，则可以为None
        :param mean: 数据集的平均值
        :param std: 数据集的标准差
        :param proportion_train: 训练集的比例，默认80%
        :param proportion_test: 测试集比例，默认20%
        :param classify: 是否为分类问题的数据集，如果是分类问题，则归一化不会对标签应用，否则会将标签也归一化处理
        """
        self.dataframe = None
        self.x_title = None
        self.y_title = None
        self.normal_method = None
        self.y_range = None
        self.x_range = None
        self.proportion_train = proportion_train
        self.proportion_test = proportion_test
        if isinstance(data_source, pd.DataFrame):
            self.dataframe = data_source
            self.x_title = x_title or []
            self.y_title = y_title or []
            if not isinstance(self.y_title, list):
                self.y_title = [self.y_title]
        elif isinstance(data_source, YkDict):
            files = data_source.get_settings("dataset.data_file")
            self.normal_method = data_source.get_settings("dataset.normalization") or "z-score"
            input_set = data_source.get("input")
            self.x_title = [item["name"] for item in input_set]
            self.x_range = [None if item.get("range") is None else eval(item["range"]) for item in input_set]
            del input_set
            output_set = data_source.get_settings("output.para")
            if len(output_set) > 0 and isinstance(output_set[0], str):
                self.y_title = output_set
                self.y_range = None
            else:
                self.y_title = [item["name"] for item in output_set]
                self.y_range = [None if item.get("range") is None else eval(item["range"]) for item in output_set]
            for file in files:
                ext = file.get("type")
                filename = file.get("name")
                if not os.path.exists(filename):
                    continue
                if ext == "csv":
                    data_frame = read_csv_ex(filename)
                else:
                    data_frame = pd.read_excel(filename)
                if self.dataframe is not None and data_frame is not None:
                    self.dataframe = pd.concat([self.dataframe, data_frame], axis=0, ignore_index=True)
                else:
                    self.dataframe = self.dataframe or data_frame

            # 删除某些行
            self.drop_by_condition(data_source.get_settings("dataset.drop"))

        self.classify = classify
        # 仅保留x,y相关的数据列，删除其他列
        titles = self.x_title.copy()
        titles.extend(self.y_title)
        if self.dataframe.shape[0] < 1:
            logger.warning("传入的数据文件中数据为空或数据文件不存在")
        self.dataframe = self.dataframe[titles].copy()

        # 找出dataframe中非数值的行
        self.dataframe["is_number"] = self.dataframe.apply(lambda _: all_number(_), axis=1)
        origin_titles = set(self.dataframe.index)
        self.dataframe = self.dataframe[self.dataframe['is_number']]
        self.non_numeric_lines = list(origin_titles - set(self.dataframe.index))
        if len(self.non_numeric_lines) > 0:
            logger.warning(f"数据集中存在非数值的行，已删除这些行，行号为：{self.non_numeric_lines}")
        self.dataframe = self.dataframe.astype(float).copy()
        self.dataframe = self.dataframe[titles].copy()

        # 数据标准化
        self.mean = mean  # 可能为None，后续处理
        self.std_range = std
        self.dataframe_std = None  # 归一化的数据集
        # self.set_standard()

    def set_standard(self, mean=None, std_range=None, normal_method=None, x_range=None, y_range=None):
        """
        设置数据的归一化参数，在初始化部分数据时，直接从部分数据集得到的归一化参数可能出现偏差，这里提供一种外部设置的方法。
        不建议中途更改数据归一化方法，否则可能导致模型预测结果很离谱。

        min-max将数据归一化到(-1,1)的区间上

        :param mean: 参数的平均值
        :param std_range: 参数的标准差或振幅
        :param normal_method: 数据归一化方法，支持"z-score"和"min-max"
        :param y_range: [(0, 20)]
        :param x_range: [(0, 100), (0, 20), (0, 30)]
        :return:
        """
        if normal_method is None or normal_method == self.normal_method:
            if mean is None and std_range is None:
                logger.debug(f"mean and std is None, try to calculate by method {self.normal_method}")
                if self.normal_method == "z-score":
                    self.mean = self.mean or self.dataframe.mean()
                    self.std_range = self.std_range or self.dataframe.std()
                    self.dataframe_std = self.standard(self.dataframe)  # 必须放在这里，不然可能由于编译优化被忽略
                    if self.classify:  # 分类问题，不能对标签进行归一化处理
                        self.dataframe_std[self.y_title] = self.dataframe[self.y_title]
                    return
                else:
                    self.x_range = x_range or self.x_range
                    self.y_range = y_range or self.y_range
                    if self.y_range is not None:
                        x_min = [x[0] for x in self.x_range]
                        y_min = [y[0] for y in self.y_range]
                        x_max = [x[1] for x in self.x_range]
                        y_max = [y[1] for y in self.y_range]
                        x_min.extend(y_min)
                        all_min = np.asarray(x_min)
                        x_max.extend(y_max)
                        all_max = np.asarray(x_max)
                        title = copy.deepcopy(self.x_title)
                        title.extend(self.y_title)
                        self.mean = pd.Series(data=(all_min + all_max) / 2, index=title)
                        self.std_range = pd.Series(data=(all_max - all_min) / 2, index=title)
                    else:
                        logger.warning("数据归一化方法为min-max，但未设置各参数的取值范围")
            else:
                self.mean = mean
                self.std_range = std_range
            if self.mean is not None and self.std_range is not None:
                self.dataframe_std = self.standard(self.dataframe)
            else:
                logger.debug(f"数据归一化失败，原因：{self.mean=}, {self.std_range=}")
                self.dataframe_std = None
        else:
            self.normal_method = normal_method
            self.set_standard(mean=mean, std_range=std_range, normal_method=normal_method, x_range=x_range,
                              y_range=y_range)
        if self.classify:  # 分类问题，不能对标签进行归一化处理
            self.dataframe_std[self.y_title] = self.dataframe[self.y_title]

    def standard(self, df):
        """
        数据标准化

        :param df: Dataframe(num, input_and_output_dim)
        :return:
        """
        # Dataframe和Series运算的前提是：Dataframe的列标题和Series的索引名必须一一对应，而不仅仅看维度，否则可能会出错，
        return (df - self.mean) / self.std_range  # mean Series (input_and_output_dim,)

    def standard_reverse(self, out):
        """
        将预测结果反标准化

        :param out:
        :return:
        """
        std = self.std_range[self.y_title]
        mean = self.mean[self.y_title]
        if isinstance(std, pd.Series):
            std = std.item()  # Series.values是ndarray
        if isinstance(mean, pd.Series):
            mean = mean.item()
        return out * std + mean

    def __getitem__(self, index):
        """
        DataSet子类必须实现的方法，用于根据索引返回一条数据，数据类型需要是Tensor

        :param index:
        :return:
        """
        if self.dataframe_std is None:
            logger.warning(f"数据集没有归一化处理")
            self.dataframe_std = self.dataframe
        single_item = self.dataframe_std.iloc[index, :]
        _x = torch.from_numpy(single_item[self.x_title].to_numpy()).to(torch.float32)
        if self.classify:  # 如果是分类问题，则输出必须是torch.LongTensor类型
            # crossEntropyLoss会将整数转换成one-hot类型的数组，因此每一个标签必须是整数，不能是数组
            _y = torch.from_numpy(single_item[self.y_title].to_numpy()).to(torch.long).squeeze()
            # _y = _y.long()
        else:
            _y = torch.from_numpy(single_item[self.y_title].to_numpy()).to(torch.float32)

        return _x, _y

    def __len__(self):
        """
        DataSet子类必须实现的方法，用于获取DataSet的大小

        :return:
        """
        return self.dataframe.shape[0]

    def get_size(self):
        return self.dataframe.shape[0]

    def drop_by_condition(self, conditions):
        for cond in conditions:
            if list(cond.keys())[0] == "or":
                for co in cond.get("or"):
                    if "<=" in co:
                        title, value = tuple(co.split("<="))
                        title = str(title).strip()
                        value = float(value)
                        self.dataframe = self.dataframe[self.dataframe[title] > value]  # 删除小于的行 = 保留大于的行
                    elif ">=" in co:
                        title, value = tuple(co.split(">="))
                        title = str(title).strip()
                        value = float(value)
                        self.dataframe = self.dataframe[self.dataframe[title] < value]  # 删除小于的行 = 保留大于的行
                    elif "<" in co:
                        title, value = tuple(co.split("<"))
                        title = str(title).strip()
                        value = float(value)
                        self.dataframe = self.dataframe[self.dataframe[title] >= value]  # 删除小于的行 = 保留大于的行
                    elif ">" in co:
                        title, value = tuple(co.split(">"))
                        title = str(title).strip()
                        value = float(value)
                        self.dataframe = self.dataframe[self.dataframe[title] <= value]  # 删除大于的行 = 保留小于的行

    def split_set(self, part1=None, part2=None, part3=None):
        """
        按照指定的比例将数据集分割，一般用于将总体数据集分割为训练集，测试集，验证集等

        :param part1:
        :param part2:
        :param part3:
        :return:
        """
        part1 = part1 or self.proportion_train
        part2 = part2 or self.proportion_test
        if part3 is not None:
            assert part1 + part2 + part3 == 1, "数据集比例之和不为1"
            size = self.get_size()
            size1, size2 = int(part1 * size), int(part2 * size)
            set1, set2, set3 = torch.utils.data.random_split(self, [size1, size2, size - size1 - size2])
            return set1, set2, set3
        elif part2 is not None:
            if part1 + part2 < 1:
                return self.split_set(part1, part2, 1 - part1 - part2)
            else:
                size = self.get_size()
                size1 = int(part1 * size)
                return torch.utils.data.random_split(self, [size1, size - size1])
        else:
            size = self.get_size()
            size1 = int(part1 * size)
            return torch.utils.data.random_split(self, [size1, size - size1])


class DataFitterNet(torch.nn.Module):
    def __init__(self, settings1, trial=None):
        """
        一个用于数据拟合的神经网络类库，神经网络架构通过settings.yaml文件进行配置

        :param settings1:
        :param trial: 使用optuna超参数调优时会传入该参数
        """
        super(DataFitterNet, self).__init__()
        self.dataset: DataSetFitting | None = None  # 数据集的信息，主要需要使用数据集中的归一化与反归一化的信息，但不会保存dataframe数据
        cfg = settings1.get("networks")  # 获取神经网络结构信息
        settings1 = YkDict(settings1)
        self.settings = settings1
        self.trial = trial
        self.cfg = cfg
        self.in_num = 0  # 输入层神经元个数，对应输入参数的个数
        self.out_num = 1
        loss_func_type = settings1.get_settings("networks.loss_fn.type")
        if loss_func_type == "CrossEntropy":  # 必须是分类问题才能使用CrossEntropy损失函数
            self.classify = True
            self.class_num = settings1.get_settings("networks.loss_fn.bak_info")

        train_settings = settings1.get_settings("networks.train") or {}
        self.lr = self.get_para_of_optuna_str(train_settings.get("learning_rate") or 1e-3, "lr")
        self.epochs = int(train_settings.get("epochs") or 10)
        self.batch_size = self.get_para_of_optuna_str(train_settings.get("batch_size") or 64, "batch_size")

        self.mean: Optional[pd.Series] = None
        self.std: Optional[pd.Series] = None
        self.normal_method = None  # 数据归一化方法
        self.x_title = settings1.get("input") or []
        self.y_title = settings1.get("output") or []
        if not isinstance(self.y_title, list):  # 因为输出经常为一个参数，如果用户没有以列表形式指定该参数，则转换成列表形式
            self.y_title = [self.y_title]
        self.max_err = 0
        self.average_err = 0
        _cell_num_last_layer = 0  # 循环中记录上一层神经网络的输出个数
        i = 1
        layer_dict = OrderedDict()
        for layer in cfg.get("layers"):  # 从配置中拿到神经网络各层的信息，进而构建神经网络
            _type = self.get_para_of_optuna_str(layer.get("type"), f"layer_type{i}")
            _cell_num = 1
            if _type == "input":  # 输入/输出层的神经元个数可以根据输入/输出参数个数自动确定
                _cell_num = layer.get("cell_num") or 10
                if layer.get("cell_num") == "auto" or layer.get("cell_num") is None:
                    self.in_num = len(settings1.get("input"))
                    _cell_num = self.in_num
                else:
                    self.in_num = int(layer.get("cell_num") or 10)
                    _cell_num = self.in_num
            elif _type == "linear":
                bias = False if layer.get("bias") is False else True
                _cell_num = self.get_para_of_optuna_str(layer.get("cell_num") or 10, f"cell_num{i}")
                layer_dict[f"layer{i}"] = nn.Linear(_cell_num_last_layer, _cell_num, bias=bias)
            elif _type == "relu":
                layer_dict[f"layer{i}"] = nn.ReLU()
                _cell_num = _cell_num_last_layer  # 激活函数输入输出个数不变
            # elif _type == 'softmax':
            #     self.layers.append(nn.Softmax())
            elif _type == "sigmoid":
                layer_dict[f"layer{i}"] = nn.Sigmoid()
                _cell_num = _cell_num_last_layer
            elif _type == "tanh":
                layer_dict[f"layer{i}"] = nn.Tanh()
                _cell_num = _cell_num_last_layer
            elif _type == "dropout":
                p = self.get_para_of_optuna_str(layer.get('rate'), "dropout_rate")
                layer_dict[f"layer{i}"] = nn.Dropout(p=p)
                _cell_num = _cell_num_last_layer
            elif _type.lower() == "rbf":
                _cell_num = layer.get("cell_num") or 10
                self.in_num = len(settings1.get("input"))
                self.out_num = len(settings1.get("output"))
                logger.error("暂不支持径向基神经网络")
            elif _type.lower() == "none":  # 空层
                continue
            elif _type == "output":  # 输入/输出层的神经元个数可以根据输入/输出参数个数自动确定
                if self.classify:  # 如果是分类问题，则输出个数为类别数量，分别对应每一类的概率
                    self.out_num = self.class_num
                else:
                    if layer.get("cell_num") == "auto" or layer.get("cell_num") is None:
                        self.out_num = len(self.y_title)
                    elif settings1.get_settings("output.type") == "single_output":
                        if layer.get("cell_num") != "auto" and int(layer.get("cell_num")) != 1:
                            logger.warning(
                                "数据集使用single_output，但神经网络模型输出层单元个数不为1，忽略神经网络输出单元个数设置！")
                        self.out_num = 1
                    else:
                        self.out_num = layer.get("cell_num")
                bias = False if layer.get("bias") is False else True
                layer_dict[f"layer{i}"] = nn.Linear(_cell_num_last_layer, self.out_num, bias=bias)
            else:
                logger.warning(f"发现不支持的layer类型：{_type}")

            _cell_num_last_layer = _cell_num
            i = i + 1

        if self.classify:
            layer_dict[f"layer{i}"] = nn.Softmax(dim=1)  # nn.functional.softmax()

        self.net = nn.Sequential(layer_dict)
        weight_decay = self.get_para_of_optuna_str(settings1.get_settings("networks.optimizer.weight_decay") or 0,
                                                   "weight_decay")
        if settings1.get_settings("networks.optimizer.type") == "adam":
            self.optimizer = torch.optim.Adam(self.parameters(), lr=self.lr, weight_decay=weight_decay)
        else:
            self.optimizer = torch.optim.SGD(self.parameters(), lr=self.lr, weight_decay=weight_decay)

        if settings1.get_settings("networks.loss_fn.type") == "MSE":
            self.loss_fn = nn.MSELoss(reduction="mean")
        elif settings1.get_settings("networks.loss_fn.type").lower() == "max":
            from yangke.stock.prediction.pytorch_pred_stock import MAXLoss
            self.loss_fn = MAXLoss()
        elif settings1.get_settings("networks.loss_fn.type") == "PriorLoss":
            self.loss_fn = PriorLoss(self.x_title, self.net)
            self.loss_fn.add_knowledge(settings1.get_settings("networks.loss_fn.bak_info"))
        elif settings1.get_settings("networks.loss_fn.type") == "CrossEntropy":
            self.loss_fn = nn.CrossEntropyLoss()
        elif settings1.get_settings("networks.loss_fn.type") == "BCE":
            self.loss_fn = nn.BCELoss()
        elif settings1.get_settings("networks.loss_fn.type") == "CTC":
            self.loss_fn = nn.CTCLoss()
        else:
            self.loss_fn = nn.GaussianNLLLoss

    def forward(self, x):
        out = self.net(x)
        return out

    def prediction(self, x_input, is_normalized=False):
        """
        预测指定输入参数，输入参数应为未进行归一化处理的原始数据

        :param x_input: x.shape = torch.Size([batch_size, input_dim])，也可以是长度为input_dim的列表或ndarray
        :param is_normalized: x_input是否已经归一化，默认为False，则prediction会执行归一化，否则不执行归一化直接预测
        :return:
        """
        mean = self.mean
        std = self.std
        if isinstance(self.mean, pd.Series):
            mean = self.mean[self.x_title].values
        if isinstance(self.std, pd.Series):
            std = self.std[self.x_title].values

        if isinstance(x_input, pd.DataFrame):
            x_input = x_input[self.x_title].values  # df.values是一个ndarray对象
        elif isinstance(x_input, list):
            x_input = np.asarray(x_input)

        # 将x_input转换成torch.tensor类型
        if isinstance(x_input, np.ndarray):
            if not is_normalized:
                x_input = (x_input - mean) / std  # 输入数据归一化
            x_input = torch.from_numpy(x_input)
        x_input = x_input.to(torch.float32)
        self.eval()
        y = self.forward(x_input)
        if self.classify:  # 分类问题，需要找到输出中概率最大的数的索引为最终的类别
            res = torch.argmax(y, dim=1)
        else:
            res = standard_reverse(y, mean=self.mean[self.y_title], std=self.std[self.y_title])
            if isinstance(res, np.ndarray) and res.size == 1:
                res = res.item()
        return res

    def set_standard(self, mean, std, x_titles, y_titles, normal_method):
        """
        设置预测时用到的归一化数据的信息

        :param mean:
        :param std:
        :param x_titles:
        :param y_titles:
        :param normal_method:
        :return:
        """
        self.mean = mean
        self.std = std
        self.x_title = x_titles
        self.y_title = y_titles
        self.normal_method = normal_method

    def save_yk(self, path):
        checkpoint = {
            'normal_method': self.normal_method,
            'mean': self.mean,
            'std': self.std,
            'x_title': self.x_title,
            'y_title': self.y_title,
            'model_state_dict': self.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'max_err': self.max_err,
            'average_err': self.average_err,
            'settings': self.settings
        }
        torch.save(checkpoint, path)

    @staticmethod
    def load_yk(path):
        if path is None or not os.path.exists(path):
            logger.debug("神经网络模型文件不存在！")
            return None
        checkpoint = torch.load(path)
        model1 = DataFitterNet(checkpoint.get("settings"))
        model1.set_standard(checkpoint['mean'], checkpoint['std'], checkpoint['x_title'], checkpoint['y_title'],
                            checkpoint['normal_method'])
        model1.max_err = checkpoint['max_err']
        model1.average_err = checkpoint['average_err']
        model1.load_state_dict(checkpoint['model_state_dict'])
        model1.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        return model1

    def __str__(self):
        str1 = super(DataFitterNet, self).__str__()
        return str1[:-1] + "  (Optimizer): " + self.optimizer.__str__().replace("\n", "\n  ", 1).replace("\n",
                                                                                                         "\n  ") + "\n)"

    def device(self):
        return next(self.parameters()).device

    def train_loop(self, data_loader):
        size = len(data_loader.dataset)
        self.train()  # 设置神经网络为训练模式
        loss = 0
        is_tqdm = self.settings.get_settings("print.tqdm")
        if is_tqdm:
            from tqdm import tqdm
            pb = tqdm(data_loader)
        else:
            pb = data_loader
            pb.set_description = logger.info
        relative_err = 0  # 如果是分类问题，则记录的是分类错误的数据条目数量
        max_err = 0
        for batch, (x, y) in enumerate(pb):  # 这里的(x, y)是归一化后的数据
            x = x.to(self.device())
            y = y.to(self.device())
            predict = self.forward(x)

            if isinstance(self.loss_fn, PriorLoss):  # 先验知识的损失函数需要y对x的导数
                loss = self.loss_fn(predict, y, x)
            elif isinstance(self.loss_fn, nn.MSELoss):
                loss = self.loss_fn(predict, y)
            elif isinstance(self.loss_fn, nn.CrossEntropyLoss):
                loss = self.loss_fn(predict, y)
            elif isinstance(self.loss_fn, nn.CTCLoss):
                logger.error(f"暂不支持CTC损失函数")
                return
            else:
                logger.error(f"暂不支持{self.loss_fn.__class__.__name__}损失函数")

            self.optimizer.zero_grad()  # 每一次训练梯度要清零
            loss.backward()
            self.optimizer.step()

            if batch % 10 == 0:
                # loss, current = loss.parent(), batch * len(x)  # loss是Tensor对象，没有parent，使用tensor.item()取值
                loss, current = loss.item(), batch * len(x)  # loss是Tensor对象，没有parent，使用tensor.item()取值
                pb.set_description(f"loss: {loss:>7f}  [{current:>6d}/{size:>6d}-{self.y_title}]")

            if self.classify:
                relative_err += torch.sum(y.flatten() != torch.argmax(predict, dim=1))
            else:
                # 累加当前的平均误差，更新当前的最大误差
                pred = self.dataset.standard_reverse(predict)  # 预测的真实值，任何情况都可以计算
                _y = self.dataset.standard_reverse(y)  # 实际的真实值
                max_err = max(max_err, (abs(pred - _y) / abs(_y)).max())  #
                relative_err = ((pred - _y).abs() / _y.abs()).sum() + relative_err  # 所有批次总的相对误差
        if self.classify:
            relative_err = relative_err / size
            logger.debug(f"训练集测试结果：分类错误概率为{relative_err}")
        else:
            relative_err = relative_err / size  # 平均相对误差
            logger.debug(f"训练集预测结果：相对误差为{relative_err.item():>8f}，最大误差为{max_err.item():>8f}")
        return loss, (relative_err, max_err)

    def test_loop(self, data_loader):
        num_batches = len(data_loader)
        size = len(data_loader.dataset)
        test_loss = 0
        self.eval()  # 停止更新权值参数，dropout层全部激活
        relative_err = 0  # 分类问题，则为分类错误的数据条目的个数
        max_err = 0
        with torch.no_grad():  # 停止autograd模块的工作，不影响dropout和batch norm层的行为，可以和self.eval()同时使用
            for _x, _y in data_loader:
                _x = _x.to(self.device())
                _y = _y.to(self.device())
                pred = self.forward(_x)

                # 不同的损失函数，需要传入的参数不一样
                if isinstance(self.loss_fn, PriorLoss):  # 先验知识的损失函数需要y对x的导数
                    # PriorLoss不支持torch.no_grad下计算损失
                    # loss = self.loss_fn(pred, _y, _x)
                    ...
                elif isinstance(self.loss_fn, nn.MSELoss):
                    loss = self.loss_fn(pred, _y)
                    test_loss += loss.item()  # 所有批次总的损失函数值
                elif isinstance(self.loss_fn, nn.CrossEntropyLoss):
                    loss = self.loss_fn(pred, _y)
                    test_loss += loss.item()  # 所有批次总的损失函数值
                elif isinstance(self.loss_fn, nn.CTCLoss):
                    logger.error(f"暂不支持CTC损失函数")
                    return
                else:
                    logger.error(f"暂不支持{self.loss_fn.__class__.__name__}损失函数")

                if self.classify:
                    relative_err += torch.sum(_y.flatten() != torch.argmax(pred, dim=1))
                else:
                    pred = self.dataset.standard_reverse(pred)  # 预测的真实值
                    _y = self.dataset.standard_reverse(_y)  # 实际的真实值
                    # max_err = max(max_err, (abs(pred-y)/abs(y)).max(0))  # tensor.max()返回最大值,tensor.max(0)返回最大值和索引
                    max_err = max(max_err, (abs(pred - _y) / abs(_y)).max())  #
                    relative_err = ((pred - _y).abs() / _y.abs()).sum() + relative_err  # 所有批次总的相对误差

        relative_err = relative_err / size  # 平均相对误差
        if isinstance(self.loss_fn, PriorLoss):
            logger.debug(f"测试集预测结果({self.y_title[0]})")
        elif self.classify:
            logger.debug(f"测试集预测结果：分类错误的概率为：{relative_err}")
        else:
            test_loss /= num_batches  # 平均损失
            logger.debug(f"测试集预测结果({self.y_title[0]}): 平均损失为{test_loss:>8f}")
        return loss, (relative_err, max_err)

    def validate_dataset(self, dataset: DataSetFitting):
        """
        判断当前神经网络训练用的数据集和初次训练是用的数据集的归一化参数是否相同，如果不相同，则统一
        """
        if dataset is None or dataset.std_range is None:
            logger.warning(f"训练数据集为空！")
            return True

        if self.std is None and self.mean is None and self.normal_method is None:  # 第一次训练
            logger.debug("首次训练 First train......")
            self.std, self.mean, self.normal_method = dataset.std_range, dataset.mean, dataset.normal_method
            return True

        # 如果self.std不为None，则说明是在原来训练的基础上再次训练
        if dataset.std_range.equals(self.std) and \
                dataset.mean.equals(self.mean) and dataset.normal_method == self.dataset.normal_method:
            return True
        else:
            dataset.set_standard(mean=self.dataset.mean, std_range=self.dataset.std_range,
                                 normal_method=self.dataset.normal_method)
            logger.warning(
                "新数据集与之前训练时使用的数据集的归一化参数不同，这会导致预测结果错误，已自动使用之前训练的归一化参数")
            return False

    def start_train(self, dataset: DataSetFitting, writer=None):
        """
        开始模型训练，多次训练，需要保证dataset数据集中关于归一化的参数（包括归一化方法，数据平均值，标准差等）完全相同，否则会出错。

        :param dataset: DataSetFitting类的对象
        :param writer: tensorboard的记录器
        :return:
        """
        relative_err = []  # 预测结果的相对误差
        if writer is None:
            writer = SummaryWriter(f'./runs')  # 可视化数据存放在这个文件夹
        self.dataset = dataset  # 将传入的dataset设置为神经网络的数据集，该数据集中保存了归一化的参数信息
        self.validate_dataset(dataset)

        writer.add_graph(self, torch.rand([1, self.in_num], device=self.device()))
        train_set, test_set = dataset.split_set()
        train_loader = DataLoader(dataset=train_set, batch_size=self.batch_size, shuffle=True)
        test_loader = DataLoader(dataset=test_set, batch_size=self.batch_size, shuffle=True)
        for t in range(self.epochs):
            logger.debug(f"-------------------------Epoch {t + 1}-------------------------------")
            train_loss, train_err = self.train_loop(train_loader)
            test_loss, (test_relative_err, test_max_err) = self.test_loop(test_loader)
            relative_err.append(test_relative_err)
            if self.classify:
                logger.debug(f"交叉熵损失为：{test_loss:>8f}，分类错误的概率为：{test_relative_err:>8f}")
            else:
                logger.debug(f"平均相对误差为：{test_relative_err:>8f}，最大相对误差为{test_max_err.item():>8f}")
            # ------------------------- 损失曲线图 ---------------------------------
            writer.add_scalar('train/损失', train_loss, t)
            writer.add_scalar('test/平均误差', test_relative_err, t)
            if not self.classify:
                writer.add_scalar('test/最大误差', test_max_err, t)
            # ------------------------- 损失曲线图 ---------------------------------
            # ------------------------- 权重直方图 ---------------------------------
            for i, (name, param) in enumerate(self.named_parameters()):
                if 'bn' not in name:
                    writer.add_histogram(name + "_data", param, t)
                    writer.add_histogram(name + "_grad", param.grad, t)
            # ------------------------- 权重直方图 ---------------------------------
            try:
                if test_relative_err < 0.002 and test_max_err < 0.01:
                    self.max_err = test_max_err
                    self.average_err = test_relative_err
                    break
            except IndexError:  # 当relative_err列表长度小于3时，会报IndexError错误，此处忽略错误继续训练
                pass
            self.max_err = test_max_err
            self.average_err = test_relative_err
            if self.trial is not None:
                self.trial.report(self.average_err, t)
                if self.trial.should_prune():
                    raise optuna.TrialPruned
        logger.debug(f"测试集预测结果的相对误差随epoch的变化为：{[x.item() for x in relative_err]}")
        writer.close()
        logger.debug("\n神经网络训练完成。")
        return self.average_err, self.max_err

    def get_para_type(self, p):
        if isinstance(p, list):
            result = "int"
            for p_ in p:
                if self.get_para_type(p_) == "float":
                    result = "float"
                elif self.get_para_type(p_) == "str":
                    result = "str"
            return result
        else:
            if str(p).strip().isnumeric():  # 小数的isnumeric()方法返回的是false
                return "int"
            else:
                try:
                    _ = eval(p)
                    return "float"
                except NameError:
                    return "str"

    def get_para_of_optuna_str(self, string, name):
        """
        处理设置项中的Optuna优化项，当设置项的值以Optuna开头时，则自动返回Optuna的采样值。如果不是以Optuna开头的变量，则返回原始值

        :param string: 设置项的值
        :param name: 变量名，不影响返回值，但是Optuna工具根据该值识别是哪个变量的采样值，从而给出采样值
        :return:
        """
        result = 0
        if str(string).startswith("optuna"):
            p1 = string.replace("optuna(", "").replace(")", "")
            if "[" not in p1:
                p_list = p1.split(",")
                type1 = self.get_para_type(p_list)
                if type1 == "float":
                    step = None if len(p_list) == 2 else float(p_list[2])
                    result = self.trial.suggest_float(name, float(p_list[0]), float(p_list[1]), step=step)
                elif type1 == "int":
                    step = None if len(p_list) == 2 else int(p_list[2])
                    result = self.trial.suggest_int(name, int(p_list[0]), int(p_list[1]), step=step)
            else:
                p_list = eval(p1)
                result = self.trial.suggest_categorical(name, p_list)
        else:
            result = string
        return result


class OptunaModel:
    def __init__(self, settings=None):
        if settings is None:
            settings = YkDict({})
        self.settings = copy.deepcopy(settings)
        self.settings["networks"] = copy.deepcopy(settings.get_settings("optuna.networks"))
        self.n_trials = int(settings.get_settings("optuna.n_trials") or 10)
        self.device = 'cpu'
        self.mean = None
        self.std = None
        self.x_title = None
        self.y_title = None
        self.train_set = None
        self.test_set = None

    def optimize(self):
        study_name = "model_study20220525"
        study = optuna.create_study(study_name=study_name, direction="minimize",
                                    storage=f'sqlite:///{study_name}.db', load_if_exists=True)
        study.optimize(self.objective, n_trials=self.n_trials)
        trial = study.best_trial
        logger.debug(f"最优模型的损失为{trial.value}")
        logger.debug(f"最优模型的参数为{trial.params}")
        df = study.trials_dataframe()
        print(df)
        self.visualization(study_name)

    @staticmethod
    def visualization(study_name):
        study = optuna.create_study(study_name=study_name, direction="minimize",
                                    storage=f'sqlite:///{study_name}.db', load_if_exists=True)
        optuna.visualization.plot_contour(study).show()  # 参数的等高线图
        optuna.visualization.plot_optimization_history(study).show()  # 优化历史曲线
        optuna.visualization.plot_param_importances(study).show()  # 参数的重要性
        optuna.visualization.plot_intermediate_values(study).show()  # Trails的学习曲线
        optuna.visualization.plot_parallel_coordinate(study).show()  # 高纬度参数的关系，看不懂
        optuna.visualization.plot_slice(study).show()  # 可视化独立参数

    def start_train(self, train_set, test_set):
        self.train_set = train_set
        self.test_set = test_set
        return self.optimize()

    def objective(self, trial):
        model = DataFitterNet(self.settings, trial).to(self.device)
        model.set_standard(self.mean, self.std, self.x_title, self.y_title)
        logger.debug("try model:")
        print(model)
        loss, max_err = model.start_train(self.train_set, self.test_set)
        max_err = max_err.item() if isinstance(max_err, torch.Tensor) else max_err
        loss = loss.item() if isinstance(loss, torch.Tensor) else loss
        trial.set_user_attr('max_err', max_err)
        return loss

    def to(self, device):
        self.device = device
        return self

    def set_standard(self, mean, std, x_title, y_title, *args):
        self.mean = mean
        self.std = std
        self.x_title = x_title
        self.y_title = y_title


class NN:
    def __init__(self, x=None, y=None, dataframe=None, df_x_titles=None, df_y_title=None):
        self.x = x
        self.y = y
        self.dataframe = dataframe
        self.df_x_titles = df_x_titles
        self.df_y_title = df_y_title
        self.settings = {
            "input": df_x_titles,
            "output": df_y_title,
            "networks": {
                "train": {
                    "epochs": 20,
                    "batch_size": 32,
                    "learning_rate": 0.01,
                },
                "loss_fn": {
                    "type": "MSE",

                },
                "optimizer": {
                    "type": "adam",
                },
                "layers": [
                    {"type": "input", "cell_num": "auto"},
                    {"type": "linear", "cell_num": 64, "bias": True},
                    {"type": "relu"},
                    {"type": "linear", "cell_num": 32, "bias": True},
                    {"type": "sigmoid"},
                    {"type": "output", "cell_num": "auto"}
                ],
            },
            "save_path": "default.torch",
            "normalization_method": "z-score"
        }

        self.dataset = DataSetFitting(self.dataframe, self.df_x_titles, self.df_y_title)
        self.dataset.set_standard(normal_method=self.settings.get("normalization_method"))

    def set_batch_size(self, batch_size):
        self.settings["networks"]["train"]["batch_size"] = batch_size

    def set_learning_rate(self, lr):
        self.settings["networks"]["train"]["learning_rate"] = lr

    def set_epochs(self, epochs):
        self.settings["networks"]["train"]["epochs"] = epochs

    def train(self):
        self.net = DataFitterNet(settings1=self.settings)
        self.net.start_train(self.dataset)

    def predict(self, x):
        return self.net.prediction(x)

    def save(self, file):
        self.net.save_yk(file)

    def load(self, file):
        self.net = DataFitterNet.load_yk(file)


def train_model(settings1=None):
    """
    按照settings.yaml文件训练神经网络模型，并保存到settings.yaml指定的位置

    如果settings.networks没有定义具体的网络模型，但是settings.optuna.networks中定义了网络模型的寻优空间参数，则会自动使用
    Optuna库对模型超参数进行寻优，并将寻优结果得到的最有网络模型定义写入settings.yml文件中。再次调用该方法，则会使用寻优得到的
    网络模型架构进行数据拟合，将模型权值信息写入settings.output.save_path指定的路径中。

    如果settings.networks定义了具体的网络模型，则该方法只对定义的模型进行训练，将训练后的权值信息写入settings.output.save_path
    指定的路径中。

    如果该方法同时训练多个单输出模型，则模型架构的优化只会进行一次，即第一个模型架构的优化结果会应用于后续的多个单输出数据拟合任务。

    :return:
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"使用{device}进行计算")
    if settings1 is None:
        settings1 = get_settings()

    if settings1.get("networks") is not None:  # 如果存在networks的定义就直接使用该定义
        optimize_model = False
    elif settings1.get("optuna") is not None:  # 如果存在optuna的设置，就使用该设置获取最有网络模型定义
        optimize_model = True
    else:
        logger.error("未找到模型设置信息，请确认！")
        return
    _settings_ = copy.deepcopy(settings1)
    output = _settings_.get("output") or {}
    if output.get("type") == "single_output":
        paras = copy.deepcopy(output.get("para") or {})
        for i, para in enumerate(paras):
            output["para"] = [para]
            output["save_path"] = settings1.get_settings("output.save_path")[i]
            model = OptunaModel(_settings_).to(device) if optimize_model else DataFitterNet(_settings_).to(device)
            logger.debug(model)
            dataset_all = DataSetFitting(_settings_)  # 获取所有的数据集
            model.set_standard(dataset_all.mean, dataset_all.std_range, dataset_all.x_title, dataset_all.y_title,
                               dataset_all.normal_method)  # 将数据集的数据归一化信息添加到模型中，方便以后使用
            part1 = float(_settings_.get_settings("dataset.data_training.proportion"))
            part2 = float(_settings_.get_settings("dataset.data_test.proportion"))
            train_set, test_set = dataset_all.split_set(part1, part2)  # 均已是归一化后的数据
            model.start_train(train_set, test_set)
            if not optimize_model:
                model.save_yk(output["save_path"])
            else:
                model.update_settings_file("settings.yml")
                train_model()


def re_train(data_file, settings1=None):
    """
    在现有模型基础上再次训练，该方法对数据的归一化方法必须与初次训练时一致，因此本方法会忽略settings1中的数据归一化相关设置，而自动采用原模型中
    的数据归一化方法

    :param data_file: 数据文件,csv文件
    :param settings1: 可以直接传入settings字典，则该方法不会再从外部yaml文件读取设置信息
    :return:
    """
    device = "cuda" if torch.cuda.is_available() else "cpu"
    logger.info(f"使用{device}再次训练")
    if settings1 is None:
        settings1 = get_settings()
    _settings_ = copy.deepcopy(settings1)
    if isinstance(data_file, list):
        _data_file = []
        for file in data_file:
            _data_file.append({"name": file, "type": "csv"})
        _settings_["dataset"]["data_file"] = _data_file
    else:
        _settings_["dataset"]["data_file"] = [{"name": data_file, "type": "csv"}]
    output = _settings_.get("output") or {}
    if output.get("type") == "single_output":
        paras = copy.deepcopy(output.get("para") or {})
        for i, para in enumerate(paras):
            output["para"] = [para]
            output["save_path"] = settings1.get_settings("output.save_path")[i]
            model = DataFitterNet.load_yk(output["save_path"])
            model.epochs = _settings_.get_settings("networks.train.epochs")  # 再次训练时的epochs和初次训练时的一般不相同
            logger.debug(model)
            dataset_all = DataSetFitting(_settings_)  # 获取所有的数据集
            if _settings_.get_settings("dataset.normalization") != model.normal_method:
                logger.warning(f"再训练时数据归一化方法({_settings_.get_settings('dataset.normalization')})与"
                               f"模型初次训练时({model.normal_method})不一致，这可能导致预测结果错误")
                logger.warning(f"已强制切换为模型初次训练时使用的数据归一化方法！({model.normal_method})")
            dataset_all.set_standard(model.mean, model.std, model.normal_method)
            part1 = 0.95
            part2 = 0.05
            train_set, test_set = dataset_all.split_set(part1, part2)  # 均已是归一化后的数据
            model.start_train(train_set, test_set)

            model.save_yk(output["save_path"])


def filter_err_condition(model, data_file=None):
    """
    将model在整个数据集上进行测试，过滤小偏差的点，删选出偏差较大的点，一般后续对偏差较大的点继续学习

    :param model:
    :param data_file:
    :return:
    """
    settings = get_settings()
    if data_file is not None:
        settings["dataset"]["data_file"] = [{"name": data_file, "type": "csv"}]
    _settings_ = copy.deepcopy(settings)
    dataset_all = DataSetFitting(_settings_)
    dataset_all.set_standard(model.mean, model.std_range)


def setup_seed(seed=10):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    np.random.seed(seed)
    random.seed(seed)


def test():
    model = DataFitterNet.load_yk(r"D:\lengduan\data\model_p2.dat")
    args = {
        "power": 400,
        "flow_heat": 0,
        "p_env": 98,
        "t_env": 30,
        "humid": 0.60,
        "p_gas": 3.8,
        "t_gas": 18,
        "flow_fgh": 40,
        "flow_tca": 100,
        "flow_oh": 3,
        "flow_rh": 0
    }
    x = [v for k, v in args.items()]
    pump, fun = 2, 3
    x.extend([pump, fun])
    p = model.prediction(x)
    print(p)


def deal_settings_path(settings, **kwargs):
    """
    当settings.yaml文件中使用了带变量的路径时，如"E:/热工院//retrain{unit}_0.csv",
    本方法将变量{unit}替换为指定的变量。

    :param settings:
    :return:
    """
    files = []

    for data_file in settings.get_settings("dataset.data_file"):
        pth = data_file["name"].replace(r"{unit}", "1")
        type1 = data_file["type"]
        files.append({"name": pth, "type": type1})
    settings["dataset"]["data_file"] = files
    return settings


if __name__ == "__main__":
    # setup_seed()
    # OptunaModel(None).visualization("model_study20220525")
    # settings1 = get_settings()
    # deal_settings_path(settings1)
    # train_model(settings1)
    # # settings["output"]["save_path"] = [r"D:\lengduan\data\model_p1.dat"]
    # # settings["output"]["para"] = ["背压"]
    # re_train(data_file=[
    #     r"D:\lengduan\data\retrain1_0.csv",
    #     r"D:\lengduan\data\retrain1_1.csv",
    #     r"D:\lengduan\data\retrain1_7.csv",
    #     r"D:\lengduan\data\retrain1_9.csv",
    #     r"D:\lengduan\data\retrain1_10.csv",
    #     r"D:\lengduan\data\retrain1_11.csv",
    # ], settings1=settings_1)
    # re_train(data_file=[
    #     r"D:\lengduan\data\retrain2_0.csv",
    #     r"D:\lengduan\data\retrain2_1.csv",
    #     r"D:\lengduan\data\retrain2_7.csv",
    #     r"D:\lengduan\data\retrain2_8.csv",
    #     r"D:\lengduan\data\retrain2_9.csv",
    #     r"D:\lengduan\data\retrain2_10.csv",
    #     r"D:\lengduan\data\retrain2_11.csv",
    # ], settings1=settings_1)

    import torch
    import torch.autograd

    x = torch.tensor([2.0], requires_grad=True)
    y = x ** 3

    y.backward(retain_graph=True)
    y.backward(retain_graph=True)
    y.backward()  # 反向传播,求解导数，即y对x求导
    print("x.grad = ", x.grad)
