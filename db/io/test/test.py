"""
Test read and write
"""
import os
import unittest

from db.io.manager import write_csv_to_sql, write_csv_from_sql
from db.sql.connection.singleton import Database


class TestCSV(unittest.TestCase):

    def test_write_to_sql(self):
        """
        Test write to sqlite
        """
        mp = {
            "a": "integer",
            "b": "varchar"
        }
        fpath = os.getcwd()
        fpath = os.path.sep.join([fpath, "productdata", "test_data.csv"])
        write_csv_to_sql(
            fpath,
            ":memory:",
            "test_table",
            headers=["a", "b"],
            table_mappings=mp,
            has_headers=True)
        rvals = []
        db = Database.instance(None)
        c = db.cursor()
        for row in c.execute("SELECT * FROM test_table"):
            rvals.append(row)
        assert len(rvals) == 2

    def test_write_to_csv(self):
        """
        Test write out to csv
        """
        mp = {
            "a": "integer",
            "b": "varchar"
        }
        fpath = os.getcwd()
        fpath = os.path.sep.join([fpath, "productdata", "test_data"])
        write_csv_to_sql(
            fpath,
            ":memory:",
            "test_table",
            headers=["a", "b"],
            table_mappings=mp,
            has_headers=True)
        rvals = []
        db = Database.instance(None)
        c = db.cursor()
        for row in c.execute("SELECT * FROM test_table"):
            rvals.append(row)
        assert len(rvals) == 2
        fpath = os.getcwd()
        fpath = os.path.sep.join([fpath, "productdata", "out_data.csv"])
        write_csv_from_sql(db, ["a", "b"], fpath, "test_table")
