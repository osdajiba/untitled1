#!/usr/bin/python3
# -*- coding: utf-8 -*-
import itertools
import logging
import os

import matplotlib.pyplot as plt
import pandas as pd

from lib import data_resource, stragety, execution, performance, portfolio


def plot_backtest_results(equity_curve, trade_signals, benchmark_returns, asset_prices):
    """
    Plot the results of the backtest including the equity curve, trade signals, benchmark returns, and asset prices.

    :param equity_curve: Pandas DataFrame containing equity curve data.
    :param trade_signals: Pandas DataFrame containing trade signals data.
    :param benchmark_returns: Pandas DataFrame containing benchmark returns data.
    :param asset_prices: Pandas DataFrame containing asset prices data.

    TODO: the function's robust should be tested
    """
    try:
        # Plotting logic
        plt.figure(figsize=(14, 8))

        # Plot Asset Prices, Equity Curve, Benchmark Returns
        plt.plot(asset_prices.index, asset_prices, label='Asset Prices')
        plt.plot(equity_curve.index, equity_curve['Equity Curve'], label='Equity Curve', color='blue')
        plt.plot(benchmark_returns.index, benchmark_returns['Benchmark Returns'], label='Benchmark Returns',
                 color='green')

        # Display Trade Signals on Equity Curve
        plt.scatter(trade_signals['Buy_Signal'].index, equity_curve.loc[trade_signals['Buy_Signal'].index],
                    label='Buy Signal', color='green', marker='^', alpha=1)
        plt.scatter(trade_signals['Sell_Signal'].index, equity_curve.loc[trade_signals['Sell_Signal'].index],
                    label='Sell Signal', color='red', marker='v', alpha=1)

        plt.title('Backtest Results')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.legend()
        plt.grid(True)
        plt.show()

    except Exception as e:
        logging.error(f"Error plotting backtest results: {str(e)}")


def display_additional_metrics(metrics):
    """
    Display additional metrics of the backtest.

    :param metrics: Dictionary containing various performance metrics.

    TODO: the function's robust should be tested
    """
    try:
        metrics_df = pd.DataFrame(list(metrics.items()), columns=['Metric', 'Value'])
        logging.info("\nAdditional Metrics:")
        logging.info(metrics_df)

    except Exception as e:
        logging.error(f"Error displaying additional metrics: {str(e)}")


# # 假设您已经定义了 DataSource、Strategy、Performance、Portfolio 和 ExecutingSystem 类
#
# # 创建各个组件的实例
# data_source = DataSource(data_path='your_data_path', start_date='2022-01-01', end_date='2022-12-31')
# strategy = Strategy(parameters=your_parameters)
# performance = Performance(initial_data=your_initial_data)
# portfolio = Portfolio(initial_cash_list=your_cash_list, asset_name_list=your_asset_names, ...)
# exec_sys = ExecutingSystem(order_waitlist=your_order_waitlist, system_status=your_system_status)
#
# # 创建 BacktestEngine 实例
# with BacktestEngine(data_source=data_source, strategy=strategy, performance=performance,
#                     portfolio=portfolio, exec_sys=exec_sys) as engine:
#     # 在这里执行您的相关操作
#     pass

