"""
# File       : 时间序列_数据对齐.py
# Time       ：2023/9/30 16:54
# Author     ：xuewei zhang
# Email      ：jingmu_predict@qq.com
# version    ：python 3.10
# Description：
"""
from datetime import datetime
import pandas as pd
from typing import List


class 时间序列_数据对齐:

    def __init__(self, data: pd.DataFrame, 时间栏='收盘时间'):
        self.data = data
        self.时间栏 = 时间栏

    def 查找_时间范围(self, 查找时间: datetime, 查找精度='1min') -> List[int]:
        """
        :param 查找时间: datetime
        :param 查找精度: str , '1min' or '1h' or '1d'
        :return: pd.DataFrame
        """
        # 1. 对齐时间 按 对齐标准 , 将多出来的时间归零
        if 查找精度 == '1min':
            对齐时间 = 查找时间.replace(second=0, microsecond=0)
            self.data[self.时间栏] = self.data[self.时间栏].apply(lambda x: x.replace(second=0, microsecond=0))
        elif 查找精度 == '1h':
            对齐时间 = 查找时间.replace(minute=0, second=0, microsecond=0)
            self.data[self.时间栏] = self.data[self.时间栏].apply(
                lambda x: x.replace(minute=0, second=0, microsecond=0))
        elif 查找精度 == '1d':
            对齐时间 = 查找时间.replace(hour=0, minute=0, second=0, microsecond=0)
            self.data[self.时间栏] = self.data[self.时间栏].apply(
                lambda x: x.replace(hour=0, minute=0, second=0, microsecond=0))
        else:
            raise Exception('对齐标准错误, 请检查')

        # 2. 查找对齐时间的位置
        # 2.1 获取时间栏
        时间栏 = self.data[self.时间栏]
        # 2.2 在时间serial中查找对应时间
        对齐时间索引位置 = 时间栏[时间栏 == 对齐时间].index.tolist()
        return 对齐时间索引位置


if __name__ == '__main__':

    csv_path = r'/Volumes/AI_1505056/量化交易/币安_K线数据_1d/BTCUSDT-1m-201909-202308.csv'
    data = pd.read_csv(csv_path, dtype={"开盘价": 'float64', "最高价": 'float64', "最低价": 'float64',
                                        "收盘价": 'float64', "成交量": 'float64', "报价币成交量": 'float64', "成单数": 'float64',
                                        "吃单方买入的基础币数量": 'float64', "吃单方买入的报价币数量": 'float64'})
    # to datetime
    data['收盘时间'] = pd.to_datetime(data['收盘时间'])

    # drop part of columns if it exits
    data.drop(columns=['开盘时间戳', '收盘时间戳'], inplace=True)

    #
    数据预处理 = 时间序列_数据对齐(data, '收盘时间')
    i = 数据预处理.查找_时间范围(datetime(2023, 8, 29, 16, 54, 0), 查找精度='1d')
    print(i)
