#!/usr/bin/python3
# -*- coding: utf-8 -*-
import queue
import threading
# execution.py

from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)  # Set the desired log level


def process_execution_response(execution_response):
    """
    Process execution response and handle success or failure.

    Args:
        execution_response (dict): Execution response.
    """
    order_id = execution_response.get('order_id')
    if execution_response.get('status') == 'SUCCESS':
        execution_time = execution_response.get('time')
        logging.info(f"Order {order_id} executed successfully.")
        # Update order attributes if necessary
        # Log the order execution
        log_order_execution(order_id, execution_time)
        # Monitor the order status after execution
        monitor_order_status(order_id)
        # Send notifications (you can replace this with your notification logic)
        send_notification("Order Executed", f"Order {order_id} executed successfully.")
    else:
        logging.error(f"Order {order_id} execution failed: {execution_response.get('message')}")
        # Log the error
        log_error(f"Error executing order {order_id}: {execution_response.get('message')}")
        # Send error notification
        send_notification("Order Execution Failed",
                          f"Error executing order {order_id}: {execution_response.get('message')}")


def process_modification_response(modify_response):
    """
    Process modification response and handle success or failure.

    Args:
        modify_response (dict): Modification response.
    """
    order_id = modify_response.get('order_id')
    if modify_response.get('status') == 'SUCCESS':
        creation_time = modify_response.get('time')
        logging.info(f"Order {order_id} modified successfully.")
        # Log the order modification
        log_order_modification(order_id, creation_time)
        # Monitor the order status after modification
        monitor_order_status(order_id)
        # Send notifications (you can replace this with your notification logic)
        send_notification("Order Modified", f"Order {order_id} modified successfully.")
    else:
        logging.error(f"Order {order_id} modification failed: {modify_response.get('message')}")
        # Log the error
        log_error(f"Error modifying order {order_id}: {modify_response.get('message')}")
        # Send error notification
        send_notification("Order Modification Failed",
                          f"Error modifying order {order_id}: {modify_response.get('message')}")


def process_cancellation_response(order_response):
    """
    Process cancellation response and handle success or failure.

    Args:
        order_response (dict): Cancellation response.
    """
    order_id = order_response.get('order_id')

    if order_response.get('status') == 'SUCCESS':
        cancellation_time = order_response.get('time')
        logging.info(f"Order {order_id} canceled successfully.")
        # Log the order cancellation
        log_order_cancellation(order_id, cancellation_time)
        # Monitor the order status after cancellation
        monitor_order_status(order_id)
        # Send notifications (you can replace this with your notification logic)
        send_notification("Order Canceled", f"Order {order_id} canceled successfully.")
    else:
        logging.error(f"Order {order_id} cancellation failed: {order_response.get('message')}")
        # Log the error
        log_error(f"Error canceling order {order_id}: {order_response.get('message')}")
        # Send error notification
        send_notification("Order Cancellation Failed",
                          f"Error canceling order {order_id}: {order_response.get('message')}")


def handle_error(e):
    """
    Handle threading error.

    Args:
        e (Exception): Exception raised during thread running.
    """
    logging.error(f"Threading error occurred: {str(e)}")
    # Log the exception
    log_error(f"Exception during execution system thread runs{str(e)}")

    # Send error notification
    send_notification("Execution System Thread Running Error",
                      f"Exception during thread runs {str(e)}")


def handle_cancellation_error(order_id, e):
    """
    Handle cancellation error.

    Args:
        order_id (str): ID of the order.
        e (Exception): Exception raised during cancellation.
    """
    logging.error(f"Error canceling order {order_id}: {str(e)}")

    # Log the exception
    log_error(f"Exception during order cancellation {order_id}: {str(e)}")

    # Send error notification
    send_notification("Order Cancellation Error",
                      f"Exception during order cancellation {order_id}: {str(e)}")


def handle_modification_error(order_id, e):
    """
    Handle modification error.

    Args:
        order_id (str): ID of the order.
        e (Exception): Exception raised during modification.
    """
    logging.error(f"Error modifying order {order_id}: {str(e)}")

    # Log the exception
    log_error(f"Exception during order modification {order_id}: {str(e)}")

    # Send error notification
    send_notification("Order Modification Error",
                      f"Exception during order modification {order_id}: {str(e)}")


def handle_execution_error(order_id, e):
    """
    Handle execution error.

    Args:
        order_id (str): ID of the order.
        e (Exception): Exception raised during execution.
    """
    logging.error(f"Error executing order {order_id}: {str(e)}")

    # Log the exception
    log_error(f"Exception during order execution {order_id}: {str(e)}")

    # Send error notification
    send_notification("Order Execution Error",
                      f"Exception during order execution {order_id}: {str(e)}")


