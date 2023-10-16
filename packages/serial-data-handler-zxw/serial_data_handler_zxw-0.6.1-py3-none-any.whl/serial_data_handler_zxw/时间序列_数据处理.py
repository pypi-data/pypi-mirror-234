"""
# File       : 时间序列_数据处理.py
# Time       ：2023/9/25 17:00
# Author     ：xuewei zhang
# Email      ：jingmu_predict@qq.com
# version    ：python 3.8
# Description：
1. 根据传入的数据,生成训练数据,并保证训练数据的连续性
1. Generate training pd原始数据 based on the incoming pd原始数据, and ensure the continuity of the training pd原始数据

# Attention:
传入的数据必须指定时间列(或其他顺序列)
You must specify the time column (or other sequential column) of the incoming pd原始数据
传入的数据必须已按顺序排列好
The incoming pd原始数据 must be sorted in order
"""
import numpy as np
import pandas as pd
from tqdm import tqdm
from datetime import timedelta, datetime

from typing import List, Tuple


class 生成训练数据_避开时间断点:
    断点: np.ndarray  # 断点序号,即数据连续位置的最后一行行号

    def __init__(self, data: pd.DataFrame, column_timestamp='timestamp', gap=timedelta(minutes=2)):
        self.data = data
        self.column_timestamp = column_timestamp
        self.gap = gap
        # 检查数据是否连续
        self.断点 = self.查找断点(data, column_timestamp, gap)

    @staticmethod
    def 查找断点(_df: pd.DataFrame, 时间栏='收盘时间', gap=timedelta(minutes=2)) -> np.ndarray:
        _df[时间栏] = pd.to_datetime(_df[时间栏])
        # cal diff
        _df['_diff_zxw_apqmu38oum'] = _df['收盘时间'].diff()
        # 断点序号
        断点序号 = _df[_df['_diff_zxw_apqmu38oum'] > gap].index.to_numpy()
        # drop _diff_zxw_ which is no longer needed
        _df.drop(columns=['_diff_zxw_apqmu38oum'], inplace=True)
        return 断点序号

    def 数据划分_避开断点(self, input长度: int, output长度: int, step=1) -> List[Tuple[int, int, int, int]]:
        """
        生成训练数据
        :param input长度: 输入数据长度
        :param output长度: 输出数据长度,
        :param step: 步长
        :return:[(input_start, input_end, output_start, output_end), ...]
        """
        训练数据序号表 = []
        # 一条数据链的长度
        链长度 = input长度 + output长度
        # 数据总长度
        数据总长度 = len(self.data)
        # 生成训练数据序号表,即每条数据链的起始位置,如果该数据链横跨断点位置,则不生成该数据链
        for i in tqdm(range(0, 数据总长度 - 链长度 + 1, step)):
            start, end = i, i + 链长度

            # if start - self.断点 的结果包含0
            if np.any(start - self.断点 == 0) or np.any(end - self.断点 == 0):
                continue

            # 如果该数据链横跨断点位置,则不生成该数据链: 如果横跨断点,则值中包含-1,否则不包含-1
            是否横跨断点 = np.divide((start - self.断点), np.abs(start - self.断点)) * \
                           np.divide((end - self.断点), np.abs(end - self.断点))
            # np累乘
            是否横跨断点 = np.prod(是否横跨断点)
            if 是否横跨断点 == -1:
                # print(f"数据链横跨断点,20不生成该数据链: {start} - {end}")
                continue
            else:
                训练数据序号表.append((start, start + input长度, start + input长度, end))

        return 训练数据序号表


def 时间列_三角函数化(timeSerial: pd.Series, 起始日期: datetime = None, 周期=timedelta(days=1)):
    """
    时间列预处理
    :param timeSerial: 数据
    :param 起始日期: 起始日期, 如果为None,则取timeSerial的最小值
    :param 周期: 时间栏
    :return:
    """
    # 判断timeSerial是否是pd.Serial的datetime类型
    if timeSerial.dtype != 'datetime64[ns]':
        raise TypeError("timeSerial必须是datetime类型(timeSerial must be datetime type)")

    # 判断timeserial内数据的最小间隔是否大于1秒
    if timeSerial.diff().min() < timedelta(seconds=1):
        print("如果您的数据间隔小于1秒,请做相应的乘法转换,例如: 1毫秒的数据,请乘以1000,转换为秒级数据")
        print("If your pd原始数据 interval < 1s, please do the corresponding multiplication conversion,"
              "\n such as: 1ms pd原始数据, you should multiply by 1000, convert to second-level pd原始数据")
        raise ValueError("timeSerial内数据的最小间隔必须大于1秒(pd原始数据 interval must be greater than 1 second)")

    # 1. 如果起始日期为None,则取timeSerial的最小值
    if 起始日期 is None:
        起始日期 = timeSerial.min()

    # 2. 将时间列转换为秒级数据
    time_points = (timeSerial - 起始日期).dt.total_seconds()
    # print(time_points)

    # 3. 计算指定的一个周期总共多少秒
    周期总秒数 = 周期.total_seconds()

    # 4. 将时间点转换为[0, 2π]范围内的值，每天一个周期
    angles = (time_points % 周期总秒数) * (2 * np.pi / 周期总秒数)
    return angles


if __name__ == '__main__':
    from matplotlib import pyplot as plt

    csv_path = "/Volumes/AI_1505056/量化交易/币安_K线数据/BTCUSDT-1m-201909-202308.csv"
    data = pd.read_csv(csv_path)

    # 生成训练数据
    x = 生成训练数据_避开时间断点(data, column_timestamp='收盘时间', gap=timedelta(minutes=2))
    print(x.断点)
    训练数据index = x.数据划分_避开断点(input长度=100, output长度=100, step=1)
    print(f"{训练数据index[0]=}")
    [print("error ", len(i)) for i in 训练数据index if len(i) != 4]
    print(len(训练数据index))

    # 时间列_三角函数化
    data['收盘时间'] = pd.to_datetime(data['收盘时间'])
    data['收盘时间y'] = 时间列_三角函数化(data['收盘时间'], 周期=timedelta(days=1))
    plt.plot(data['收盘时间'], data['收盘时间y'])
    plt.show()
