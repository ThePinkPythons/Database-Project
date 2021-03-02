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
import json

from docopt import docopt

from db.sql import Database


def build_db(database, table, headers):
    """
    Build the data store

    :param database:    The database
    :param table:   Table to use
    :param headers: Headers to use
    :return: A prebuilt database object
    """
    db = Database.instance(database, table, headers)




if __name__ == "__main__":
    arguments = docopt(__doc__, version='Database Project 0.1')
    database = arguments.get("--database", "project.db")
    table = arguments.get("--table", "data")
    headers = arguments.get("--headers", None)
    if headers:
        headers = json.loads(headers)
    Database.instance(database, table, headers)
