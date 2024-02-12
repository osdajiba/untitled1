#!/usr/bin/python3
# -*- coding: utf-8 -*-
import hashlib
from datetime import datetime
import random
import logging
import execution
from dataclasses import asdict


class Order:
    def __init__(self, symbol, quantity, action, exec_settings, order_type=None, price=None, position_effect=None,
                 status='PENDING', order_id=None, creation_time=None, execution_time=None, cancellation_time=None):
        """
        Initialize a generic order.

        :param order_type: The type of the order, e.g., 'LIMIT', 'MARKET', 'STOP', etc.
        :param symbol: The trading symbol for the order (e.g., stock ticker).
        :param quantity: The quantity of assets to be traded.
        :param action: The action of the order, e.g., 'BUY' or 'SELL'.
        :param price: The specified price for the order (None for market orders).
        :param position_effect: The direction of the order in terms of opening or closing a position, e.g., 'OPEN' or 'CLOSE'.
        """
        # Basic order params
        self.order_type = order_type
        self.symbol = symbol
        self.quantity = quantity
        self.action = action
        self.price = price
        self.position_effect = position_effect
        self.status = status
        self.slippage = exec_settings.slippage
        self.transaction_fee = exec_settings.transaction_fee

        # Order execution params
        self.order_id = order_id
        self.creation_time = creation_time
        self.execution_time = execution_time
        self.cancellation_time = cancellation_time

    def __enter__(self):
        # Generate order_id and set creation_time on initialization
        if self.order_id is None:
            self.generate_order_id()
        if self.creation_time is None:
            self.creation_time = datetime.now()
        self.log_order_details()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def generate_order_id(self):
        """
        Generate a unique order ID.
        # This method need overloading in child class.
        """
        if self.order_id is None:
            timestamp = self.creation_time
            random_part_1 = str(random.randint(10, 99))
            random_part_2 = str(random.randint(10, 99))

            mapped_info = f"{self.order_type}-{self.symbol}-{self.quantity}-{self.action}-{self.price}-{self.position_effect}"
            # Combine timestamp, random number, and hashed info
            combined_info = f"{random_part_1}-{mapped_info}-{random_part_2}"

            # Use SHA-256 hash function to generate a unique ID
            hash_object = hashlib.sha256(combined_info.encode())
            hashed_info = hash_object.hexdigest()[:12]  # Take the first 12 characters of the hash
            self.order_id = f"{timestamp}-{hashed_info}"

    def cancel(self, status, execution_time):
        """
        Cancel the order.
        """
        if self.status == 'PENDING':
            self.status = status
            self.execution_time = execution_time

    def execute(self, status, execution_time, quantity):
        """
        Execute the order.
        """
        if self.status == 'PENDING':
            self.status = status
            self.execution_time = execution_time
            self.quantity = quantity

    def modify(self, order_args):
        """
        Execute the order.
        """
        if self.status == 'PENDING':
            self.set_order_args(order_args)
            self.status = 'EXECUTED'

    def get_status(self):
        return self.status

    def get_symbol(self):
        return self.symbol

    def get_action(self):
        return self.action

    def get_position_effect(self):
        return self.position_effect

    def get_order_type(self):
        return self.order_type

    def get_price(self):
        return self.price

    def get_quantity(self):
        return self.quantity

    def get_condition(self):
        return self.condition

    def get_creation_time(self):
        return self.creation_time

    def get_execution_time(self):
        return self.execution_time

    def get_cancellation_time(self):
        return self.cancellation_time

    def get_order_id(self):
        return self.order_id

    def get_slippage(self):
        return self.slippage

    def get_transaction_fee(self):
        return self.transaction_fee

    def get_order_args(self):
        """
        Return the order parameters as a dictionary.

        Returns:
            dict: A dictionary containing the order parameters.
        """
        order_args = {
            'order_type': self.order_type,
            'symbol': self.symbol,
            'quantity': self.quantity,
            'action': self.action,
            'price': self.price,
            'position_effect': self.position_effect,
            'status': self.status,
            'order_id': self.order_id,
            'creation_time': self.creation_time,
            'execution_time': self.execution_time,
            'cancellation_time': self.cancellation_time
        }
        return order_args

    def set_order_args(self, order_args):
        """
        Set the order parameters using a dictionary.

        Args:
            order_args (dict): A dictionary containing the order parameters.
        """
        for key, value in order_args.items():
            setattr(self, key, value)

    def set_status(self, status):
        self.status = status

    def set_symbol(self, symbol):
        self.symbol = symbol

    def set_action(self, action):
        self.action = action

    def set_position_effect(self, position_effect):
        self.position_effect = position_effect

    def set_order_type(self, order_type):
        self.order_type = order_type

    def set_price(self, price):
        self.price = price

    def set_quantity(self, quantity):
        self.quantity = quantity

    def set_condition(self, condition):
        self.condition = condition

    def set_creation_time(self, creation_time):
        self.creation_time = creation_time

    def set_execution_time(self, execution_time):
        self.execution_time = execution_time

    def set_cancellation_time(self, cancellation_time):
        self.cancellation_time = cancellation_time

    def set_order_id(self, order_id):
        self.order_id = order_id

    def set_slippage(self, slippage):
        self.slippage = slippage

    def set_transaction_fee(self, transaction_fee):
        self.transaction_fee = transaction_fee

    def is_pending(self):
        return self.status == 'PENDING'

    def is_filled(self):
        return self.status == 'FILLED'

    def is_cancelled(self):
        return self.status == 'CANCELLED'

    def modify_quantity(self, new_quantity):
        self.quantity = new_quantity

    def modify_price(self, new_price):
        self.price = new_price

    def modify_action(self, new_action):
        self.action = new_action

    def log_order_details(self):
        """
        Log relevant order details.
        """
        logger = logging.getLogger('order_logger')

        # Configure the logger (configure it only once in your application)
        logging.basicConfig(filename='order_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')

        attributes_to_log = [
            'order_id', 'symbol', 'quantity', 'action', 'price',
            'status', 'order_type', 'position_effect', 'slippage',
            'transaction_fee', 'execution_time', 'creation_time', 'cancellation_time'
        ]

        for attribute in attributes_to_log:
            logger.info(f"{attribute.capitalize().replace('_', ' ')}: {getattr(self, attribute)}")

    def update_status(self, new_status):
        """
        Update the status of the order.
        :param new_status: The new status for the order.
        """
        self.status = new_status

    def get_order_details(self):
        """
        Get details of the order.

        :return: A dictionary containing details of the order.
        """
        return {
            'order_type': self.order_type,
            'symbol': self.symbol,
            'quantity': self.quantity,
            'action': self.action,
            'price': self.price,
            'status': self.status,
            'order_id': self.order_id,
            'creation_time': self.creation_time,
            'execution_time': self.execution_time,
            'cancellation_time': self.cancellation_time,
        }


