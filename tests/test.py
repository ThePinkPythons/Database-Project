"""
Main tests
"""

import unittest

from db.sql.connection.singleton import Database
from main import build_db, upload_csv


class MainTests(unittest.TestCase):
    """
    Main Unit Tests
    """

    def create_test_db(self):
        """
        Setup the test database in RAM
        """
        headers = {
            "product_id": "varchar",
            "quantity": "integer",
            "wholesale_price": "double precision",
            "sale_price": "double precision",
            "supplier_id": "varchar"
        }
        build_db(":memory:", "products", headers)

    def test_build_db(self):
        """
        Test build db in main
        """
        self.create_test_db()
        db = Database.instance(None)
        c = db.cursor()
        try:
            c.execute("SELECT * FROM products")
        finally:
            c.close()

    def test_upload_csv(self):
        """
        Test uploading the CSV file
        """
        self.create_test_db()
        headers = {
            "product_id": "varchar",
            "quantity": "integer",
            "wholesale_price": "double precision",
            "sale_price": "double precision",
            "supplier_id": "varchar"
        }
        upload_csv(headers.keys(), True)
        db = Database.instance(None)
        c = db.cursor()
        try:
            rows = []
            for row in c.execute("SELECT * FROM products"):
                rows.append(row)
            assert len(rows) > 10000
        finally:
            c.close()
