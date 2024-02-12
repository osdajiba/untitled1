#!/usr/bin/python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd


def sma(data, window=10):
    """
    计算简单移动平均线（SMA）

    :param data: 包含股票价格数据的 DataFrame
    :param window: 移动平均窗口大小
    :return: 在原始数据上添加了SMA列的 DataFrame
    """

    result = data['close'].rolling(window=window).mean()
    return result


def rsi(data, window=14):
    """
    计算相对强度指数（RSI）

    :param data: 包含股票价格数据的 DataFrame
    :param window: RSI 窗口大小
    :return: 在原始数据上添加了RSI列的 DataFrame
    """

    delta = data['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    result = 100 - (100 / (1 + avg_gain / avg_loss))
    return result


def vwap(data):
    """
    计算成交量加权平均价（VWAP）

    :param data: 包含股票价格和成交量数据的 DataFrame，必须包含 'close'（收盘价）和 'volume'（成交量）列
    :return: 在原始数据上添加了 VWAP 列的 DataFrame
    """

    result = (((data['close'] + data['low'] + data['high']) / 3 * data['volume']).cumsum() /
              data['volume'].cumsum())
    return result


def atr(data, period=14):
    """
    计算平均真实范围（ATR）

    :param data: 包含股票价格数据的 DataFrame，必须包含 'high'（最高价）、'low'（最低价）和 'close'（收盘价）列
    :param period: ATR 计算的周期，默认为 14
    :return: 在原始数据上添加了 ATR 列的 DataFrame
    """

    # 计算 True Range（TR）
    data['tr0'] = abs(data['high'] - data['low'])
    data['tr1'] = abs(data['high'] - data['close'].shift())
    data['tr2'] = abs(data['low'] - data['close'].shift())
    true_range = data[['tr0', 'tr1', 'tr2']].max(axis=1)

    # 计算 ATR
    result = true_range.rolling(window=period).mean()

    return result


def SuperTrend(data, period=14, multiplier=3):
    """
    计算 SuperTrend 指标

    :param data: 包含股票价格数据的 DataFrame，必须包含 'high'（最高价）、'low'（最低价）和 'close'（收盘价）列
    :param period: ATR 计算的周期，默认为 14
    :param multiplier: SuperTrend 的倍数，默认为 3
    :return: 在原始数据上添加了 SuperTrend 列的 DataFrame
    """

    result = pd.DataFrame(index=data.index)  # Initialize result DataFrame with the same index as data

    # 计算 ATR
    ATR = atr(data, period)

    # 计算基础 Super-trend
    upper_band = (data['high'] + data['low']) / 2 + multiplier * ATR.shift()
    lower_band = (data['high'] + data['low']) / 2 - multiplier * ATR.shift()

    result['SuperTrend'] = None
    for i in range(1, len(data)):
        if data['close'][i - 1] <= upper_band[i - 1]:
            result['SuperTrend'][i] = upper_band[i]
        elif data['close'][i - 1] >= lower_band[i - 1]:
            result['SuperTrend'][i] = lower_band[i]
        else:
            result['SuperTrend'][i] = result['SuperTrend'][i - 1]

    return result


def aroon(data, window=14):
    """
    计算 Aroon 指标

    :param data: 包含股票价格数据的 DataFrame，必须包含 'high'（最高价）和 'low'（最低价）列
    :param window: Aroon 计算的周期，默认为 14
    :return: 在原始数据上添加了 Aroon Up 和 Aroon Down 列的 DataFrame
    """

    result = pd.DataFrame(index=data.index)  # Initialize result DataFrame with the same index as data
    result['aroon_up'] = (window - data['high'].rolling(window=window).apply(np.argmax) + 1) / window * 100
    result['aroon_down'] = (window - data['low'].rolling(window=window).apply(np.argmin) + 1) / window * 100
    return result


def ma(data, window=20):
    """
    计算移动平均线（MA）

    :param data: 包含股票价格数据的 DataFrame，必须包含 'close'（收盘价）列
    :param window: 移动平均窗口大小，默认为 20
    :return: MA 列的 DataFrame
    """

    result = data['close'].rolling(window=window).mean()
    return result


def BB(data, window=20, num_std_dev=2):
    """
    计算布林带指标

    :param data: 包含股票价格数据的 DataFrame，必须包含 'close'（收盘价）列
    :param window: 移动平均窗口大小，默认为 20
    :param num_std_dev: 布林带宽度为移动平均的标准差倍数，默认为 2
    :return: 含上轨、中轨和下轨列的 DataFrame
    """
    result = pd.DataFrame(index=data.index)  # Initialize result DataFrame with the same index as data

    MA = (ma(data, window=window))
    data['std'] = data['close'].rolling(window=window).std()

    result['upper_band'] = MA + num_std_dev * data['std']
    result['lower_band'] = MA - num_std_dev * data['std']
    result['middle_band'] = MA

    return result


# Test
if __name__ == "__main__":
    # test data
    data = pd.DataFrame({
        'close': [10, 12, 8, 15, 13, 14, 11, 9, 10, 12],
        'volume': [1000, 1200, 800, 1500, 1300, 1400, 1100, 900, 1000, 1200],
        'high': [12, 15, 10, 18, 14, 16, 13, 11, 12, 15],
        'low': [8, 10, 7, 12, 9, 11, 9, 8, 9, 10],
    })

    # SMA
    data_with_sma = sma(data.copy(), window=3)
    print("Data with SMA:")
    print(data_with_sma)

    # RSI
    data_with_rsi = rsi(data.copy(), window=4)
    print("\nData with RSI:")
    print(data_with_rsi)

    # VWAP
    data_with_vwap = vwap(data.copy())
    print("Data with VWAP:")
    print(data_with_vwap)

    # ATR
    data_with_atr = atr(data.copy(), period=4)
    print("Data with ATR:")
    print(data_with_atr)

    # SuperTrend
    data_with_supertrend = SuperTrend(data.copy(), period=4, multiplier=3)
    print("Data with Supertrend:")
    print(data_with_supertrend)

    # Bolling bands
    data_with_factors = BB(data.copy(), window=4, num_std_dev=2)
    print("Data with Bollinger Bands, Aroon, and MA:")
    print(data_with_factors)
