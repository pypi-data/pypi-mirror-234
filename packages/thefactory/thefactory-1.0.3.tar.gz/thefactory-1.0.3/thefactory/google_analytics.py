import json
import os
from datetime import datetime, timedelta

import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from mysql.connector import Error as MySQLError

from thefactory.config import DBasePool, create_sql_eng
from sqlalchemy import create_engine


def assemble_filters(filters):
    filter_clauses = []
    for filter_item in filters:
        field = f"ga:{filter_item['field']}"
        operator = filter_item.get('operator')
        values = filter_item.get('values', [])

        if operator == '==':
            filter_clause = ','.join([f"{field}=={val}" for val in values])
        elif operator == '!=':
            filter_clause = ','.join([f"{field}!={val}" for val in values])
        elif operator == '<':
            filter_clause = f"{field}<{'|'.join(values)}"
        # Add more conditions as needed
        else:
            continue  # Skip if the operator is not recognized

        filter_clauses.append(filter_clause)

    return ";".join(filter_clauses)


def get_date_range(custom_start=None, custom_end=None, days_back=7):
    """
    Return the start and end date for data fetching.
    If custom dates are provided, use those; otherwise, calculate based on the last 'days_back' days.

    :param custom_start: Custom start date in the format 'YYYY-MM-DD'
    :param custom_start: Custom start date in the format 'YYYY-MM-DD'
    :param custom_end: Custom end date in the format 'YYYY-MM-DD'
    :param days_back: Number of days back to go for the default date range
    :return: Tuple containing start_date and end_date in the format 'YYYY-MM-DD'
    """
    # If custom dates are provided, use those
    if custom_start and custom_end:
        return custom_start, custom_end

    # Otherwise, calculate dates
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days_back)

    return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')


def daterange(start_date, end_date):
    """
    Generate a sequence of dates from start_date to end_date.

    :param start_date: Start date in the format 'YYYY-MM-DD'
    :param end_date: End date in the format 'YYYY-MM-DD'
    :return: Generator yielding dates in the sequence
    """
    current_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    while current_date <= end_date:
        yield current_date.strftime('%Y-%m-%d')
        current_date += timedelta(days=1)


