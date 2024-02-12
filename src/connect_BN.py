#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flask import Flask, request  # 导入后端框架
import json
import ccxt  # 导入开单工具
import time


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
            result = json.load(file)
        return result
    except FileNotFoundError:
        print(f"Error: Config file not found at {file_path}")
    except Exception as e:
        print(f"Error loading config file: {e}")


# 开单函数（这里是Binance Api接口的程序）
def open_order(data):
    try:
        symbol = data['symbol'].replace('PERP', '')
        side = data['side']
        amount = float(format(float(data['amount']), '.%sf' % data['point']))
        if side == 'buy':
            bn.fapiPrivatePostOrder(
                {"symbol": symbol, "side": "BUY", "type": "MARKET", "quantity": amount, 'reduceOnly': 'false',
                 "timestamp": int(time.time() * 1000)})
        else:
            bn.fapiPrivatePostOrder(
                {"symbol": symbol, "side": "SELL", "type": "MARKET", "quantity": amount, 'reduceOnly': 'false',
                 "timestamp": int(time.time() * 1000)})
        return
    except Exception as e:
        print(e)


app = Flask(__name__)


def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


app.after_request(after_request)


@app.route("/open", methods=['POST'])
def open1():
    data = json.loads(request.data)
    open_order(data)
    return '1'


if __name__ == '__main__':
    file_path = "../conf/config.json"
    config = load_config(file_path)

    apiKey = config['apiKey']
    secret = config['secret']
    proxies = config['proxies']
    timeout = config['timeout']

    bn = ccxt.binance()
    bn.apiKey = apiKey
    bn.proxies = proxies
    bn.timeout = timeout

    bn.fetch_balance()
    # app.run('0.0.0.0', 7890)  # 端口接入
