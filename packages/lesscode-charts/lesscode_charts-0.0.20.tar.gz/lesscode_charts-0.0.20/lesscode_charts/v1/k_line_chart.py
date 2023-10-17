from typing import List, Any

"""
K线图
"""


class KLineChart:
    @staticmethod
    def k_line(data: List[Any], x: List[Any], y: List[Any], unit: str = "",
               title: str = "", x_name: str = "", y_name: str = ""):
        """
        :param data: 数据，以为数组或者多维数组
        :param x: x轴数据
        :param y: y轴数据
        :param unit: 数据单位
        :param title: 图题
        :param x_name: x轴名字
        :param y_name: y轴名字
        :return:
        """

        result = {
            "xName": x_name,
            "yName": y_name,
            "x": x,
            "y": y,
            "series": [
                {
                    "name": title,
                    "data": data,
                    "unit": unit
                }
            ],
        }

        return result
