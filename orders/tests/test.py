"""
Tests for the table
"""

import unittest

from db.sql.connection.singleton import Database
from orders.handler import CancelOrder


class OrderTests(unittest.TestCase):

    def test_update_record(self):
        mp = {
            "order_id": "varchar",
            "status": "varchar"
        }
        keys = mp.keys()
        _db = Database.instance(":memory:", "test_table", mp)
        data = [{
            "order_id": "test_id",
            "status": "active"
        }]
        CancelOrder(["order_id", "status"], "")

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
