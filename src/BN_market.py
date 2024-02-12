import configparser
import json

import pandas as pd
from datetime import timedelta
import ccxt

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数


def conn_exchange(user_config):
    # try:
        exchange = ccxt.binance()
        exchange.fetch_balance(user_config)

    # except Exception as e:
    #     print(f"An unexpected error occurred: {e}")
    #     exchange = None
    # return exchange


def signin_exchange(user_config):
    try:
        exchange = ccxt.binance(user_config)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exchange = None
    return exchange


# 获取K线数据
def fetch_ohlcv_data(exchange, time_interval='1m', symbol='BTC/USDT'):
    # try:
    ohlcv = exchange.fetch_ohlcv(symbol=symbol, timeframe=time_interval)
    df = pd.DataFrame(ohlcv, columns=['MTS', 'open', 'high', 'low', 'close', 'volume'])
    df['candle_begin_time'] = pd.to_datetime(df['MTS'], unit='ms')
    df['candle_begin_time_GMT8'] = df['candle_begin_time'] + timedelta(hours=8)
    df = df[['candle_begin_time_GMT8', 'open', 'high', 'low', 'close', 'volume']]
    # except Exception as e:
    # print(f"An unexpected error occurred: {e}")
    # df = None
    return df


def load_config(file_path):
    """
    Load configuration from a JSON file.

    Parameters:
    - file_path (str): The path to the JSON configuration file.

    Returns:
    - dict: A dictionary containing the configuration settings.
    """
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print(f"Error: Config file not found at {file_path}")
    except Exception as e:
        print(f"Error loading config file: {e}")


# Test
if __name__ == "__main__":
    # Example usage:
    config_file_path = '../conf/config.json'
    config_data = load_config(config_file_path)

    if config_data:
        print("Config loaded successfully")

    # connect to binance
    Exchange = conn_exchange(config_data)
    # if Exchange is not None:
    #     Exchange = signin_exchange(config_data)
    # if Exchange is None:
    #     print("Failed to sign in")
