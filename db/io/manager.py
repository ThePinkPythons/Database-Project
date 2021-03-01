"""
Entry point utilities for reading db and storing in sql
"""

from db.crud.executor import create_records
from db.io.sink import CSVSink
from db.io.source import CSVSource
from db.sql.connection.singleton import Database
from db.sql.query.builder import Select


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
    conn = Database.instance(db, table, table_mappings)
    csv = CSVSource(filepath, headers=headers, batch_size=batch_size)
    for batch in csv:
        create_records(conn, batch)


def write_csv_from_sql(db, headers, fpath, table="products", batch_size=10000):
    """
    Writes the db file stored in the database to the file

    :param db: The db to write
    :param headers: The headers to use in the select
    :param fpath:   The file path
    :param table:   The table to insert into
    """
    conn = Database.instance(db)
    c = conn.cursor()
    csv = CSVSink(fpath, headers)
    select = Select(table, headers)
    select = str(select)
    batch = []
    for record in c.execute(str(select)):
        rdict = dict(zip(headers, record))
        batch.append(rdict)
        if len(batch) > batch_size:
            csv.write_rows(batch)
            batch = []
    if len(batch) > 0:
        csv.write_rows(batch)
    csv.close()
    del batch
