"""
Entry point utilities for reading csv and storing in sql
"""
from csv.reader.csv import CSVSource


def read_csv(filepath, headers=None):
    """
    Reads the csv from the file path

    :param filepath:    The file path
    :param headers: Headers list in the order they appear in the csv
    """
    csv = CSVSource(filepath)



def write_csv(db, fpath,table="products"):
    """
    Writes the csv file stored in the database to the file

    :param csv: The csv to write
    :param fpath:   The file path
    :param table:   The table to insert into
    """
    pass