class LimitOrder(Order):
    def __init__(self, symbol, quantity, action, limit_price, exec_settings=None):
        """
        Initialize a limit order.

        :param limit_price: The specified price at or better than which the order should be executed.

        TODO: the specify input parameters
        TODO: more functions
        """
        super().__init__(symbol, quantity, action, exec_settings)
        self.type = 'LIMIT'


class MarketOrder(Order):
    def __init__(self, symbol, quantity, action, exec_settings=None):
        """
        Initialize a market order.

        TODO: the specify input parameters
        TODO: more functions
        """
        super().__init__(symbol, quantity, action, exec_settings)
        self.type = 'MARKET'


class StopOrder(Order):
    def __init__(self, symbol, quantity, action, stop_price, exec_settings=None):
        """
        Initialize a stop order.

        :param stop_price: The specified price at which the stop order becomes a market order.

        TODO: the specify input parameters
        TODO: more functions
        """
        super().__init__(symbol, quantity, action, exec_settings)
        self.type = 'STOP'


class TakeProfitOrder(Order):
    def __init__(self, symbol, quantity, action, take_profit_price, exec_settings=None):
        """
        Initialize a take-profit order.

        :param take_profit_price: The specified price at or better than which the order should be executed.

        TODO: the specify input parameters
        TODO: more functions
        """
        super().__init__(symbol, quantity, action, exec_settings)
        self.type = 'TAKE_PROFIT'


class StopLossOrder(Order):
    def __init__(self, symbol, quantity, action, stop_loss_price, exec_settings=None):
        """
        Initialize a stop-loss order.

        :param stop_loss_price: The specified price at which the stop-loss order becomes a market order.

        TODO: the specify input parameters
        TODO: more functions
        """
        super().__init__(symbol, quantity, action, exec_settings)
        self.type = 'STOP_LOSS'


class IcebergOrder(LimitOrder):
    def __init__(self, symbol, quantity, action, limit_price, display_quantity, exec_settings=None):
        """
        Initialize an iceberg order.

        :param display_quantity: The quantity of the order that is displayed in the order book.

        TODO: the specify input parameters
        TODO: more functions
        """
        super().__init__(symbol, quantity, action, exec_settings)
        self.type = 'ICEBERG'
        self.display_quantity = display_quantity


class TrailingStopOrder(StopOrder):
    def __init__(self, symbol, quantity, action, stop_percent, exec_settings=None):
        """
        Initialize a trailing stop order.

        :param stop_percent: The percentage below the market price for a sell order or above for a buy order.

        TODO: the specify input parameters
        TODO: more functions
        """
        super().__init__(symbol, quantity, action, exec_settings)
        self.type = 'TRAILING_STOP'
        self.stop_percent = stop_percent


class OCOOrder(Order):
    def __init__(self, symbol, quantity, action, limit_price, stop_price, exec_settings=None):
        """
        Initialize an OCO (One-Cancels-the-Other) order.

        :param limit_price: The price at which the limit order should be executed.
        :param stop_price: The price at which the stop order should be executed.

        TODO: the specify input parameters
        TODO: more functions
        """
        super().__init__(symbol, quantity, action, exec_settings)
        self.type = 'OCO'
        self.limit_order = LimitOrder(symbol, quantity, action, limit_price)
        self.stop_order = StopOrder(symbol, quantity, action, stop_price)


# Example usage
exec_settings = execution.Execution_settings(transaction_fee=0.00002, slippage=0.01)

with Order('AAPL', 10, 'BUY', exec_settings, 'OPEN', price=150.0) as order_instance:
    # Some operations within the context
    order_instance.status = 'EXECUTED'
    order_instance.execution_time = datetime.now()
    # Exiting the context will call __exit__, and if the status is still 'PENDING', it will cancel the order
