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
    main.py [--write_csv=<out_path>] [--db=<db>]
    main.py [--db_only] [--csv_path=<csv_path>]

Options:
  -h --help                Show this screen.
  --version                Show version.
  --headers=<headers>      Headers for the db file in the order they appear
  --db=<db>                Database to use
  --create=<create>        Tells the program to create the database
  --csv_path=<csv_path>    Path to the product data csv for initializing the database
  --website_only           Start only the analytics website
  --discord_only           Only start the discord app
  --write_csv=<out_dir>    Tells the program to simply write out the sqllite3 database to csvs in the output folder.
  --db_only                Only create the database
"""
import datetime
import json
import logging
import os
import subprocess
import sys
import threading

from docopt import docopt

from bot import discordbot
from db.io.manager import write_csv_to_sql, write_csv_from_sql
from db.sql.connection.singleton import Database
from orders.handler import create_order_table, ORDER_TABLE_MAPPING
from products.handler import PRODUCT_MAPPING, create_product_table
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


def upload_csv(file, headers, table, has_headers, csv_mappings=None):
    """
    Upload the CSV file

    :param file:    Name of the file to upload
    :param headers: Any headers
    :param table: Table to write to
    :param has_headers: Whether there are headers in the csv
    :param csv_mappings:    Optional mappings for ETL
    """
    fpath = os.getcwd()
    fpath = os.path.sep.join([fpath, "productdata", file])
    write_csv_to_sql(
        fpath, table=table, headers=headers, has_headers=has_headers, csv_mappings=csv_mappings)


def create_tables(csv, create, headers, database, build_tables):
    """
    Prepares the database

    :param csv:     Whether to upload a csv
    :param create:  Whether to create tables
    :param headers: Any csv headers
    :param database:  Database or path to database to use
    :param build_tables:  Whether to create tables
    """
    if csv and create.lower() == "true":
        if headers:
            headers = json.loads(headers)
        else:
            product_headers = {
                "product_id": "varchar",
                "quantity": "integer",
                "wholesale_price": "double precision",
                "sale_price": "double precision",
                "supplier_id": "varchar"
            }
            order_headers = {
                "date": "integer",
                "author_id": "varchar",
                "zip": "varchar",
                "product_id": "varchar",
                "quantity": "integer"
            }
            order_mappings = {
                "date": "utc",
                "author_id": "varchar",
                "zip": "varchar",
                "product_id": "varchar",
                "quantity": "integer"
            }
        if build_tables:
            build_db(database, "products", headers)
            create_product_table()
            create_order_table()
            create_users_table()
        else:
            _db = Database.instance(database)
        upload_csv("product_data.csv", product_headers.keys(), table="products", has_headers=True)
        upload_csv("order_data.csv", order_headers.keys(), table="orders", has_headers=True,
                   csv_mappings=order_mappings)
    else:
        _db = Database.instance(database)


def write_tables_to_csv(write_tables, database):
    """
    Write tables to  CSV from databse if specified

    :param write_tables: Path to CSV files
    :param database:    Database to use
    """
    try:
        if os.path.exists(write_tables):
            # start database
            db = Database.instance(database)

            # get headers
            order_headers = ORDER_TABLE_MAPPING.keys()
            product_headers = PRODUCT_MAPPING.keys()

            # order path
            order_path = "orders_{}.csv".format(str(datetime.datetime.now().timestamp()))
            order_path = os.path.sep.join([write_tables, order_path])

            # product path
            product_path = "product_{}.csv".format(str(datetime.datetime.now().timestamp()))
            product_path = os.path.sep.join([write_tables, product_path])

            # write orders
            write_csv_from_sql(db, order_headers, order_path, "orders")

            # write csv
            write_csv_from_sql(db, product_headers, product_path, "products")
        else:
            raise FileNotFoundError("DIRECTORY NOT FOUND ERROR: {}".format(write_tables))
    except Exception as e:
        print("ERROR: You May Need to Instantiate Your Database")
        raise e


def start_discord(arguments):
    """
    Starts the discord application using the command line.

    :param arguments:   Arguments from docopt
    """
    database = arguments.get("--db", "db.sqlite3")
    write_tables = arguments.get("--write_csv", None)
    db_only = arguments.get("--db_only", None)
    if database is None:
        database = "db.sqlite3"
    headers = arguments.get("--headers", None)
    build_tables = False
    csv = arguments.get("--csv_path", None)
    create = arguments.get("--create", "False")
    if create is None:
        if csv:
            create = "true"
        else:
            create = "False"
    else:
        build_tables = True
    create_tables(csv, create, headers, database, build_tables)

    if write_tables:
        write_tables_to_csv(write_tables, database)
    elif db_only is None:
        discordbot.start()


def start_website():
    """
    Start the associated statistics website
    """
    if arguments.get("--db_only", None) is None:
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
    website_proc = None
    discord_thread = None

    python_path = os.environ.get("PYTHON_PATH", "python")

    # create threads
    if arguments.get("--discord_only", False) or arguments.get("--website_only", False) is False:
        logging.info("Creating Discord Thread")
        discord_thread = threading.Thread(target=start_discord, args=(arguments,))
        discord_thread.daemon = True
        discord_thread.start()
    elif arguments.get("--website_only", False) or arguments.get("--discord_only", False) is False:
        if python_path:
            logging.info("Creating Website Thread")
            djangopath = os.getcwd()
            djangopath = os.path.sep.join([djangopath, 'website', 'manage.py'])
            website_proc = subprocess.Popen([python_path, djangopath, 'runserver'])
        else:
            logging.warning("Must Specify a Python Path to Run the Website from this Part of the Application.")

    # wait for threads to terminate
    logging.info("Waiting for Threads to Complete")
    if discord_thread:
        discord_thread.join()
    if website_proc:
        logging.info("You Must Manually Kill this Process When Running a Website")
