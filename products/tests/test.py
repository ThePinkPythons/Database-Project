"""
Tests for the products
"""

import unittest

from db.crud.executor import create_records, get_record, update_record
from db.sql.connection.singleton import Database
from db.sql.query.builder import Create, Select, Update
from products.handler import create_product_table, Product, GetProduct, DeleteProduct, UpdateProduct, drop_product_table


class ProductTests(unittest.TestCase):

    def test_create_product_table(self):
        """
        Tests creating the product table
        """
        _db = Database.instance(":memory:")
        try:
            create_product_table()
        except Exception as e:
            print(e)

    def test_create_product(self):
        """
        Test creating a product
        """
        _db = Database.instance(":memory:")
        try:
            create_product_table()
        except Exception as e:
            print(e)
        product = Product(1, 10.0, 20.0, 'test', 'test')
        product.save()

    def test_get_product(self):
        """
        Test obtaining a product
        """
        _db = Database.instance(":memory:")
        try:
            create_product_table()
        except Exception as e:
            print(e)
        product = Product(1, 10.0, 20.0, 'test', 'test')
        product.save()
        product = GetProduct()
        product.by_product_id('test')
        products = product.query()
        print(products)
        assert len(products) == 1


    def test_update_product(self):
        """
        Test updating a product
        """
        _db = Database.instance(":memory:")
        try:
            create_product_table()
        except Exception as e:
            print(e)
        product = Product(1, 10.0, 20.0, 'test', 'test')
        product.save()
        product = GetProduct()
        product.by_product_id('test')
        products = product.query()
        print(products)
        assert len(products) == 1

    def test_delete_product(self):
        """
        Test deleting a product
        """
        _db = Database.instance(":memory:")
        try:
            create_product_table()
        except Exception as e:
            print(e)
        product = Product(1, 10.0, 20.0, 'test', 'test')
        product.save()
        product = GetProduct()
        product.by_product_id('test')
        products = product.query()
        print(products)
        assert len(products) >= 1
        product = DeleteProduct()
        product.with_product_id('test')
        product.delete()
        product = GetProduct()
        product.by_product_id('test')
        products = product.query()
        print(products)
        assert len(products) == 0

    def test_update_product(self):
        """
        Test update a product
        """
        _db = Database.instance(":memory:")
        try:
            create_product_table()
        except Exception as e:
            print(e)
        product = Product(1, 10.0, 20.0, 'test', 'test')
        product.save()
        product = GetProduct()
        product.by_product_id('test')
        products = product.query()
        print(products)
        assert len(products) >= 1
        product = UpdateProduct()
        product.set_quantity(100)
        product.update()
        product = GetProduct()
        product.by_product_id('test')
        products = product.query()
        print(products)
        assert len(products) >= 1
        assert products[0].get("quantity", 0) == 100

    def test_drop_products_table(self):
        """
        Test drop the products table
        """
        _db = Database.instance(":memory:")
        try:
            create_product_table()
        except Exception as e:
            print(e)
        drop_product_table()
