"""
Order class
"""
from uuid import uuid4

from db.crud.executor import create_table, create_records, delete_record, get_record
from db.sql.query.builder import CreateTable, Delete, Create, Select
from db.templates.dbobject import DatabaseObject


# Table headers
TABLE_HEADERS = {
    "product_id": "varchar",
    "quantity": "integer",
    "email": "varchar",
    "order_id": "varchar",
    "address": "varchar",
    "city": "varchar",
    "state": "varchar",
    "zip": "varchar"
}


class Order(DatabaseObject):
    """
    Order Object. Allows users to reuse the object by
    setting new product ids repeatedly.
    """

    def __init__(self, email, address, city, state, zip):
        """
        Constructor

        :param email:   Email address
        :param address:   Shipping address
        :param city:    Shipping city
        :param state:   Shipping state
        :param zip:     Shipping zip code
        """
        self._order = {
            "product_id": None,
            "quantity": None,
            "email": email,
            "order_id": str(uuid4()),
            "address": address,
            "city": city,
            "state": state,
            "zip": zip,
        }

    @property.setter
    def product_id(self, product_id):
        """
        Set the product id

        :param product_id:  The product uuid
        """
        self._order["product_id"] = product_id

    @property.setter
    def quantity(self, quantity):
        """
        Set the quantity

        :param quantity:    The quantity
        """
        self._order["quantity"] = quantity

    def save(self):
        """
        Save the order
        """
        create = Create("orders", self._order.keys())
        create_records(
            self._order.keys, create, [self._order])


class DeleteOrdersByProductId(object):

    def __init__(self, product_id):
        """
        Constructor

        :param product_id:  Product Id to delete
        """
        self._product_id = product_id

    def delete(self):
        """
        Run the delete
        """
        del_o = Delete("orders")
        del_o.equals("product_id", self._product_id)
        delete_record(del_o)


class DeleteOrdersByOrderId(object):

    def __init__(self, order_id):
        """
        Constructor

        :param order_id:  Delete the order
        """
        self._order_id = order_id

    def delete(self):
        """
        Run the delete
        """
        del_o = Delete("orders")
        del_o.equals("order_id", self._order_id)
        delete_record(del_o)


class GetOrdersByUser(object):

    def __init__(self, email):
        """
        Constructor

        :param email:   Email user id to orders by
        """
        self._email = email
        self._product_id = None
        self._fields = TABLE_HEADERS.keys()
        self.select = Select("orders", self._fields)
        self.select.equals("email", email)

    @property.setter
    def product_id(self, product_id):
        """
        The product id

        :param product_id:  Product id
        """
        self._product_id = product_id

    def query(self):
        """
        Perform the queries. Reset the selector for reuse.

        :return:    Dictionaries of objects
        """
        records = []
        for row in get_record(self._sel):
            record = dict(zip(self._fields, row))
            records.append(record)
        self.select = Select("orders", self._fields)
        return records


class GetOrdersByProductId(object):

    def __init__(self, product_id):
        """
        Constructor

        :param email:   Email user id to orders by
        """
        self._fields = TABLE_HEADERS.keys()
        self._select = Select("orders", self._fields)
        self.select.equals("product_id", product_id)

    def query(self):
        """
        Perform the queries. Reset the selector for reuse.

        :return:    Dictionaries of objects
        """
        records = []
        for row in get_record(self._sel):
            record = dict(zip(self._fields, row))
            records.append(record)
        self.select = Select("orders", self._fields)
        return records


def create_order_table():
    """
    Creates an order table
    """
    create = CreateTable("orders", TABLE_HEADERS)
    create_table(create)
