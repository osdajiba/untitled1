#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""CryptoDataFetcher：
用于获取okx永续数据
"""
import pandas as pd
import ccxt
from datetime import datetime, timedelta
import os
from tqdm import tqdm

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 500)  # 最多显示数据的行数


class CryptoDataFetcher:
    def __init__(self, time_interval='12h'):
        self.exchange = ccxt.okx()
        self.time_interval = time_interval
        self.start_time = None
        self.end_time = datetime.utcnow()
        self.filename = rf'C:\Users\PythonWork\bitcoin\data\{self.time_interval}_data.feather'

    def set_time_range(self, start, end=None):
        self.start_time = datetime.strptime(start, '%Y-%m-%d %H:%M:%S')
        if end is not None:
            self.end_time = datetime.strptime(end, '%Y-%m-%d %H:%M:%S')
        else:
            self.end_time = datetime.utcnow()

    def fetch_data(self):
        all_symbols = self.exchange.load_markets()
        perpetual_symbols = [symbol for symbol in all_symbols if symbol.endswith('/USDT:USDT')]
        all_symbol_data = []
        for symbol in tqdm(perpetual_symbols, desc="Fetching symbols"):
            try:
                # print(f"Fetching  interval data for {symbol}")
                since = self.exchange.parse8601(self.start_time.strftime('%Y-%m-%dT%H:%M:%SZ'))
                end = self.exchange.parse8601(self.end_time.strftime('%Y-%m-%dT%H:%M:%SZ'))

                symbol_data = []
                while since < end:
                    data = self.exchange.fetch_ohlcv(symbol, timeframe=self.time_interval, since=since, limit=99)
                    if data:
                        # 如果获取到数据，则扩展symbol_data并更新since为最新的数据时间戳
                        symbol_data.extend(data)
                        last_data_timestamp = data[-1][0]
                        since = last_data_timestamp
                    else:
                        # 如果没有获取到数据，则增加一个时间间隔后再尝试
                        since += self.exchange.parse_timeframe(self.time_interval) * 1000
                        # print(pd.to_datetime(since, unit='ms'))

                if symbol_data:
                    df = pd.DataFrame(symbol_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
                    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
                    df['symbol'] = symbol
                    all_symbol_data.append(df)
            except Exception as e:
                print(f"Error fetching data for {symbol}: {str(e)}")
        # 合并所有币种的数据并存储
        full_data = pd.concat(all_symbol_data, ignore_index=True)
        full_data.to_feather(self.filename)

    def update_data(self):
        try:
            # 读取现有数据
            existing_data = pd.read_feather(self.filename)

            # 确定最新的时间戳
            last_update = existing_data['timestamp'].max()
            self.set_time_range(last_update.strftime('%Y-%m-%d %H:%M:%S'))

            # 获取并添加新数据
            self.fetch_data()

            # 读取新数据并与现有数据合并
            new_data = pd.read_feather(self.filename)
            updated_data = pd.concat([existing_data, new_data]).drop_duplicates().reset_index(drop=True)
            if len(updated_data) > len(existing_data):
                # 如果有新数据被添加
                updated_data.to_feather(self.filename)
                print("数据已更新。")
            else:
                # 如果没有新数据被添加
                print("数据已经是最新的，无需更新。")

        except Exception as e:
            print(f"Error updating data: {str(e)}")


if __name__ == "__main__":
    # 创建CryptoDataFetcher实例
    data_fetcher = CryptoDataFetcher(time_interval='12h')
    if not os.path.exists(data_fetcher.filename):
        print("未找到现有数据文件，开始初次数据抓取...")
        # 设置初始的时间范围以抓取数据
        data_fetcher.set_time_range("2020-01-01 00:00:00")
        # 初次抓取数据
        data_fetcher.fetch_data()
        print("初次数据抓取完成。")
    # 设置要抓取数据的时间范围
    else:
        print("开始数据更新...")
        # 更新数据
        data_fetcher.update_data()
        print("数据更新完成。")
