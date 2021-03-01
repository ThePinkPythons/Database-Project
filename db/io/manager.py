"""
Entry point utilities for reading db and storing in sql
"""

import sqlite3

from db.crud.executor import create_records
from db.io.source import CSVSource
from db.sql.connection.singleton import Database


def write_csv_to_sql(filepath, db=":memory:", table="products", headers=None, table_mappings=None, batch_size=100):
    """
    Writes a given CSV to a table

    :param filepath:    The file path
    :param db:  The database object
    :param table:   Name of the table
    :param headers: Headers list in the order they appear in the db
    :param table_mappings:  Table mappings for creation or None to avoid table creation
    :param batch_size:  Number of records per batch
    """
    db = Database.instance(db, table, table_mappings)
    csv = CSVSource(filepath, headers=headers, batch_size=batch_size)
    for batch in csv:
        create_records(db, batch)


def read_csv_from_sql(db, sql, fpath, table="products"):
    """
    Writes the db file stored in the database to the file

    :param db: The db to write
    :param fpath:   The file path
    :param table:   The table to insert into
    """
    pass