def log_order_modification(order_id, creation_time):
    """
    Log the order modification details.

    Args:
        order_id (str): ID of the order.
        creation_time (str): time of the order was created
    """
    logging.info(f"Order {order_id} executed at {creation_time}.")


def log_order_cancellation(order_id, cancellation_time):
    """
    Log the order cancellation details.

    Args:
        order_id (str): ID of the order.
        cancellation_time (str): time of the order was canceled
    """
    logging.info(f"Order {order_id} canceled at {cancellation_time}.")


def log_order_execution(order_id, execution_time):
    """
    Log the order execution details.

    Args:
        order_id (str): ID of the order.
        execution_time (str): time of the order was executed
    """
    logging.info(f"Order {order_id} executed at {execution_time}.")


def log_error(error_message):
    """
    Log the error details.

    Args:
        error_message (str): the error of functions which should be logged.
    """
    logging.error(f"Error: {error_message}")


def send_notification(title, message):
    """
    Send a notification.

    Args:
        title (str): title of the message which should be sent to the user
        message (str): message sent to the user
    """
    logging.info(f"Notification - Title: {title}, Message: {message}")


def monitor_order_status(order_id):
    """
    Monitor the order status for further actions.

    Args:
        order_id (str): ID of the order.

    TODO: Implement the monitoring logic.
    """
    # Placeholder for monitoring logic
    logging.info(f"Monitoring order {order_id} status.")


class ExecutionSettings:
    def __init__(self, transaction_fee, slippage):
        """
        Initialize the Execution_settings object with transaction fee and slippage.

        :param transaction_fee: The cost per transaction.
        :param slippage: The allowed slippage for trade execution.

        TODO: more settings may include
        """
        self.transaction_fee = transaction_fee
        self.slippage = slippage

    def set_transaction_fee(self, transaction_fee):
        """
        Set the transaction fee.

        :param transaction_fee: The new transaction fee.
        """
        self.transaction_fee = transaction_fee

    def set_slippage(self, slippage):
        """
        Set the slippage.

        :param slippage: The new slippage.
        """
        self.slippage = slippage


class OrderExecutionThread(threading.Thread):
    def __init__(self, executing_system, order_queue):
        super().__init__()
        self.executing_system = executing_system
        self.order_queue = order_queue
        self.stop_event = threading.Event()

    def run(self):
        while not self.stop_event.is_set():
            try:
                order = self.order_queue.get(timeout=1)  # 获取订单，设置超时时间
                if order is not None:
                    # 执行订单
                    self.executing_system.execute_order(order)
            except queue.Empty:
                continue

    def stop(self):
        self.stop_event.set()


