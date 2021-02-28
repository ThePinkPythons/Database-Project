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
  --headers=<headers>      Headers for the csv file in the order they appear
  --db=<db>                Database to use
"""

from docopt import docopt


if __name__ == "__main__":
    arguments = docopt(__doc__, version='Database Project 0.1')
    database = arguments.get()
