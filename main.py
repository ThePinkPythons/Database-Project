"""
CS3250 Project. Includes Discord Chat Bot and CSV Reader

Usage:
    main.py <csv_path>
    main.py <csv_path> [--db=<db>]
    main.py <csv_path> [--table=<table>]
    main.py <csv_path> [--headers=<headers>]
    main.py <csv_path> [--table=<table>] [--headers=<headers>]
    main.py <csv_path> [--headers=<headers>] [--table=<table>]
    main.py <csv_path> [--db=<db>] [--headers=<headers>] [--table=<table>]
    main.py <csv_path> [--headers=<headers>] [--db=<db>] [--table=<table>]
    main.py <csv_path> [--headers=<headers>] [--table=<table>] [--db=<db>]
    main.py <csv_path> [--table=<table>] [--headers=<headers>] [--db=<db>]
    main.py <csv_path> [--table=<table>] [--db=<db>] [--headers=<headers>]

Options:
  -h --help                Show this screen.
  --version                Show version.
  --table=<table>          Name of the table in sqlite3
  --headers=<headers>      Headers for the db file in the order they appear
  --db=<db>                Database to use
"""
#import json

#from docopt import docopt
import os

from bot import discordBot
from db.io.manager import write_csv_to_sql
from db.sql.connection.singleton import Database
from orders.handler import create_order_table
from user.handler import create_users_table


def build_db(database, table, headers):
    """
    Build the productdata store

    :param database:    The database
    :param table:   Table to use
    :param headers: Headers to use
    :return: A prebuilt database object
    """
    Database.instance(database, table, headers)


def upload_csv(headers, has_headers):
    """
    Upload the CSV file

    :param headers: Any headers
    :param has_headers: Whether there are headers in the csv
    """
    fpath = os.getcwd()
    fpath = os.path.sep.join([fpath, "productdata", "product_data.csv"])
    write_csv_to_sql(fpath, headers=headers, has_headers=has_headers)


if __name__ == "__main__":
    #arguments = docopt(__doc__, version='Database Project 0.1')
    #database = arguments.get("--database", "project.db")
    #table = arguments.get("--table", "productdata")
    #headers = arguments.get("--headers", None)
    #if headers:
    #    headers = json.loads(headers)
    headers = {
        "product_id": "varchar",
        "quantity": "integer",
        "wholesale_price": "double precision",
        "sale_price": "double precision",
        "supplier_id": "varchar"
    }
    build_db(":memory:", "products", headers)
    create_order_table()
    create_users_table()
    upload_csv(headers.keys(), has_headers=True)
    discordBot.start()
