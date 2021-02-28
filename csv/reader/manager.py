"""
Entry point utilities for reading csv and storing in sql
"""

import sqlite3

from csv.reader.csv import CSVSource


def read_csv_to_sql(filepath, db, table, headers=None):
    """
    Reads the csv from the file path to the specified table

    :param filepath:    The file path
    :param db:  The database object
    :param table:   Name of the table
    :param headers: Headers list in the order they appear in the csv
    """
    csv = CSVSource(filepath)
    for row in csv:
        print(row)


def write_csv_from_sql(db, fpath,table="products"):
    """
    Writes the csv file stored in the database to the file

    :param csv: The csv to write
    :param fpath:   The file path
    :param table:   The table to insert into
    """
    pass
