"""
Entry point utilities for reading db and storing in sql
"""
import dateparser

from db.crud.executor import create_records
from db.io.sink import CSVSink
from db.io.source import CSVSource
from db.sql.connection.singleton import Database
from db.sql.query.builder import Select, Create


def prepare_batch(batch, mappings):
    """
    Prepare the batch. Make necessary alterations to data.

    Field mappings have the form
     {
        "product_id": "varchar",
        "cost": "double",
        "quantity": "integer",
        "date": "utc"
    }

    UTC forces a string to a UTC integer timestamp.

    :param batch:   The batch to transform
    :param mappings:    Mappings to enforce
    :return: Prepared batch
    """
    out_batch = []
    keys = mappings.keys()
    for record in batch:
        for key in keys:
            data_type = mappings[key]
            data_val = record.get(key, None)
            if data_val:
                if isinstance(data_val, str) \
                        and data_type == "utc":
                    try:
                        data_val = dateparser.parse(data_val)
                        if data_val:
                            record[key] = data_val.timestamp()
                        else:
                            record[key] = None
                    except Exception as e:
                        record[key] = None
        out_batch.append(record)
    return out_batch


def write_csv_to_sql(
        filepath,
        db=":memory:",
        table="products",
        headers=None,
        has_headers=False,
        table_mappings=None,
        batch_size=100,
        csv_mappings=None):
    """
    Writes a given CSV to a table

    Field mappings have the form
     {
        "product_id": "varchar",
        "cost": "double",
        "quantity": "integer"
    }

    :param filepath:    The file path
    :param db:  The database object
    :param table:   Name of the table
    :param headers: Headers list in the order they appear in the db
    :param has_headers: The headers
    :param table_mappings:  Table mappings for creation or None to avoid table creation
    :param batch_size:  Number of records per batch
    :param csv_mappings: If present, forces the mappings to conform
    """
    _conn = Database.instance(db, table, table_mappings)
    csv_headers = None
    if has_headers is False:
        csv_headers = headers
    elif headers:
        csv_headers = headers
    csv = CSVSource(filepath, headers=csv_headers, has_headers=has_headers, batch_size=batch_size)
    try:
        for batch in csv:

            if len(batch) > 0:
                if has_headers:
                    record = batch[0]
                    if csv_headers is None:
                        headers = record.keys()
                    else:
                        csv_headers = headers
                query = Create(table, headers)
                if csv_mappings:
                    batch = prepare_batch(batch, csv_mappings)
                create_records(headers, query, batch)
    finally:
        csv.close()


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
