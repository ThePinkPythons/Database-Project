"""
CS3250 Project. Includes Discord Chat Bot and CSV Reader

Usage:
    main.py <csv_path> [--table=<table>]
    main.py <csv_path> [--headers=<headers>]
    main.py <csv_path> [--table=<table>] [--headers=<headers>]
    main.py <csv_path> [--headers=<headers>] [--table=<table>]

Options:
  -h --help                Show this screen.
  --version                Show version.
  --table=<table>          Name of the table in sqlite3
  --headers=<headers>      Headers for the csv file in the order they appear
"""

from docopt import docopt


if __name__ == "__main__":
    pass
