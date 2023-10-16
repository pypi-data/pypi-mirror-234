from collections import OrderedDict
from copy import deepcopy
from typing import List

"""
柱状图/直方图/折线图
"""


class HistogramChart:
    @staticmethod
    def format_data(data, data_key="", name_key="", unit="", name="", default="", value_func=None):
        return {"data": data, "data_key": data_key, "name_key": name_key, "unit": unit,
                "name": name,
                "default": default, "value_func": value_func}

    @staticmethod
    def list2single_histogram(data: List[dict], title: str = "", unit: str = "",
                              x_name: str = "", y_name: str = None, x_key="key", y_key="value", **kwargs):
        """
        单柱状图
        :param y_key:
        :param x_key:
        :param data: 数据，示例：[{"key":"2020","value":10}]
        :param title: 图题
        :param unit: 数据单位
        :param x_name: x轴名称
        :param y_name: y轴名称
        :param kwargs: 额外数据，放在pool里
        :return:
        """
        x = []
        y = []
        for item in data:
            x.append(item.get(x_key))
            y.append(item.get(y_key))
        result = {
            "xName": x_name,
            "yName": y_name,
            "title": title,
            "x": x,
            "series": [
                {
                    "name": title,
                    "data": y,
                    "unit": unit
                }
            ]
        }
        if kwargs:
            result["pool"] = kwargs

        return result

    @staticmethod
    def list2more_histogram(data: List[dict], title: str = "", unit: str = "",
                            x_name: str = "", y_name: str = None, x_key="key", y_key="value", **kwargs):
        """
        多柱状图
        :param y_key:
        :param x_key:
        :param data: 数据，示例：[{"key":"2020","value":[10]}]
        :param title: 图题
        :param unit: 数据单位
        :param x_name: x轴名称
        :param y_name: y轴名称
        :param kwargs: 额外数据，放在pool里
        :return:
        """
        x = []
        y = []
        for item in data:
            x.append(item.get(x_key))
            y.append(item.get(y_key))
        result = {
            "xName": x_name,
            "yName": y_name,
            "title": title,
            "x": x,
            "series": [
                {
                    "name": title,
                    "data": y,
                    "unit": unit
                }
            ]
        }
        if kwargs:
            result["pool"] = kwargs

        return result

    @staticmethod
    def list2histogram(data: List[dict], title: str = "",
                       x_name: str = "", y_name: str = None, x_index: int = 0, x_func=None, **kwargs):
        """
        单/多柱状图
        :param x_func:
        :param x_index:
        :param data: [{"data":{"2020":200},"data_key":"","unit":"","name":"","default":""}] 或者
                     [{"data":{"2020":{"count":200}}, "data_key":"value","unit":"","name":"","default":""}] 或者
                     [{"data":[{"year":"2020","value":200}], "data_key":"value","name_key":"year","unit":"","name":"",
                       "default":"","value_func":None}]
        :param title:
        :param x_name:
        :param y_name:
        :param kwargs:
        :return:
        """
        result = {
            "xName": x_name,
            "yName": y_name,
            "title": title,
            "x": [],
            "series": []
        }
        if data:
            choose_data = data[x_index].get("data")
            x = []
            if choose_data:
                if isinstance(choose_data, dict) or isinstance(choose_data, OrderedDict):
                    x = list(data[x_index].get("data", {}).keys())
                elif isinstance(choose_data, list):
                    name_key = data[x_index].get("name_key", "name")
                    x = [_.get(name_key) for _ in choose_data]
            if x_func:
                x = x_func(x)
            result["x"] = x
            series = []
            for _ in data:
                tmp = []
                data_key = _.get("data_key")
                unit = _.get("unit")
                name = _.get("name")
                default = _.get("default", 0)
                _data = _.get("data")
                name_key = _.get("name_key", "name")
                value_func = _.get("value_func")
                chart_type = _.get("type", "line")
                if isinstance(_data, list):
                    _data = {v.get(name_key): v.get(data_key, default) for v in _data}
                if isinstance(_data, dict):
                    for i in x:
                        _value = _data.get(i)
                        if isinstance(_value, dict):
                            _value = _value.get(data_key, default)
                        if not _value:
                            _value = default
                        if value_func:
                            _value = value_func(_value)
                        tmp.append(_value)
                    series.append({"name": name, "unit": unit, "type": chart_type, "data": tmp})
            result["series"] = series
        if kwargs:
            result["pool"] = kwargs

        return result

    @staticmethod
    def bar_chart(data: dict, detail_list: list):
        """
        字典转多柱
        :param data: {"INB1335":{"count":1,"sum":10}}
        :param detail_list: [{"name":"计数","unit":"个","data_key":"count","func":int},
                             {"name":"求和","unit":"万","data_key":"sum","func":lambda x:x/10000}   ]
        :return:
        """
        result = {"x": [], "series": detail_list}
        for detail in detail_list:
            detail["data"] = []
        for k, v in data.items():
            result.get("x").append(k)
            for index, item in enumerate(detail_list):
                data_key_list = item.get("data_key", "count").split("&")
                value: dict = deepcopy(v)
                for data_key in data_key_list:
                    # 若为int，只可能为0，不会在get处报错
                    value = value.get(data_key, 0) if value else 0
                if item.get("func"):
                    func = item.get("func")
                    item["data"].append(func(value))
                else:
                    item["data"].append(value)
        for item in detail_list:
            item.pop("func", None)
            item.pop("data_key", None)
        if not result.get("x"):
            result["series"] = []
        return result