class ExecutingSystem:
    def __init__(self, order_waitlist=None, system_status='on'):
        """
        Initialize the ExecutingSystem.

        Args:
            order_waitlist (list): List of orders to wait for execution.
            system_status (str): The system status.
        """
        self.current_volume = None
        self.current_price = None

        if order_waitlist is None:
            order_waitlist = []
        self.order_waitlist = order_waitlist
        self.system_status = system_status

        # define execution_thread
        self.execution_thread = None
        self.lock = threading.Lock()
        self.order_queue = queue.Queue()

    def run(self):
        """
        Start the system.

        This method starts the order execution thread if the system status is 'on'.
        """
        try:
            if self.system_status == 'on':
                # 启动订单执行线程
                self.execution_thread = OrderExecutionThread(self, self.order_queue)
                self.execution_thread.start()
            else:
                logging.error("Cannot start system: System status is not 'on'.")

        except Exception as e:
            handle_error(e)

    def stop(self):
        """
        Stop the system.

        This method stops the order execution thread if it is running.
        """
        try:
            if self.execution_thread and self.execution_thread.is_alive():
                # 停止订单执行线程
                self.execution_thread.stop()
                self.execution_thread.join()
            else:
                logging.warning("No active execution thread to stop.")

        except Exception as e:
            handle_error(e)

    def set_sys_status(self, status):
        """
        Set the system status.

        Args:
            status (str): The new status of the system.
        """
        self.system_status = status

    def set_current_market(self, current_volume=None, current_price=None):
        """
        Set the current market parameters.

        Args:
            current_volume (float): The new current volume.
            current_price (float): The new current price.
        """
        if current_volume is not None and current_price is not None:
            self.current_volume = current_volume
            self.current_price = current_price
        else:
            logging.warning("Invalid parameters provided for updating current market parameters.")

    def executing_order(self, order_id, order_quantity):
        """
        Execute the order.

        Args:
            order_id (str): The ID of the order.
            order_quantity (float): The quantity of assets in the order.

        Returns:
            Tuple containing execution response and current volume after execution.
        """
        try:
            # Check if there is enough volume to execute the order
            if self.current_volume <= 0:
                logging.warning("Current volume is zero or negative. Exiting executing_order.")
                status = "PENDING"
                execution_time = datetime.now()
                exec_response = {
                    'status': status,
                    'order_id': order_id,
                    'time': execution_time,
                    'message': 'Current volume is zero or negative, simulated execution failed',
                    'executed_quantity': 0
                }
                remain_quantity = order_quantity
                return exec_response, status, execution_time, remain_quantity

            # Execute the order
            executed_quantity = min(self.current_volume, order_quantity)
            self.current_volume -= executed_quantity
            execution_time = datetime.now()

            # Define execution status and message
            if executed_quantity == order_quantity:
                status = "SUCCESS"
                message = 'Simulated execution is executed successfully'
                self.order_waitlist.remove(order_id)
            else:
                status = "PARTIAL"
                message = 'Simulated execution is partially executed'

            remain_quantity = order_quantity - executed_quantity

            exec_response = {
                'status': status,
                'order_id': order_id,
                'time': execution_time,
                'message': message,
                'executed_quantity': executed_quantity
            }

            return exec_response, status, execution_time, remain_quantity

        except Exception as e:
            logging.error(f"Error executing order: {e}")
            raise  # Re-raise the exception to propagate it further if needed

    def modifying_order(self, order_id):
        try:
            creation_time = datetime.now()
            # Create a response object
            modify_response = {
                'status': 'SUCCESS',
                'order_id': order_id,
                'time': creation_time,
                'message': 'Order modified successfully',
            }

            # Remove the executed order from the waitlist
            self.order_waitlist.remove(order_id)

            return modify_response, order_id, creation_time

        except Exception as e:
            # Handle the exception (e.g., log the error, send notification)
            logging.error(f"Error modifying order: {e}")
            raise  # Re-raise the exception to propagate it further if needed

    def cancelling_order(self, order_id):
        """
        Simulated cancellation for demonstration purposes.

        TODO: simulated cancellation
        """
        try:
            status = 'SUCCESS'
            cancellation_time = datetime.now()
            # Placeholder for simulated execution
            cancel_response = {
                'status': status,
                'order_id': order_id,
                'time': cancellation_time,
                'message': 'Order canceled successfully',
            }

            # Remove the executed order from the waitlist
            self.order_waitlist.remove(order_id)

            return cancel_response, status, cancellation_time

        except Exception as e:
            # Handle the exception (e.g., log the error, send notification)
            logging.error(f"Error modifying order: {e}")
            raise  # Re-raise the exception to propagate it further if needed

    def execute_order(self, order):
        """
        Execute the order logic.

        Args:
            order(Object): Object containing all args and methods of an order

        TODO: connecting to the trading platform
        TODO: place order
        """
        order_id = order.get_order_id()
        order_quantity = order.get_quantity()
        try:
            # Placeholder for connecting to the trading platform *
            # platform_connection = conn_exchange()

            # Placeholder for placing the order *
            # order_response = place_order(platform_connection, order)

            # Simulate order execution
            exec_response, status, execution_time, quantity = self.executing_order(order_id, order_quantity)
            order.execute(status, execution_time, quantity)

            # Log execution result
            process_execution_response(exec_response)
        except Exception as e:
            handle_execution_error(order_id, e)

    def modify_order(self, order, order_args):
        """
        Modify the order based on the provided order arguments.

        Args:
            order(Object): Object containing all args and methods of an order
            order_args (dict): Dictionary containing the modified order parameters.

        TODO: connecting to the trading platform
        TODO: place order
        """
        order_id = order.get_order_id()
        try:
            # Placeholder for connecting to the trading platform *
            # platform_connection = conn_exchange()

            # Placeholder for placing the order *
            # order_response = place_order(platform_connection, order)

            # Simulate order modification
            modify_response, order_id, creation_time = self.modifying_order(order_id)
            order.modify(order_args)

            process_modification_response(modify_response)

        except Exception as e:
            handle_modification_error(order_id, e)

    def cancel_order(self, order):
        """
        Cancel the order logic.

        Args:
            order(Object): Object containing all args and methods of an order

        TODO: connecting to the trading platform
        TODO: place order
        """
        order_id = order.get_order_id()
        try:
            # Placeholder for connecting to the trading platform *
            # platform_connection = conn_exchange()

            # Placeholder for placing the order *
            # order_response = place_order(platform_connection, order)

            # Simulate order cancellation
            cancel_response, status, cancellation_time = self.cancelling_order(order_id)
            order.cancel(status, cancellation_time)

            process_cancellation_response(cancel_response)

        except Exception as e:
            handle_cancellation_error(order_id, e)
