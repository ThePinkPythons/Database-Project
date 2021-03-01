"""
Test the executor
"""

import unittest

from db.crud.executor import create_records, update_record, get_record, delete_record
from db.sql.connection.singleton import Database
from db.sql.query.builder import Create, Update, Select, Delete


class ExecutorTests(unittest.TestCase):

    def test_create_records(self):
        """
        Test create a record
        """
        mp = {
            "a": "integer"
        }
        keys = mp.keys()
        _db = Database.instance(":memory:", "test_table", mp)
        create = Create("test_table", keys)
        create_records(keys, create, [{"a": 1}, {"a": 2}])

    def test_update_record(self):
        """
        Test the updater
        """
        mp = {
            "a": "integer"
        }
        keys = mp.keys()
        _db = Database.instance(":memory:", "test_table", mp)
        up = Update("test_table", {"a": 2})
        up.less_than_or_equal_to("a", 3)
        update_record(up)

    def test_select(self):
        """
        Test the select
        """
        mp = {
            "a": "integer"
        }
        db = Database.instance(":memory:", "test_table", mp)
        keys = mp.keys()
        create = Create("test_table", keys)
        create_records(keys, create, [{"a": 1}, {"a": 2}])
        sel = Select("test_table", ["a"])
        sel.less_than_or_equal_to("a", 3)
        rvals = []
        for r in get_record(sel):
            rvals.append(r)
        assert(len(rvals) > 0)

    def test_delete_record(self):
        mp = {
            "a": "integer"
        }
        db = Database.instance(":memory:", "test_table", mp)
        keys = mp.keys()
        create = Create("test_table", keys)
        create_records(keys, create, [{"a": 1}, {"a": 2}])
        sel = Select("test_table", ["a"])
        sel.less_than_or_equal_to("a", 3)
        rvals = []
        for r in get_record(sel):
            rvals.append(r)
        assert (len(rvals) == 2)
        d = Delete("test_table")
        d.greater_than("a", 1)
        delete_record(d)
        sel = Select("test_table", ["a"])
        sel.less_than_or_equal_to("a", 3)
        rvals = []
        for r in get_record(sel):
            rvals.append(r)
        assert (len(rvals) == 1)
