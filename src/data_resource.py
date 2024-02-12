#!/usr/bin/python3
# -*- coding: utf-8 -*-

# dataloader.py

import pandas as pd
import pymysql
import logging

logging.basicConfig(level=logging.INFO)


def load_csv(file_path):
    """
    Load data from a CSV file and return a Pandas DataFrame.

    :param file_path: Path to the CSV file.
    :return: Pandas DataFrame containing the loaded data.
    """
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        logging.error(f"Error loading data from CSV: {e}")
        return None


def load_excel(file_path):
    """
    Load data from an Excel file and return a Pandas DataFrame.

    :param file_path: Path to the Excel file.
    :return: Pandas DataFrame containing the loaded data.
    """
    try:
        data = pd.read_excel(file_path)
        return data
    except Exception as e:
        logging.error(f"Error loading data from Excel: {e}")
        return None


def load_database(connection_string, query):
    """
    Load data from a data source using a SQL query and return a Pandas DataFrame.

    :param connection_string: Database connection string.
    :param query: SQL query to retrieve the data.
    :return: Pandas DataFrame containing the loaded data.
    """
    try:
        # Parse the connection string to extract database-related information
        db_info = connection_string.split('/')
        user, password, host, database = db_info

        # Create a database connection
        connection = pymysql.connect(
            user=user,
            password=password,
            host=host,
            database=database
        )

        # Execute the query and retrieve data
        data = pd.read_sql_query(query, connection)

        # Close the database connection
        connection.close()

        return data
    except Exception as e:
        logging.error(f"Error loading data from the data source: {e}")
        return None


class DataSource:
    def __init__(self, data_path, start_date=None, end_date=None):
        if start_date is None or end_date is None:
            self.set_date_range(start_date, end_date)
        self.end_date = start_date
        self.start_date = end_date
        self.data_path = data_path
        self.data = None

    def set_date_range(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        logging.info("Date range has changed:")
        logging.info(f"Start date: {self.start_date}")
        logging.info(f"End date: {self.end_date}")

    def auto_set_date_range(self):
        try:
            if self.data is not None:
                data = self.data
                date_column = next((col for col in data.columns if 'date' in col.lower()), None)
                if date_column is not None:
                    data.rename(columns={date_column: 'date'}, inplace=True)
                    start_date = data['date'].min()
                    end_date = data['date'].max()
                    self.start_date = start_date
                    self.end_date = end_date
                logging.info("Parameters 'start_date', 'end_date' may not be filled, "
                             "use the first date and the end date of given data as default!")
                logging.info("Call function: 'set_date_range' if you want to set the date range yourself.")

        except Exception as e:
            logging.error(f"Unexpected error in auto_set_date_range: {e}")

    def load_data(self):
        """
        Load data based on the data source type.

        :return: Pandas DataFrame containing the loaded data.
        TODO: download data if no local data was found
        """
        data = None
        try:
            if self.data_path.endswith('.csv'):
                data = load_csv(self.data_path)
            elif self.data_path.endswith(('.xls', '.xlsx')):
                data = load_excel(self.data_path)
            elif self.data_path.startswith('data_source://'):
                # Assuming data_source connection string and query are specified in the data_path
                connection_string, query = self.data_path.split('://')[1].split('/')
                data = load_database(connection_string, query)

            if data is not None:
                self.data = data

            if self.start_date is None and self.end_date is None:
                self.auto_set_date_range()

            return data

        except Exception as e:
            logging.error(f"Error loading data: {e}")
            return None

    def get_data_column(self, column_name):
        # Get specific historical market data
        if self.data is not None and column_name in self.data.columns:
            return self.data[column_name]
        else:
            logging.warning(f"{column_name} does not exist in data or data is None")
            return None

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def get_historical_data(self):
        try:
            historical_data = self.load_data()
            return historical_data
        except Exception as e:
            logging.error(f"Error get historical data: {e}")
            raise  # Re-raise the exception to propagate it further if needed
