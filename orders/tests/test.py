"""
Tests for the table
"""

import unittest

from db.sql.connection.singleton import Database
from orders.handler import CancelOrder, Order, ORDER_TABLE_MAPPING, GetOrders


class OrderTests(unittest.TestCase):

    def test_update_record(self):
        _db = Database.instance(":memory:", "orders", ORDER_TABLE_MAPPING)
        order = Order("test_author", "test", "active", "test", "test", "test")
        order.quantity(1)
        order.price(2)
        order.save()
        orders = GetOrders("test_author")
        records = orders.query()
        assert len(records) == 1
        cancel = CancelOrder("test_id")
        cancel.cancel()
        orders = GetOrders("test_author")
        records = orders.query()
        assert len(records) == 1
        order = records[0]
        assert order["status"] == "cancelled"

    def test_create_order_table(self):
        pass

    def test_create_order_table_does_not_terminate_on_exists(self):
        pass

    def test_create_order(self):
        pass

    def test_get_order(self):
        pass

    def test_get_orders(self):
        pass

    def test_cancel_order(self):
        pass
