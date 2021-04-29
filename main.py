"""
CS3250 Project. Includes Discord Chat Bot and CSV Reader.

Usage:
    main.py [--csv_path=<csv_path>] [--website_only|--discord_only]
    main.py [--csv_path=<csv_path>] [--db=<db>] [--create=<create>] [--website_only|--discord_only]
    main.py [--csv_path=<csv_path>] [--table=<table>] [--website_only|--discord_only]
    main.py [--csv_path=<csv_path>] [--headers=<headers>] [--website_only|--discord_only]
    main.py [--csv_path=<csv_path>] [--table=<table>] [--headers=<headers>] [--website_only|--discord_only]
    main.py [--csv_path=<csv_path>] [--headers=<headers>] [--table=<table>] [--website_only|--discord_only]
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
  --website_only           Start only the analytics website
  --discord_only           Only start the discord app
"""

import json
import logging
import os
import sys
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
    # set logger
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

    # get arguments from docopt
    arguments = docopt(__doc__, version='Database Project 0.1')
    logging.info("Database Project 0.1")
    threads = []
    website_thread = None
    discord_thread = None

    # create threads
    if arguments.get("--discord_only", False) or arguments.get("--website_only", False):
        logging.info("Creating Discord Thread")
        discord_thread = threading.Thread(target=start_discord, args=(arguments,))
        discord_thread.daemon = True
        discord_thread.start()
        discord_thread.join()
    elif arguments.get("--website_only", False) or arguments.get("--discord_only", False):
        logging.info("Creating Website Thread")
        website_thread = threading.Thread(target=start_website)
        website_thread.start()
        website_thread.join()

    # start threads
    logging.info("Starting Threads")
    if discord_thread:
        discord_thread.start()
    if website_thread:
        website_thread.start()

    # wait for threads to terminate
    logging.info("Waiting for Threads to Complete")
    if discord_thread:
        discord_thread.join()
    if website_thread:
        website_thread.join()
