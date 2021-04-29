"""
CS3250 Project. Includes Discord Chat Bot and CSV Reader.

Usage:
    main.py [--csv_path=<csv_path>]
    main.py [--csv_path=<csv_path>] [--db=<db>] [--create=<create>]
    main.py [--csv_path=<csv_path>] [--table=<table>]
    main.py [--csv_path=<csv_path>] [--headers=<headers>]
    main.py [--csv_path=<csv_path>] [--table=<table>] [--headers=<headers>]
    main.py [--csv_path=<csv_path>] [--headers=<headers>] [--table=<table>]
    main.py [--csv_path=<csv_path>] [--db=<db>] [--headers=<headers>] [--table=<table>] [--create=<create>]
    main.py [--csv_path=<csv_path>] [--headers=<headers>] [--db=<db>] [--table=<table>] [--create=<create>]
    main.py [--csv_path=<csv_path>] [--headers=<headers>] [--table=<table>] [--db=<db>] [--create=<create>]
    main.py [--csv_path=<csv_path>] [--table=<table>] [--headers=<headers>] [--db=<db>] [--create=<create>]
    main.py [--csv_path=<csv_path>] [--table=<table>] [--db=<db>] [--headers=<headers>] [--create=<create>]

Options:
  -h --help                Show this screen.
  --version                Show version.
  --headers=<headers>      Headers for the db file in the order they appear
  --db=<db>                Database to use
  --create=<create>        Tells the program to create the database
  --csv_path=<csv_path>    Path to the product data csv for initializing the database
"""

import json
import os
import threading

from docopt import docopt

from bot import discordbot
from db.io.manager import write_csv_to_sql
from db.sql.connection.singleton import Database
from orders.handler import create_order_table
from user.handler import create_users_table
from website.manage import website


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


def start_discord(arguments):
    """
    Starts the discord application using the command line.

    :param arguments:   Arguments from docopt
    """
    database = arguments.get("--db", "db.sqlite3")
    headers = arguments.get("--headers", None)
    csv = arguments.get("--csv_path", None)
    create = arguments.get("--create", "False")
    if csv and create.lower() == "true":
        if headers:
            headers = json.loads(headers)
        else:
            headers = {
                "product_id": "varchar",
                "quantity": "integer",
                "wholesale_price": "double precision",
                "sale_price": "double precision",
                "supplier_id": "varchar"
            }
        build_db(database, "products", headers)
        create_order_table()
        create_users_table()
        upload_csv(headers.keys(), has_headers=True)
    discordbot.start()


def start_website():
    """
    Start the associated statistics website
    """
    website()


if __name__ == "__main__":
    arguments = docopt(__doc__, version='Database Project 0.1')
    threads = []
    discord_thread = threading.Thread(target=start_discord, args=(arguments, ))
    discord_thread.daemon = True
    threads.append(discord_thread)
    website_thread = threading.Thread(target=start_website)
    threads.append(website_thread)
    threads[0].start()
    #threads[1].start()
    threads[0].join()
    #threads[1].join()
