#!/usr/bin/env python3

"""Provide a generic class to interact with an sqlite3 database."""

import os
import sqlite3 as s3
import syslog
import time
import traceback

import pandas as pd

from . import funfile as mf


class SqlDatabase:  # pylint: disable=R0902
    """A class to interact with SQLite3 databases."""

    def __init__(
        self,
        database=".local/databasefile.sqlite3",
        schema=None,
        table=None,
        insert=None,
        debug=False,
    ):
        self.debug = debug
        self.home = os.environ["HOME"]
        self.version = 3.0
        self.database = database
        self.schema = schema
        self.table = table
        self.sql_insert = insert
        self.sql_query = None
        self.dataq = []
        self.db_version = self._test_db_connection()

    def _test_db_connection(self):
        """Print the version of the database.

        Returns:
            None
        """
        consql = None
        try:
            consql = s3.connect(self.database, timeout=9000)
        except s3.Error as her:
            mf.syslog_trace(
                # pylint: disable-next=C0301
                f"Unexpected SQLite3 error of type {type(her).__name__} when connecting to server.",
                syslog.LOG_CRIT,
                self.debug,
            )
            mf.syslog_trace(traceback.format_exc(), syslog.LOG_CRIT, self.debug)
            if consql:  # attempt to close connection to sqlite3 server
                consql.close()
                mf.syslog_trace(" ** Closed SQLite3 connection. **", False, self.debug)
            raise
        cursor = consql.cursor()
        try:
            cursor.execute("SELECT sqlite_version();")
            versql = cursor.fetchone()
            cursor.close()
            consql.commit()
            consql.close()
            mf.syslog_trace(
                f"Attached to SQLite3 server: {versql}", syslog.LOG_INFO, self.debug
            )
            mf.syslog_trace(
                f"Using DB file             : {self.table}@{self.database}",
                syslog.LOG_INFO,
                self.debug,
            )
        except s3.Error as her:
            mf.syslog_trace(
                f"Unexpected SQLite3 error of type {type(her).__name__} during test.",
                syslog.LOG_CRIT,
                self.debug,
            )
            mf.syslog_trace(traceback.format_exc(), syslog.LOG_CRIT, self.debug)
            raise
        return versql

    def queue(self, data):
        """Append data to the queue for insertion.

        Args:
            data (dict): data to be inserted

        Returns:
            None
        """
        if isinstance(data, dict):
            self.dataq.append(data)
            mf.syslog_trace(f"Queued : {data}", False, self.debug)
        else:
            mf.syslog_trace("Data must be a dictionary!", syslog.LOG_CRIT, self.debug)
            raise TypeError

    def insert(self, method="ignore", index="sample_time"):
        """Commit queued data to the database.

        Args:
            method (str):   how to handle duplicates in the database.
                            Possible options are:
                            'ignore' (database will not be changed) or
                            'replace' (existing data will be removed and new data inserted).
            index (str):    name of the field to be used as the index.

        Returns:
            None

        Raises:
            ValueError: if <sql_insert> is not defined
            sqlite3.Error: when commit fails serverside
            Exception: to catch unknown errors during the exchange
        """
        consql = None
        if not self.insert:
            raise ValueError("No instruction provided")

        try:
            consql = s3.connect(self.database, timeout=9000)
        except s3.Error as her:
            mf.syslog_trace(
                # pylint: disable-next=C0301
                f"Unexpected SQLite3 error of type {type(her).__name__} when connecting to server.",
                syslog.LOG_CRIT,
                self.debug,
            )
            mf.syslog_trace(traceback.format_exc(), syslog.LOG_CRIT, self.debug)
            if consql:  # attempt to close connection to sqlite3 server
                consql.close()
                mf.syslog_trace(" ** Closed SQLite3 connection. **", False, self.debug)
            raise

        while self.dataq:
            element = self.dataq[0]
            df_idx = index  # list(element.keys())[0]    # this should always be 'sample_time'
            df = pd.DataFrame(element, index=[df_idx])
            try:
                df.to_sql(name=self.table, con=consql, if_exists="append", index=False)
                mf.syslog_trace(f"Inserted : \n{df}\n", False, self.debug)
            except s3.IntegrityError:
                # probably "sqlite3.IntegrityError: UNIQUE constraint failed".
                # this can be passed
                if method == "ignore":
                    mf.syslog_trace(
                        "Duplicate entry. Not adding to database.", False, self.debug
                    )
                if method == "replace":
                    element_time = element[f"{df_idx}"]
                    sql_command = f'DELETE FROM {self.table} WHERE {df_idx} = "{element_time}";'
                    cursor = consql.cursor()
                    try:
                        cursor.execute(sql_command)
                        cursor.fetchone()
                        cursor.close()
                        consql.commit()
                    except s3.IntegrityError:
                        pass
                        # probably "sqlite3.IntegrityError: UNIQUE constraint failed".
                        # this can be passed
                    except s3.Error as her:
                        mf.syslog_trace(
                            # pylint: disable-next=C0301
                            f"SQLite3 error of type {type(her).__name__} when commiting to server.",
                            syslog.LOG_ERR,
                            self.debug,
                        )
                        mf.syslog_trace(traceback.format_exc(), syslog.LOG_ERR, self.debug)
                        raise
                    df.to_sql(name=self.table, con=consql, if_exists="append", index=False)
                    mf.syslog_trace(f"Replaced : \n{df}\n", False, self.debug)
            except s3.Error as her:
                mf.syslog_trace(
                    f"SQLite3 error of type {type(her).__name__} when commiting to server.",
                    syslog.LOG_ERR,
                    self.debug,
                )
                mf.syslog_trace(traceback.format_exc(), syslog.LOG_ERR, self.debug)
                raise
            except Exception as her:
                mf.syslog_trace(
                    f"Unexpected error of type {type(her).__name__} !",
                    syslog.LOG_ERR,
                    self.debug,
                )
                mf.syslog_trace(traceback.format_exc(), syslog.LOG_ERR, self.debug)
                raise
            self.dataq.pop(0)

        consql.close()

    def latest_datapoint(self):
        """
        Look up last entry in the database table.

        Returns:
            date and time of the youngest entry in the table
        """
        consql = None
        try:
            consql = s3.connect(self.database, timeout=9000)
        except s3.Error as her:
            mf.syslog_trace(
                # pylint: disable-next=C0301
                f"Unexpected SQLite3 error of type {type(her).__name__} when connecting to server.",
                syslog.LOG_CRIT,
                self.debug,
            )
            mf.syslog_trace(traceback.format_exc(), syslog.LOG_CRIT, self.debug)
            if consql:  # attempt to close connection to sqlite3 server
                consql.close()
                mf.syslog_trace(" ** Closed SQLite3 connection. **", False, self.debug)
            raise
        cursor = consql.cursor()
        try:
            cursor.execute(f"SELECT MAX(sample_epoch) from {self.table};")
            max_epoch = cursor.fetchone()
            human_epoch = time.localtime(max_epoch[0])
            cursor.close()
            consql.commit()
            consql.close()
            mf.syslog_trace(
                f"Latest datapoint in {self.table}: "
                f"{max_epoch[0]} = {time.strftime('%Y-%m-%d %H:%M:%S', human_epoch)}",
                False,
                self.debug,
            )
        except s3.Error as her:
            mf.syslog_trace(
                f"Unexpected SQLite3 error of type {type(her).__name__} during test.",
                syslog.LOG_CRIT,
                self.debug,
            )
            mf.syslog_trace(traceback.format_exc(), syslog.LOG_CRIT, self.debug)
            raise
        return time.strftime("%Y-%m-%d %H:%M:%S", human_epoch)
