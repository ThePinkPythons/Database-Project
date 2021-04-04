"""
Unittests for csv
"""

import unittest

from db.sql.query.builder import Select, Create, Update, Delete, CreateTable


class QueryTests(unittest.TestCase):

    def test_delete(self):
        delete = Delete("test_table")
        delete.less_than("i", 100)
        assert str(delete) == "DELETE FROM test_table WHERE i < 100"

    def test_update(self):
        update = Update("test_table", {"i": 2, "a": "b"})
        update.less_than("i", 3)
        update.equals("a", "c")
        assert str(update) == "UPDATE test_table SET i = 2,a = 'b' WHERE i < 3 AND a LIKE 'c'"

    def test_select(self):
        sel = Select("test_table", ["a", "b"])
        assert str(sel) == "SELECT a,b FROM test_table"

    def test_insert(self):
        ins = Create("test_table", ["a", "b"])
        q = str(ins)
        assert q == "INSERT INTO test_table (a,b) VALUES(?,?)"

    def test_create_table(self):
        mapping = {
            "a": "varchar",
            "b": "integer"
        }
        create = CreateTable("test_table_two", mapping)
        query = str(create)
        assert(query == "CREATE TABLE test_table_two (a varchar,b integer)")
