# !/usr/bin/python3
# -*- coding: utf-8 -*-

from lib.backtest_engine import BacktestEngine


def main():
    """
    Main function to demonstrate the usage of the backtest engine.
    """
    # 创建数据源、交易策略、投资组合、交易执行模块、性能评估模块
    data_source = YourDataSource()
    strategy = YourStrategy()
    portfolio = YourPortfolio()
    execution = YourExecution()
    performance = YourPerformance()

    # 创建回测引擎
    backtest_engine = BacktestEngine(data_source, strategy, portfolio, execution, performance)

    # 设置回测参数
    backtest_engine.set_parameters(start_date='2020-01-01', end_date='2021-01-01', transaction_fee=0.0002,
                                   slippage=0.0005)

    # 运行回测
    backtest_engine.run_backtest()

    # 绘制回测结果
    backtest_engine.disp_result()

    # 保存回测结果
    backtest_engine.save_results('my_backtest')


if __name__ == "__main__":
    main()
