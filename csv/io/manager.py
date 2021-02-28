"""
Entry point utilities for reading csv and storing in sql
"""

import sqlite3

from csv.io.source import CSVSource


def write_csv_to_sql(filepath, db, table="products", headers=None):
    """
    Writes a given CSV to a table

    :param filepath:    The file path
    :param db:  The database object
    :param table:   Name of the table
    :param headers: Headers list in the order they appear in the csv
    """
    csv = CSVSource(filepath)
    for row in csv:
        print(row)


def read_csv_from_sql(db, sql, fpath, table="products"):
    """
    Writes the csv file stored in the database to the file

    :param csv: The csv to write
    :param fpath:   The file path
    :param table:   The table to insert into
    """
    pass
