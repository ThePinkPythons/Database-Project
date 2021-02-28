"""
Test sqllite 3 connection
"""

import unittest

from sql.connection.factory import Database


class SQLLiteTests(unittest.TestCase):

    def test_singleton_from_file(self):
        """
        Test the singleton instance from file
        """
        db = Database.instance("test.db")
        assert (db)
        v = db.execute("Select 1")
        assert (v)
        for record in v:
            assert (type(record) is tuple)
            assert (record[0] == 1)

    def test_singleton_in_memory(self):
        """
        Test the singleton in RAM
        """
        db = Database.instance(":memory:")
        assert(db)
        v = db.execute("Select 1")
        assert(v)
        for record in v:
            assert(type(record) is tuple)
            assert(record[0] == 1)
