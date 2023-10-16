import copy

from yangke.common.config import logger
from yangke.ebsilon.constant.constant import (Pressure, Temperature, MassFlow, Power, Density, Enthalpy, Unit, Area,
                                              Length, VolumeFlow, SpecificVolume, One, AngleUnit)


class Values:
    def __init__(self, values=None, values_steps=None):
        """
        设备组件的参数对象，维护两个参数字典，其中values字典代表直接的设置值，而result字典代表中间计算数值及计算结果。
        但values和result中的参数可能有重叠，如焓值既可以直接设置，也可以间接计算。

        :param values:
        :param result:
        """
        self.values_steps = values_steps or {0: {}}  # 按迭代步数保存的参数数据，元素是字典类型
        self.values = values or {}  # 字典类型

    def append_values(self, values):
        """
        在迭代部的末尾添加新的数据

        :param values:
        :return:
        """
        self.values = values
        k = len(self.values_steps)
        self.values_steps[k] = copy.deepcopy(self.values)

    def set_values(self, step, values: "dict | Values", set_none=False):
        """
        设置某个迭代步的值

        如果设置的是单个的值，且set_none=False，则相当于是更新某个时间步的某个值，即
        self.set_values(values={"P": Value(1, "MPa")}, step=1)
        和
        self.update(values={"P": Value(1, "MPa")}, set_none=False, step=1)
        效果相同。
        但当set_none为True，这两个方法的效果有区别。set_values会删除values中没有的参数，而update方法不会删除

        :param set_none: 是否用空值覆盖已有值，如果为True，则当前时间步的所有数据都会替换为values，values中没有的参数会被删除
        :param step:
        :param values:
        :return:
        """
        if isinstance(values, Values):
            values = values.get_values_of_step(step=step)
        if step is None:  # 如果未指定时间步，则默认取最后一个已有的时间步
            step = len(self.values_steps) - 1
        if self.values_steps.get(step) is None:  # 如果当前时间步没数据，则初始化为空字典
            self.values_steps[step] = {}

        if set_none:
            self.values_steps[step] = copy.deepcopy(values)  # 无论当前时间步是否有数据，都直接使用传入值覆盖当前值
        else:
            filter_values = self.get_non_null_values(values)
            self.values_steps[step].update(filter_values)

        if step == len(self.values_steps) - 1:  # 如果设置的是最后一个时间步的值，则更新self.values
            self.values = copy.deepcopy(self.values_steps[step])

    def update(self, values: dict, set_none=False, step: int | None = None):
        """
        更新数据，如果step为None，则更新当前迭代步的数据，不会增加新的迭代步，由面板至后台数据更新时，step没有设置
        如果指定了step，则更新指定迭代步的数据

        :param values:
        :param set_none: 是否用空值覆盖已有值，如果为True，则指定参数的值会被values中的空值替换，values中不包含的值不受影响
        :param step: 迭代步
        :return:
        """
        if isinstance(values, Values):
            values = values.get_values_of_step(step=step)
        if step is None:  # 如果未指定时间步，则默认取最后一个已有的时间步
            step = len(self.values_steps) - 1
        if self.values_steps.get(step) is None:  # 如果当前时间步没数据，则初始化为空字典
            self.values_steps[step] = {}

        if set_none:
            self.values_steps[step].update(values)
        else:
            _val = self.get_non_null_values(values)
            self.values_steps[step].update(_val)

        if step == len(self.values_steps) - 1:  # 如果更新的是最后一个时间步的值，则更新self.values
            self.values = copy.deepcopy(self.values_steps[step])

    def clear_result(self):
        # 清除初始状态以后的其他结果
        # 时间步0只保存画面写入的数据，计算结果永远不要写入时间步0
        if len(self.values_steps) > 1:
            self.values_steps = {0: self.values_steps.get(0)}
            self.values = self.values_steps.get(0)

    def _get_symbol(self, _val, need_unit=False):
        """
        获取某个变量的值，根据neet_unit返回相应的值
        """
        if _val.__class__.__name__ in ["float", "int", "str"]:
            if str(_val).strip() != "":  # 如果_val是非空字符串
                res = Value(_val, None) if need_unit else _val
            else:
                res = None  # 没有单位信息，则忽略need_unit参数
        elif isinstance(_val, Value):
            res = _val
        else:  # 其他未知类型，直接返回
            res = _val

        # 至此，res可能是None或Value()
        if need_unit:
            return res
        else:
            if res is None:
                return res
            elif isinstance(res, Value):
                return res.value
            else:
                return res

    def get(self, symbol, need_unit=False):
        """
        获取当前迭代步组件属性的值

        :param symbol: 参数的符号
        :param need_unit: 获取单位为unit的组件属性值
        :return:
        """
        _val = self.values.get(symbol)
        if _val is None:
            return None
        elif _val.__class__.__name__ in ["float", "int", "str"]:
            return Value(_val) if need_unit else _val
        else:
            return _val if need_unit else _val.value

    @staticmethod
    def get_non_null_values(_val):
        if _val is None:
            return {}
        filter_values = {}
        for k, v in _val.items():
            if isinstance(v, Value):
                if str(v.value).strip() != "":
                    filter_values.update({k: v})
            else:
                if v is None:
                    ...
                elif str(v).strip() != "":
                    filter_values.update({k: v})
        return filter_values

    def get_initial(self, symbol=None, need_unit=False, with_none=True):
        """
        获取初始状态下的参数值

        :param symbol: 获取指定的参数
        :param need_unit: 是否返回单位
        :param with_none: 是否返回空值
        :return:
        """
        if symbol is None:  # 获取全部参数时，忽略need_unit参数
            _val = self.values_steps.get(0)
            if with_none:  # 如果需要返回空值
                res = _val
            else:  # 不需要返回空值，则逐个判断并过滤空值
                res = self.get_non_null_values(_val)
            return res
        elif len(self.values_steps) > 0:
            _val = self.values_steps.get(0).get(symbol)
            res = self._get_symbol(_val, need_unit)
            return res
        else:
            return None

    def get_values_of_step(self, step, symbol=None, need_unit=False, with_none=True):
        """
        获取指定时间步的参数值

        :param step: 时间步
        :param symbol: 获取指定的参数
        :param need_unit: 是否返回单位
        :param with_none: 是否返回空值
        :return:
        """
        if symbol is None:  # 获取全部参数时，忽略need_unit参数
            _val = self.values_steps.get(step)
            if with_none:  # 如果需要返回空值
                res = _val
            else:  # 不需要返回空值，则逐个判断并过滤空值
                res = self.get_non_null_values(_val)
            return res
        else:
            _vals = self.values_steps.get(step)
            if _vals is None:
                return None
            else:
                _val = _vals.get(symbol)
            res = self._get_symbol(_val, need_unit)
            return res

    def get_results(self, symbol=None, need_unit=False):
        """
        获取数据中的结果数据

        :param symbol:
        :param need_unit:
        :return:
        """
        if symbol is None:  # 获取全部参数时，忽略need_unit参数
            if len(self.values_steps) > 0:
                _val = self.values_steps[len(self.values_steps) - 1]
                return _val
        else:
            if len(self.values_steps) > 0:
                _val = self.values_steps[len(self.values_steps) - 1].get(symbol)
                res = self._get_symbol(_val, symbol, need_unit)
                return res
            else:
                return None


