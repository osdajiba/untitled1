#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import numpy as np
import pandas as pd


def cumulative_returns(equity_curve):
    """
    Calculate cumulative returns.

    :param equity_curve: array-like, equity curve.
    :return: float, cumulative returns.
    """
    cumulative_return = (equity_curve[-1] / equity_curve[0]) - 1
    return cumulative_return


def maximum_drawdown(equity_curve):
    """
    Calculate maximum drawdown.

    :param equity_curve: array-like, equity curve.
    :return: float, maximum drawdown.
    """
    peak = equity_curve.max()
    trough = equity_curve.min()
    drawdown = (trough - peak) / peak
    return drawdown


def sharpe_ratio(returns, risk_free_rate):
    """
    Calculate Sharpe ratio.

    :param returns: array-like, returns.
    :param risk_free_rate: float, risk-free rate.
    :return: float, Sharpe ratio.
    """
    excess_returns = returns - risk_free_rate
    sharpe = np.mean(excess_returns) / np.std(excess_returns)
    return sharpe


def annualized_return(total_returns, num_years):
    """
    Calculate annualized return.

    :param total_returns: float, total returns.
    :param num_years: int, number of years.
    :return: float, annualized return.
    """
    annual_return = (1 + total_returns) ** (1 / num_years) - 1
    return annual_return


def number_of_trades(trades):
    """
    Calculate the number of trades.

    :param trades: array-like, trades data.
    :return: int, number of trades.
    """
    num_trades = len(trades)
    return num_trades


def average_profit_per_trade(trades):
    """
    Calculate the average profit per trade.

    :param trades: array-like, trades data.
    :return: float, average profit per trade.
    """
    profits = [trade['profit'] for trade in trades]
    average_profit = np.mean(profits)
    return average_profit


def average_holding_period(trades):
    """
    Calculate the average holding period.

    :param trades: array-like, trades data.
    :return: float, average holding period.
    """
    holding_periods = [(trade['exit_date'] - trade['entry_date']).days for trade in trades]
    average_holding_period = np.mean(holding_periods)
    return average_holding_period


def winning_percentage(trades):
    """
    Calculate the winning percentage.

    :param trades: array-like, trades data.
    :return: float, winning percentage.
    """
    num_winning_trades = sum(1 for trade in trades if trade['profit'] > 0)
    total_trades = len(trades)
    winning_percentage = num_winning_trades / total_trades
    return winning_percentage


def losing_percentage(trades):
    """
    Calculate the losing percentage.

    :param trades: array-like, trades data.
    :return: float, losing percentage.
    """
    num_losing_trades = sum(1 for trade in trades if trade['profit'] < 0)
    total_trades = len(trades)
    losing_percentage = num_losing_trades / total_trades
    return losing_percentage


def daily_or_weekly_returns_analysis(returns):
    """
    Analyze daily or weekly returns.

    :param returns: list or array, daily or weekly returns of the strategy.
    :return: dict, dictionary containing the results of returns analysis.
    """
    result = {}  # Create an empty dictionary for storing results

    returns = np.array(returns)

    # Calculate various statistics
    result['mean_return'] = np.mean(returns)
    result['std_deviation'] = np.std(returns)
    result['skewness'] = pd.Series(returns).skew()
    result['kurtosis'] = pd.Series(returns).kurtosis()

    return result  # Return the dictionary containing results


def handle_error(error):
    """
    Handle errors during performance evaluation.

    :param error: Exception object, error occurred during performance evaluation.
    """
    logging.error(f"Error occurred during performance evaluation: {error}")


def get_metrics(asset):
    """
    Calculate performance metrics and return them as a DataFrame.

    :param asset: object, asset data.
    :return: pandas DataFrame, performance metrics.
    """
    metrics_dict = {
        'cumulative_return': cumulative_returns(asset.equity_curve),
        'max_drawdown': maximum_drawdown(asset.equity_curve),
        'sharpe_ratio': sharpe_ratio(asset.returns, asset.risk_free_rate),
        'annual_return': annualized_return(asset.total_returns, asset.num_years),
        'trade_times': number_of_trades(asset.trades),
        'average_profit_per_trade': average_profit_per_trade(asset.trades),
        'average_hold_period': average_holding_period(asset.trades),
        'winning_percentage': winning_percentage(asset.trades),
        'losing_percentage': losing_percentage(asset.trades),
        'return_analysis': daily_or_weekly_returns_analysis(asset.returns)
    }
    metrics_df = pd.DataFrame(metrics_dict, index=[0])  # Convert metrics_dict to DataFrame
    return metrics_df


class Performance:
    def __init__(self, portfolio=None, initial_data=None):
        """
        Initialize Performance object.

        :param portfolio: object, portfolio data.
        :param initial_data: object, initial data for performance evaluation.
        """
        self.portfolio = portfolio
        self.data = initial_data
        logging.info("Performance evaluation parameters are initialized.")

    def initialize(self, initial_data):
        """
        Initialize performance evaluation state.

        :param initial_data: object, initial data for performance evaluation.
        """
        if self.data is None:
            self.data = initial_data
        logging.info("Performance evaluation state is initialized.")

    def update_performance(self):
        """
        Update performance metrics based on the provided portfolio.
        """
        for asset in self.portfolio:
            try:
                metrics_df = get_metrics(asset)
                logging.info("Backtest report is generated.")
                return metrics_df
            except Exception as e:
                handle_error(e)
        logging.info("Performance metrics are updated.")

    def add_custom_indicator(self, indicator):
        """
        Add a custom performance indicator.

        :param indicator: object, custom performance indicator.
        """
        # Add a custom performance indicator
        logging.info("Custom performance indicator is added.")
