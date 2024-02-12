#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Asset:
    def __init__(self, asset_name, assets_data, initial_cash, underlying_asset, initial_position,
                 transaction_fee=None, slippage=None):
        """
        Initialize an Asset object.

        :param asset_name: str, name or identifier of the asset.
        :param assets_data: Any, additional data related to the asset.
        :param initial_cash: float, initial cash amount for the asset.
        :param underlying_asset: str, underlying asset name or identifier.
        :param initial_position: float, initial position for the asset.
        :param transaction_fee: float, transaction fee for the asset (optional, default=None).
        :param slippage: float, slippage for the asset (optional, default=None).
        """
        self.asset_name = asset_name
        self.assets_data = assets_data
        self.initial_cash = initial_cash
        self.underlying_asset = underlying_asset
        self.initial_position = initial_position
        self.transaction_fee = transaction_fee
        self.slippage = slippage

    def update_to_trade(self, signals, bar):
        """
        Update portfolio based on trade signals and market data.

        :param signals: list, trade signals.
        :param bar: object, market data for the current time period.

        TODO: how to update portfolio
        """
        # Update portfolio based on trade signals and market data
        # This might involve executing trades, adjusting positions, etc.
        pass


class Portfolio:
    def __init__(self, initial_cash_list=None, asset_name_list=None, initial_position_list=None,
                 asset_list=None, assets_data_list=None, transaction_fee_list=None, slippage_list=None):
        """
        Initialize Portfolio object.

        :param initial_cash_list: list, initial cash amounts for each asset.
        :param asset_name_list: list, names or identifiers for each asset.
        :param initial_position_list: list, initial positions for each asset.
        :param asset_list: list, list of Asset objects (optional, default=None).
        :param assets_data_list: list, additional data for each asset (optional, default=None).
        :param transaction_fee_list: list, transaction fees for each asset (optional, default=None).
        :param slippage_list: list, slippage values for each asset (optional, default=None).
        """

        self.cash_list = initial_cash_list or []
        self.asset_name_list = asset_name_list or []
        self.positions_list = initial_position_list or []
        self.asset_list = asset_list or []
        self.assets_data_list = assets_data_list or []
        self.underlying_asset_list = []
        self.transaction_fee_list = transaction_fee_list or []
        self.slippage_list = slippage_list or []

        if not asset_list:
            self.initialize(reset_flag=False)
        else:
            print(f"asset_list has already exited: \n  {asset_list}")

    def initialize(self, reset_flag=True):
        if reset_flag:
            self.reset()
        for name, assets_data, cash, underlying_asset, position, fee, slippage in zip(
                self.asset_name_list, self.assets_data_list, self.cash_list, self.underlying_asset_list,
                self.positions_list, self.transaction_fee_list or [], self.slippage_list or []):
            self.asset_list.append(Asset(name, assets_data, cash, underlying_asset, position, fee, slippage))

    def reset(self):
        """
        Reset portfolio to its initial state.
        """
        # Reset portfolio to initial state
        # This might involve setting cash and positions back to their initial values
        self.cash_list = []
        self.asset_name_list = []
        self.positions_list = []
        self.asset_list = []
        self.assets_data_list = []
        self.underlying_asset_list = []
        self.transaction_fee_list = []
        self.slippage_list = []

    def handle_signals(self, signals, bar):
        pass
