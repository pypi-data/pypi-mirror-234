"""
# File       : 金融K线_AI数据预处理.py
# Time       ：2023/9/30 19:04
# Author     ：xuewei zhang
# Email      ：jingmu_predict@qq.com
# version    ：python 3.10
# Description：
"""
from typing import Literal
from datetime import timedelta, datetime
import numpy as np
import pandas as pd
import torch
from typing import List, Tuple, Union

from serial_data_handler_zxw import 时间列_三角函数化, 生成训练数据_避开时间断点

# 开盘时间戳,开盘价,最高价,最低价,收盘价,成交量,收盘时间戳,报价币成交量,成单数,吃单方买入的基础币数量,吃单方买入的报价币数量,收盘时间
金融K线_数据头 = {"开盘时间戳": "int64", "开盘价": "float64", "最高价": "float64", "最低价": "float64",
                  "收盘价": "float64", "成交量": "float64", "收盘时间戳": "int64",
                  "报价币成交量": "float64", "成单数": "float64", "吃单方买入的基础币数量": "float64",
                  "吃单方买入的报价币数量": "float64", "收盘时间": "datetime64[ns]"}


class 金融K线_AI数据预处理:
    dtype: str = "float64"  # 数据类型
    mean: pd.Series = None  # 均值
    std: pd.Series = None  # 标准差
    pd原始数据: pd.DataFrame = None  # 原始数据
    索引_训练集: List[Tuple[int, int, int, int]] = None  # 索引_训练集
    索引_测试集: List[Tuple[int, int, int, int]] = None  # 索引_测试集
    索引_训练与测试集: List[Tuple[int, int, int, int]] = None  # 索引_训练与测试集

    def __init__(self, csv_path, 模型input长度: int, 模型output长度: int, 训练测试集比例=0.8, dtype='float64'):
        """
        the columns of csv file are:开盘价	最高价	最低价	收盘价	成交量	报价币成交量	成单数	吃单方买入的基础币数量	吃单方买入的报价币数量	收盘时间
        """
        # 1. 读取并简单处理原始数据
        self.dtype = dtype
        data = pd.read_csv(csv_path, dtype={"开盘价": dtype, "最高价": dtype, "最低价": dtype,
                                            "收盘价": dtype, "成交量": dtype, "报价币成交量": dtype, "成单数": dtype,
                                            "吃单方买入的基础币数量": dtype, "吃单方买入的报价币数量": dtype})
        # to datetime
        data['收盘时间'] = pd.to_datetime(data['收盘时间'])

        # drop part of columns if it exits
        data.drop(columns=['开盘时间戳', '收盘时间戳'], inplace=True)

        # 2. 保存原始数据
        self.pd原始数据 = data

        # 3. 计算Z-Score参数
        self.计算Z_Score参数()

        # 4. 获取 训练数据与测试 数据索引
        self.索引_训练与测试集 = 生成训练数据_避开时间断点(
            data, '收盘时间', timedelta(minutes=2)
        ).数据划分_避开断点(模型input长度, 模型output长度, step=1)
        #
        self.训练测试集比例 = 训练测试集比例
        self.__划分训练集和测试集()
        #

    @staticmethod
    def help():
        说明 = """
        1. 表头严格按照以下关键字命名和排列:
        [开盘时间戳, 开盘价, 最高价, 最低价, 收盘价, 成交量, 收盘时间戳, 报价币成交量, 成单数, 吃单方买入的基础币数量, 吃单方买入的报价币数量, 收盘时间]

        2. 数据类型严格按照以下类型:
        [int64, float64, float64, float64, float64, float64, int64, float64, float64, float64, float64, datetime64[ns]]
        """
        print(说明)

    def dataset__get_item__(self, i: int, data: pd.DataFrame, 是训练集=True) -> Tuple[pd.DataFrame, pd.DataFrame]:
        return self.get_训练or测试数据(i, data, 是训练集)

    def dataset__len__(self, 是训练集=True):
        if 是训练集:
            return len(self.索引_训练集)
        else:
            return len(self.索引_测试集)

    def get_训练or测试数据(self, i: int, data: pd.DataFrame, 是训练集=True) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        :param i:
        :param data: pd.DataFrame , 用于指定是标准化后的数据 还是 原始数据
        :param 是训练集:
        :return: (input, output)
        """
        if 是训练集:
            _索引 = self.索引_训练集
        else:
            _索引 = self.索引_测试集
        #
        if _索引 is None:
            self.__划分训练集和测试集()
        #
        if i >= len(self.索引_训练集):
            raise Exception(f"索引越界, {i=}, {len(_索引)=}")
        #
        return data.iloc[_索引[i][0]:_索引[i][1], :], \
            data.iloc[_索引[i][2]:_索引[i][3], :]

    def __划分训练集和测试集(self):
        训练测试集比例 = self.训练测试集比例
        训练集长度 = int(len(self.索引_训练与测试集) * 训练测试集比例)
        self.索引_训练集 = self.索引_训练与测试集[:训练集长度]
        self.索引_测试集 = self.索引_训练与测试集[训练集长度:]

    @staticmethod
    def 排序_数据column顺序(data: pd.DataFrame, columns输出顺序: List[str] = None) -> pd.DataFrame:
        if columns输出顺序 is None:
            columns = ['收盘时间', '开盘价', '最高价', '最低价', '收盘价', '成交量', '报价币成交量', '成单数',
                       '吃单方买入的基础币数量', '吃单方买入的报价币数量']
        else:
            columns = columns输出顺序
        df = data[columns]
        return df

    def 计算Z_Score参数(self):
        self.mean = self.pd原始数据.mean()
        self.std = self.pd原始数据.std()
        # 丢弃时间列
        self.mean.drop(labels=['收盘时间'], inplace=True)
        self.std.drop(labels=['收盘时间'], inplace=True)
        print(f"数据z-score正则参数: \n{self.mean=}\n{self.std=}")

    def 标准化(
            self, data: pd.DataFrame,
            日期起点=datetime(2019, 1, 1, 0, 0, 0),
            时间周期=timedelta(days=1)
    ) -> pd.DataFrame:

        # 丢弃时间列 - mean和std变量中不包含时间列
        data_normalize = data.drop(labels=['收盘时间'], axis=1)
        # 标准化
        data_normalize = (data_normalize - self.mean) / self.std
        # 添加时间列, 时间列按天进行sin处理
        data_normalize['收盘时间'] = 时间列_三角函数化(data['收盘时间'],
                                                       起始日期=日期起点,
                                                       周期=时间周期)
        #
        return data_normalize

    def 收盘价_标准化(self, x: Union[torch.Tensor, np.ndarray, float, int]):
        return (x - self.mean["收盘价"]) / self.std["收盘价"]

    def 收盘价_逆标准化(self, x: Union[torch.Tensor, np.ndarray, float, int]):
        return x * self.std["收盘价"] + self.mean["收盘价"]

    def pd转tf(self, pd_data: pd.DataFrame, columns输出顺序: List[str] = None,
               dtype: Literal['float32', 'float64', None] = None) -> torch.Tensor:
        """
        将pd.DataFrame转换为tf.Tensor
        """
        # 按顺序排序
        pd_data = self.排序_数据column顺序(pd_data, columns输出顺序)
        # dtype
        if dtype is None:
            dtype = self.dtype

        # 转化数据
        if dtype == 'float64':
            tmp = pd_data.to_numpy().astype(np.float64)
            return torch.tensor(tmp, dtype=torch.float64)
        elif dtype == 'float32':
            tmp = pd_data.to_numpy().astype(np.float32)
            return torch.tensor(tmp, dtype=torch.float32)
        else:
            raise Exception(f"执行pd转tf失败, 不支持的数据类型, {pd_data.head()=},{self.dtype=}")


def 准确率_one_hot(outputs_one_hot: torch.Tensor, labels: torch.Tensor = None, labels_one_hot: torch.Tensor = None):
    """
    :param outputs_one_hot: [[0.8,0.1,0.05,0.02,0.03], ... ]
    :param labels: [类别,... ]
    :param labels_one_hot: [[1,0,0,0,0],... ]
    :return:
    """
    if labels is None and labels_one_hot is None:
        raise Exception("labels和labels_one_hot不能同时为空")
    if labels_one_hot and not labels:
        labels = torch.argmax(labels_one_hot, dim=-1)

    # outputs_one_hot = torch.randn(32, 100, 7)  # 仅作为示例，你应该使用你的模型输出替换它 [32batchs数据, 100个时间步, 7个类别]
    # labels_one_hot = torch.randint(0, 7, (32, 100))  # 仅作为示例，你应该使用你的真实标签替换它 [32batchs数据, 100个时间步]

    # 使用 argmax 获取最可能的类别
    predicted_labels = torch.argmax(outputs_one_hot, dim=-1)

    # 检查预测是否正确
    correct_predictions = (predicted_labels == labels)

    # 计算准确率
    accuracy = correct_predictions.float().mean().item()
    # print(f'One-hot accuracy: {accuracy * 100:.2f}%')
    return accuracy


def cal_非贪心收益率_one_hot(outputs_one_hot: torch.Tensor, labels: torch.Tensor):
    # 只要预测种类小于等于真实种类, 就认为预测正确
    predicted_labels = torch.argmax(outputs_one_hot, dim=-1)
    # 检查预测是否正确
    correct_predictions = (predicted_labels <= labels)
    # 计算准确率
    accuracy = correct_predictions.float().mean().item()
    return accuracy


if __name__ == '__main__':
    csv_file = "/Volumes/AI_1505056/量化交易/币安_K线数据/BTCUSDT-1m-201909-202308.csv"
    x = 金融K线_AI数据预处理(csv_file, 100, 100)
    xn = x.标准化(x.pd原始数据)
    xn.to_csv("/Volumes/AI_1505056/量化交易/币安_K线数据/BTCUSDT-1m-201909-202308_normalize.csv", index=False)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    print(x.pd原始数据.head())
    print(xn.head())
