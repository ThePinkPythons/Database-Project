"""
Tests for the table
"""

import unittest

from db.sql.connection.singleton import Database
from orders.handler import CancelOrder, Order, ORDER_TABLE_MAPPING, GetOrders, create_order_table, DeleteOrdersByUser, \
    drop_order_table


class OrderTests(unittest.TestCase):

    def test_update_record(self):
        """
        Test updating a record
        """
        _db = Database.instance(":memory:", "orders", ORDER_TABLE_MAPPING)
        create_order_table()
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
        _db = Database.instance(":memory:")
        create_order_table()

    def test_create_order(self):
        """
        Test creating an order
        """
        _db = Database.instance(":memory:")
        create_order_table()
        order = Order('test', 'test-order', city="test", state="test", address="test")
        order.price(10)
        order.quantity(100)
        order.save()

    def test_get_order(self):
        _db = Database.instance(":memory:")
        create_order_table()
        order = Order('test', 'test-order', city="test", state="test", address="test")
        order.product_id("test")
        order.price(10)
        order.quantity(100)
        order.save()
        order = GetOrders('test')
        orders = order.query()
        print(orders)
        assert len(orders) == 1
        assert orders[0].get("product_id", "NE") == "test"

    def test_delete_order(self):
        _db = Database.instance(":memory:")
        create_order_table()
        order = Order('test', 'test-order', city="test", state="test", address="test")
        order.product_id("test")
        order.price(10)
        order.quantity(100)
        order.save()
        order = GetOrders('test')
        orders = order.query()
        print(orders)
        assert len(orders) == 1
        assert orders[0].get("product_id", "NE") == "test"
        order = DeleteOrdersByUser('test')
        order.delete()
        order = GetOrders('test')
        orders = order.query()
        print(orders)
        assert len(orders) == 0

    def test_cancel_order(self):
        _db = Database.instance(":memory:")
        create_order_table()
        order = Order('test', 'test-order', city="test", state="test", address="test")
        order.product_id("test")
        order.price(10)
        order.quantity(100)
        order.save()
        order = GetOrders('test')
        orders = order.query()
        print(orders)
        assert len(orders) == 1
        assert orders[0].get("product_id", "NE") == "test"
        order = CancelOrder('test-order')
        order.cancel()
        order = GetOrders('test')
        orders = order.query()
        print(orders)
        assert len(orders) == 1
        assert orders[0].get("status", "NE") == "cancelled"

    def test_dop_orders(self):
        """
        Test drop the orders table
        """
        _db = Database.instance(":memory:")
        create_order_table()
        drop_order_table()
