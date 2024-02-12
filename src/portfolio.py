#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
import time
from dataclasses import dataclass
from typing import Any

# Configure logging
logging.basicConfig(level=logging.INFO)


def handle_error(message, exception):
    """
    Handle errors by logging them.

    :param message: str, error message.
    :param exception: Exception, the exception object.
    """
    logging.error(message)
    logging.exception(exception)


def match_signals(assets_data, signals):
    """
    Update portfolio based on trade signals and market data.

    :param assets_data: pd.DataFrame, asset market.
    :param signals: pd.DataFrame, trade signals.

    TODO: how to match the data and trading signals
    """
    if assets_data and signals:
        pass


@dataclass
class Asset:
    """
    Asset class represents an asset in a portfolio.
    """
    asset_name: str
    assets_data: Any
    initial_cash: float
    underlying_asset: str
    initial_position: float
    transaction_fee: float = None
    slippage: float = None

    def update_to_trade(self, signals):
        """
        Update portfolio based on trade signals and market data.

        :param signals: list, trade signals.

        TODO: how to update portfolio
        """
        try:
            # Update portfolio based on trade signals and market data
            # This might involve executing trades, adjusting positions, etc.
            if signals is not None:
                match_signals(self.assets_data, signals)
        except Exception as _:
            handle_error("Error occurred while updating portfolio.", _)
            raise


class Portfolio:
    def __init__(self, asset_list=None, assets_data_list=None):
        """
        Initialize Portfolio object.

        :param assets_data_list: list, additional data for each asset (optional, default=None).
        """

        # Initialize portfolio attributes
        self.asset_list = asset_list or []
        self.assets_data_list = assets_data_list or []

        # Initialize other lists
        self.cash_list = []  # List to store initial cash amounts for each asset
        self.asset_name_list = []  # List to store names or identifiers for each asset
        self.positions_list = []  # List to store initial positions for each asset
        self.underlying_asset_list = []  # List to store underlying assets
        self.transaction_fee_list = []  # List to store transaction fees for each asset
        self.slippage_list = []  # List to store slippage values for each asset

        # Initialize portfolio with assets if asset_list is provided, otherwise call initialize method
        if not asset_list:
            self.initialize(reset_flag=False)
        else:
            self.merge_asset_lists(asset_list)
            logging.info(f"asset_list has already existed: \n  {asset_list}")

    def initialize(self, reset_flag=True):
        """
        Initialize assets in the portfolio.

        :param reset_flag: bool, whether to reset the portfolio (default is True).
        """
        try:
            if reset_flag:
                self.reset()  # Reset portfolio if reset_flag is True
            # Iterate over asset information lists and initialize Asset objects
            for name, assets_data, cash, underlying_asset, position, fee, slippage in zip(
                    self.asset_name_list, self.assets_data_list, self.cash_list, self.underlying_asset_list,
                    self.positions_list, self.transaction_fee_list or [], self.slippage_list or []):
                # Create and append Asset objects to the asset_list
                self.asset_list.append(Asset(name, assets_data, cash, underlying_asset, position, fee, slippage))
        except Exception as _:
            handle_error("An error occurred.", _)
            raise

    def reset(self):
        """
        Reset portfolio to its initial state.
        """
        try:
            # Reset portfolio attributes to their initial states
            self.cash_list = []
            self.asset_name_list = []
            self.positions_list = []
            self.asset_list = []
            self.assets_data_list = []
            self.underlying_asset_list = []
            self.transaction_fee_list = []
            self.slippage_list = []
        except Exception as _:
            handle_error("Error occurred while resetting portfolio.", _)
            raise

    def handle_signals(self, signals):
        """
        Handle trading signals.

        :param signals: object, trading signals.
        """
        try:
            for asset in self.asset_list:
                asset.update_to_trade(signals)
        except Exception as _:
            handle_error("Error occurred while handling trading signals.", _)
            raise

    def add_new_asset(self, asset):
        """
        Add a new asset to the portfolio.

        :param asset: Asset, the new asset object to be added.
        """
        try:
            if asset not in self.asset_list:
                self.asset_list.append(asset)
        except Exception as _:
            handle_error("Error occurred while adding new asset to the portfolio.", _)
            raise

    def merge_asset_lists(self, *asset_lists):
        """
        Merge multiple asset lists into the portfolio.

        :param asset_lists: variable number of lists, each containing asset objects.
        """
        try:
            unique_assets = set(self.asset_list)
            for lst in asset_lists:
                unique_assets.update(lst)
            self.asset_list = list(unique_assets)
        except Exception as _:
            handle_error("Error occurred while merging asset lists.", _)
            raise


# Test code
if __name__ == "__main__":
    start = time.time()

    try:
        # Instantiate Portfolio
        portfolio = Portfolio()

        # Instantiate Asset
        asset = Asset(asset_name="Stock", assets_data=None, initial_cash=10000,
                      underlying_asset="USD", initial_position=10)

        # Add the asset to the portfolio
        portfolio.add_new_asset(asset)

        # Print the portfolio's asset list
        print(portfolio.asset_list)
    except Exception as e:
        handle_error("An error occurred in the test code.", e)

    end = time.time()
    print(f"running time: {end - start}")