class Value:
    def __init__(self, val='', unit=None):
        self.derived = False  # 是否是间接计算参数

        try:
            self.value = float(val)  # 将参数的值尽量转换为float类型，以方便计算
        except:
            self.value = val  # 有些值无法转换，因为表示类型的参数可能是字符串
        if unit is None:
            ...
        elif isinstance(unit, str):
            for cls in [Pressure, Temperature, MassFlow, Power, Density, Enthalpy,
                        VolumeFlow, SpecificVolume, AngleUnit, One]:
                if cls().allowed_values is None:
                    logger.debug(f"{cls}的允许单位为空")
                if unit in cls().allowed_values:
                    unit = cls(unit)
                    break
        self.unit: Unit = unit

    def __str__(self):
        return f"{self.value} {self.unit}"

    def get_default_value(self) -> float | str:
        """
        获取默认单位下的值
        """
        try:
            value = float(self.value)
            return value
        except ValueError:
            return self.value  # 也存在一些不是数值型的值，如计算类型等

    def get_value_with_unit(self, unit_str):
        """
        获取指定单位的参数的值

        :param unit_str:
        :return:
        """
        if isinstance(self.unit, Unit):
            try:
                self.value = float(self.value)
            except:
                pass
            return self.unit.transfer_to_unit(self.value, unit_str)
        else:
            return self.value
