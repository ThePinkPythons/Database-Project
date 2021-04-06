"""
Test sqllite 3 connection
"""

import unittest

from db.sql.connection.singleton import Database


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

    def test_insert(self):
        db = Database.instance(":memory:", "test_table", {"a": "integer"})
        assert (db)
        db.executemany("INSERT INTO test_table(a) VALUES(?)", [(1, ), (2, )])
        db.commit()
        db = Database.instance(None)
        v = db.execute("Select * FROM test_table")
        for record in v:
            assert (type(record) is tuple)
            assert (record[0] in [1, 2])

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