class GoogleAnalyticsProcessor:
    def __init__(self, profile_id, db_name):
        self.profile_id = profile_id
        self.db_name = db_name
        self.engine = create_engine(create_sql_eng(self.db_name))
        self.db_pool = DBasePool(dbase=db_name)  # Single instance for all methods
        self.credentials = self.get_credentials()
        self.service = build('analyticsreporting', 'v4', credentials=self.credentials)

    # Your get_credentials function
    def get_credentials(self):
        """
        Fetch credentials for the given profile ID using the database pool.
        :return: Google API Credentials object
        """
        sql = f"""SELECT key_file_location
                  FROM google_analytics.profiles
                  WHERE id = %(p_id)s"""

        with self.db_pool.connection() as (conn, curs):
            curs.execute(sql, {"p_id": self.profile_id})
            (key_file_location,) = curs.fetchone()

        credentials = Credentials.from_service_account_file(key_file_location)

        return credentials

    # Your main run_ga_query function
    # Assuming you've imported Google Analytics API v4 Client Library and your utility functions
    def truncate_output_table(self, table_name):
        """
        Truncate the given table using the provided database connection.
        :param table_name: The name of the table to truncate
        """
        if self.table_exists(table_name):
            with self.db_pool.connection() as (conn, curs):
                truncate_query = f"TRUNCATE {self.db_name}.{table_name}"
                curs.execute(truncate_query)
                conn.commit()

    def run_ga_query(self, table_name, dimensions, metrics, filters, start_date, end_date):
        """
        Run a Google Analytics query with the given parameters.

        :param table_name: The staging table
        :param dimensions: List of dimensions
        :param metrics: List of metrics
        :param filters: Filters to apply
        :param start_date: Start date for data fetch
        :param end_date: End date for data fetch
        :return: Query result data
        """
        if not self.table_exists(table_name):
            self.create_table_if_not_exists(table_name, dimensions, metrics)
        query = {
            'viewId': self.profile_id,
            'dimensions': [{'name': f'ga:{dim["name"]}'} for dim in dimensions],
            'metrics': [{'expression': f'ga:{met["name"]}'} for met in metrics],
        }
        filter_str = assemble_filters(filters)
        if filter_str:
            query['filtersExpression'] = filter_str
        for single_date in daterange(start_date, end_date):
            query['dateRanges'] = [{'startDate': single_date, 'endDate': single_date}]
            next_page_token = ''  # Initialize to an empty string to enter the loop

            while next_page_token is not None:
                query['pageToken'] = next_page_token if next_page_token else None

                try:
                    # 4. Execute the query
                    response = self.service.reports().batchGet(
                        body={
                            'reportRequests': [query]
                        }
                    ).execute()

                    # 5. Check for next page token
                    next_page_token = response.get("reports", [{}])[0].get("nextPageToken", None)

                    # 6. Parse and insert the data
                    for report in response.get("reports", []):
                        row_data = [row["dimensions"] + row["metrics"][0]["values"] for row in
                                    report.get("data", {}).get("rows", [])]
                        column_names = [name.replace('ga:', '') for name in (report['columnHeader']['dimensions'] +
                                                                             [entry['name'] for entry in
                                                                              report['columnHeader']['metricHeader'][
                                                                                  'metricHeaderEntries']])]

                        self.do_data(data=row_data, table_name=table_name, columns=column_names)

                except HttpError as e:
                    print(f"An error occurred: {e}")
                    break

    def create_table_if_not_exists(self, table_name, dimensions, metrics):
        # Check if table exists
        if not self.table_exists(table_name):
            # Read GA field metadata from central config (however you've decided to store it)
            current_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(current_dir, 'ga_field_metadata.json')
            with open(json_path, 'r') as f:
                ga_field_metadata = json.load(f)

            # Build table creation query
            query = f"CREATE TABLE {self.db_name}.{table_name} ("
            for dimension in dimensions:
                field_info = ga_field_metadata['dimensions'].get(dimension['name'])
                if field_info:
                    if field_info['format'].lower() == 'string':
                        query += f"{dimension['name']} VARCHAR({field_info['length']}),"
                    elif field_info['format'].lower() == 'float':
                        query += f"{dimension['name']} FLOAT,"
                    elif field_info['format'].lower() == 'integer':
                        query += f"{dimension['name']} INT,"
                    elif field_info['format'].lower() == 'datetime':
                        query += f"{dimension['name']} DATETIME,"
                    elif field_info['format'].lower() == 'date':
                        query += f"{dimension['name']} DATE,"

            for metric in metrics:
                field_info = ga_field_metadata['metrics'].get(metric['name'])
                if field_info:
                    if field_info['format'].lower() == 'string':
                        query += f"{metric['name']} VARCHAR({field_info['length']}),"
                    elif field_info['format'].lower() == 'float':
                        query += f"{metric['name']} FLOAT,"
                    elif field_info['format'].lower() == 'integer':
                        query += f"{metric['name']} INT,"
                    elif field_info['format'].lower() == 'datetime':
                        query += f"{metric['name']} DATETIME,"
                    elif field_info['format'].lower() == 'date':
                        query += f"{metric['name']} DATE,"

            query = query.rstrip(",")  # Remove trailing comma
            query += ");"  # Close the SQL command

            # Execute table creation query
            self.execute_query(query)

    def table_exists(self, table_name):
        try:
            with self.db_pool.connection() as (conn, curs):
                curs.execute(
                    f"""SELECT COUNT(*)
    FROM information_schema.tables
    WHERE table_schema = '{self.db_name}'
      AND table_name = '{table_name}'""")
                result = curs.fetchone()
                return result[0] == 1
        except MySQLError as e:
            print(f"An error occurred: {e}")
            return False

    def execute_query(self, query):
        try:
            with self.db_pool.connection() as (conn, curs):
                curs.execute(query)
                conn.commit()
        except MySQLError as e:
            print(f"An error occurred: {e}")

    def do_data(self, data, table_name, columns):
        df = pd.DataFrame(data, columns=columns)
        """
        Insert the data into the given table.

        :param data: The data to insert
        :param table_name: The table into which to insert the data
        """
        # Convert the list of lists to a DataFrame

        # Assuming you have a method or a way to map GA fields to your database types
        # Something like this: self.get_db_field_types()

        # Convert types as needed, e.g., date strings to datetime objects
        # Here, you'd apply whatever type conversions are necessary

        # Insert data into the table
        try:
            with self.db_pool.connection() as (conn, curs):
                df.to_sql(name=table_name, con=self.engine, if_exists='append', index=False)
        except Exception as e:
            print(f"An error occurred while inserting data: {e}")
