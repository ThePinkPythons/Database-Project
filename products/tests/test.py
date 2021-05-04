"""
Tests for the products
"""

import unittest

from db.crud.executor import create_records, get_record, update_record
from db.sql.connection.singleton import Database
from db.sql.query.builder import Create, Select, Update


class ProductTests(unittest.TestCase):

    def test_create_order_table(self):
        """
                Test create a table of orders
        """
        mp = {
            "a": "string",
            "b": "integer",
            "c": "varchar",
            "d": "integer",
            "e": "string"
        }
        keys = mp.keys()
        _db = Database.instance(":memory:", "test_order_table", mp)
        create = Create("test_order_table", keys)
        create_records(keys, create,
                       [{"a": "test_user_0", "b": 12345, "c": "product_id_0", "d": 12, "e": "status: Accepted"},
                        {"a": "test_user_1", "b": 67890, "c": "product_id_1", "d": 14711, "e": "status: Cancelled"}])

    def test_create_order_table_does_not_terminate_on_exists(self):
        pass

    def test_create_order(self):
        pass

    def test_get_order(self):
        """
            Test the get order
        """
        mp = {
            "a": "string",
            "b": "integer",
            "c": "varchar",
            "d": "integer",
            "e": "string"
        }
        db = Database.instance(":memory:", "test_order_table", mp)
        keys = mp.keys()
        create = Create("test_order_table", keys)
        create_records(keys, create,
                       [{"a": "test_user_0", "b": 12345, "c": "product_id_0", "d": 12, "e": "status: Accepted"},
                        {"a": "test_user_1", "b": 67890, "c": "product_id_1", "d": 14711, "e": "status: Cancelled"}])
        sel = Select("test_order_table", ["b"])
        order_ids = []
        for r in get_record(sel):
            order_ids.append(r)

    def test_get_orders(self):
        pass

    def test_cancel_order(self):
        """
            Test cancel order
        """
        mp = {
            "a": "string",
            "b": "integer",
            "c": "varchar",
            "d": "integer",
            "e": "string"
        }
        keys = mp.keys()
        _db = Database.instance(":memory:", "test_order_table", mp)
        up = Update("test_order_table", {"e": "status: Cancelled"})
        update_record(up)