class BacktestEngine:
    def __init__(self, **kwargs):
        """
        Initialize the Backtest Engine with specified components.

        Args:
            **kwargs: Arbitrary keyword arguments. These arguments should match the attributes of the BacktestEngine
                     class and will be used to initialize its components.
        """
        # Initialize attributes with None
        self.data_path, self.start_date, self.end_date = None, None, None
        self.parameters = None
        self.initial_data = None
        self.initial_cash_list, self.asset_name_list, self.initial_position_list = None, None, None
        self.asset_list, self.assets_data_list, self.underlying_asset_list = None, None, None
        self.transaction_fee_list, self.slippage_list = None, None
        self.order_waitlist, self.system_status = None, None

        # Set parameters using the provided keyword arguments
        self.set_parameters(kwargs)

    def __enter__(self):
        """
        Enter method for context management.
        """
        try:
            # Set up logging
            logging.basicConfig(level=logging.INFO)

            # Initialize BacktestEngine with provided parameters
            self.data_source = data_resource.DataSource(self.data_path, self.start_date, self.end_date)
            self.strategy = stragety.Strategy(self.parameters)
            self.performance = performance.Performance(self.initial_data)
            self.portfolio = portfolio.Portfolio(self.initial_cash_list, self.asset_name_list,
                                                 self.initial_position_list, self.asset_list, self.assets_data_list,
                                                 self.transaction_fee_list, self.slippage_list)
            self.exec_sys = execution.ExecutingSystem(self.order_waitlist, self.system_status)
        except Exception as e:
            logging.error(f"Error initializing Backtest Engine: {str(e)}")
            raise e

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit method for context management.
        """
        # Optional cleanup actions can be added here
        pass

    def set_parameters(self, paras):
        """
        Set parameters for the backtest.

        Args:
            paras (dict): Dictionary containing parameters to set.
        """
        if paras is not None:
            for key, value in paras.items():
                if hasattr(self, key):
                    setattr(self, key, value)
                else:
                    logging.warning(f"Ignoring unknown parameter: {key}")

    def run_backtest(self, display_result=None, reset=True):
        """
        Run the backtest using historical market data.
        """
        try:
            historical_data = self.data_source.get_historical_data()

            for bar in historical_data:
                signals = self.strategy.generate_signals(bar)
                trade_history = self.portfolio.handle_signals(signals, bar)
                self.strategy.execute_trades(self.portfolio, trade_history)
                self.performance.update_performance(self.portfolio)

            self.performance.generate_report()
            if display_result:
                self.disp_result()

            if reset:
                self.reset()
            logging.info("Backtest completed.")

        except Exception as e:
            # Log the exception
            logging.error(f"Error during backtest: {str(e)}")
            # Send error notification
            logging.info(f"Notification - "
                         f"Title: Backtest Error"
                         f"Message: Exception during backtest: {str(e)}")

    def optimize_parameters(self, parameter_ranges):
        """
        Perform parameter optimization for the backtest.

        :param parameter_ranges: Dictionary specifying parameter ranges for optimization.
        """
        best_params = None
        best_metric = float('-inf')

        param_combinations = list(
            itertools.product(*[range(*param_range) for param_range in parameter_ranges.values()]))

        for params in param_combinations:
            self.data_source.set_date_range(self.start_date, self.end_date)

            self.run_backtest()

            metric = self.get_performance_metrics()['your_metric_name']

            if metric > best_metric:
                best_metric = metric
                best_params = params

        logging.info(f"Best parameters: {best_params}")
        logging.info(f"Best metric: {best_metric}")

        return best_metric, best_params

    def disp_result(self):
        """
        Display the results of the backtest including additional metrics and visualizations.
        """
        equity_curve = self.performance.get_equity_curve()
        trade_signals = self.strategy.get_trade_signals()  # Replace with actual method to get trade signals
        benchmark_returns = self.data_source.get_benchmark_returns()  # Replace with actual method to get benchmark returns
        asset_prices = self.data_source.get_asset_prices()  # Replace with actual method to get asset prices

        # Plot the backtest results
        plot_backtest_results(equity_curve, trade_signals, benchmark_returns, asset_prices)

        # Display additional metrics
        metrics = self.performance.get_metrics()  # Assuming get_metrics returns a dictionary of metrics
        display_additional_metrics(metrics)

    def save_results(self, file_name):
        """
        Save backtest results to a file.

        :param file_name: Name of the backtest for creating a subdirectory.
        """
        try:
            # Create a subdirectory for the backtest results
            save_dir = os.path.join('../log/backtest_result/', file_name)
            os.makedirs(save_dir, exist_ok=True)

            # Save backtest results to files in the created subdirectory
            equity_curve = self.performance.get_equity_curve()
            metrics = self.performance.get_metrics()

            equity_curve.to_csv(os.path.join(save_dir, 'equity_curve.csv'))

            # Save metrics to a CSV file
            metrics_df = pd.DataFrame(list(metrics.items()), columns=['Metric', 'Value'])
            metrics_df.to_csv(os.path.join(save_dir, 'metrics.csv'))

            logging.info(f"Backtest results saved in {save_dir}")

        except Exception as e:
            logging.error(f"Error saving backtest results: {str(e)}")

    def reset(self):
        """
        Reset the backtest engine to its initial state.
        """
        self.portfolio.reset()
        self.performance.reset()
        logging.info("Backtest engine reset.")

    def get_performance_metrics(self):
        """
        Get the performance metrics of the backtest.

        :return: Dictionary containing various performance metrics.
        """
        metrics = self.performance.get_metrics()
        logging.info("Performance metrics retrieved.")
        return metrics

    def add_indicator(self, indicator):
        """
        Add a custom performance indicator to the backtest.

        :param indicator: Custom indicator to be added.
        """
        self.performance.add_custom_indicator(indicator)
        logging.info(f"Custom indicator '{indicator}' added.")
