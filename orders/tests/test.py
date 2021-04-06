"""
Tests for the table
"""

import unittest
from _msi import CreateRecord

from db.sql.connection.singleton import Database
from orders.handler import CancelOrder, Order, ORDER_TABLE_MAPPING


class OrderTests(unittest.TestCase):

    def test_update_record(self):
        _db = Database.instance(":memory:", "orders", ORDER_TABLE_MAPPING)
        order = Order("test_author", "test", "active", "test", "test", "test")
        order.quantity(1)
        order.price(2)
        order.save()
        cancel = CancelOrder("test_id")
        cancel.cancel()


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
