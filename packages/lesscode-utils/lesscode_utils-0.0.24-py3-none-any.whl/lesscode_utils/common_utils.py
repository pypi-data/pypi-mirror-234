import logging
from functools import reduce
from itertools import groupby
from typing import List, Dict, Union


def list_dict_group(data: List[Dict], key):
    """
    列表字典去重
    :param data: 数据
    :param key: 去重的key
    :return:
    """
    new_data = {"list_data": list(), "dict_data": dict()}
    data.sort(key=lambda x: x.get(key, ""))
    group_data = groupby(data, key=lambda x: x.get(key, ""))
    for data_key, values in group_data:
        _values = list(values)
        new_data["list_data"].append({"key": data_key, "values": _values})
        new_data["dict_data"].update({data_key: _values})

    return new_data


def remove_list_dict_duplicate(list_dict_data):
    """
    去除列表字典里的重复数据
    :param list_dict_data: 列表字典
    :return:
    """
    return reduce(lambda x, y: x if y in x else x + [y], [[], ] + list_dict_data)


def retry(func, params: Union[dict, list, tuple], check_func, num=1):
    """
    执行失败重试
    :param func: 要执行的函数
    :param params: 要执行的函数的参数值
    :param check_func: 校验函数
    :param num: 重试次数
    :return:
    """
    result = None
    for i in range(num):
        try:
            if params:
                if isinstance(params, dict):
                    result = func(**params)
                elif isinstance(params, list) or isinstance(params, tuple):
                    result = func(*params)
                else:
                    break
            else:
                result = func()
            flag = check_func(result)
            if flag:
                break
        except Exception as e:
            logging.error(f"error={e}")
    return result


def check_value(value, default):
    if not value:
        value = default
    return value


def fill(value, length, char: str, position="font"):
    value = str(value)
    value_len = len(value)
    if len(value) < length:
        if position == "font":
            value = char * (length - value_len) + value
        else:
            value = value + char * (length - value_len)
    return value


def check_or_add_growth_rate(data: List[dict], value_key: str, growth_rate_key: str = "growth_rate",
                             start_growth_rate: float = None, pre_value: Union[int, float] = None, flag: bool = True,
                             digits: int = None):
    """
    检查或添加增长率字段
    :param data: 数据
    :param value_key: 数据的key
    :param growth_rate_key: 增长率的key
    :param start_growth_rate: 起始增长率
    :param pre_value: 前一个数据
    :param flag: 是否乘100
    :param digits: 小数点位数
    :return:
    """
    for i, _ in enumerate(data):
        if not _.get(growth_rate_key) and value_key in _:
            if i == 0:
                if start_growth_rate:
                    if flag:
                        start_growth_rate = start_growth_rate * 100
                    if digits:
                        start_growth_rate = round(start_growth_rate, digits)
                    data[i][growth_rate_key] = start_growth_rate
                else:
                    if pre_value:
                        current = check_value(data[i].get(value_key, 0), 0) if data[i].get(value_key, 0) else 0
                        value = float(current - pre_value) / pre_value if pre_value else 0
                    else:
                        value = 0
                    if flag:
                        value = value * 100
                    if digits:
                        value = round(value, digits)
                    data[i][growth_rate_key] = value
            else:
                pre = check_value(data[i - 1].get(value_key, 0), 0) if data[i - 1].get(value_key, 0) else 0
                current = check_value(data[i].get(value_key, 0), 0) if data[i].get(value_key, 0) else 0
                value = float(current - pre) / pre if pre else 0
                if flag:
                    value = value * 100
                if digits:
                    value = round(value, digits)
                data[i][growth_rate_key] = value
