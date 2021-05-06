"""
Tests for the user table interaction
"""

import unittest

from db.sql.connection.singleton import Database
from user.handler import create_users_table, User, GetUsers, DeleteUser, drop_users_table


class UsersTests(unittest.TestCase):

    def test_create_product_table(self):
        """
        Tests creating the product table
        """
        _db = Database.instance(":memory:")
        create_users_table()

    def test_create_user(self):
        """
        Test creating a product
        """
        _db = Database.instance(":memory:")
        create_users_table()
        user = User('test', 'test', 'test', 'test', 'test')
        user.save()

    def test_get_user(self):
        """
        Test obtaining a product
        """
        _db = Database.instance(":memory:")
        create_users_table()
        user = User('test', 'test', 'test', 'test', 'test')
        user.save()
        user = GetUsers()
        user.by_author_id('test')
        users = user.query()
        assert len(users) == 1
        assert users[0].get("author_id", "NE") == 'test'

    def test_delete_user(self):
        """
        Test updating a product
        """
        _db = Database.instance(":memory:")
        create_users_table()
        user = User('test', 'test', 'test', 'test', 'test')
        user.save()
        user = GetUsers()
        user.by_author_id('test')
        users = user.query()
        assert len(users) == 1
        assert users[0].get("author_id", "NE") == 'test'
        user = DeleteUser()
        user.by_author_id("test")
        user.delete()
        user = GetUsers()
        user.by_author_id('test')
        users = user.query()
        print(users)
        assert len(users) == 0

    def test_drop_users_table(self):
        """
        Test drop the user table
        """
        _db = Database.instance(":memory:")
        create_users_table()
        drop_users_table()
