"""
Order class
"""
from uuid import uuid4

from db.crud.executor import create_table, create_records, delete_record, get_record, drop_table
from db.sql.query.builder import CreateTable, Delete, Create, Select, DropTable
from db.templates.dbobject import DatabaseObject


# Table headers
ORDER_TABLE_MAPPING = {
    "product_id": "varchar",
    "quantity": "integer",
    "price": "double precision",
    "total": "double_precision",
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
            "price": None,
            "email": email,
            "order_id": str(uuid4()),
            "address": address,
            "city": city,
            "state": state,
            "zip": zip,
        }
    
    def product_id(self, product_id):
        """
        Set the product id

        :param product_id:  The product uuid
        """
        self._order["product_id"] = product_id
    
    def quantity(self, quantity):
        """
        Set the quantity

        :param quantity:    The quantity
        """
        self._order["quantity"] = quantity

    def price(self, price):
        """
        Set the sale price

        :param price:   The price
        """
        self._order["price"] = price

    def save(self):
        """
        Save the order

        :return: Unique order uuid
        """
        if self._order.get("price", None) and self._order.get("quantity", None):
            self._order["total"] = self._order["price"] * self._order["quantity"]
        else:
            raise ValueError("Price and Quantity not Set")
        create = Create("orders", self._order.keys())
        create_records(
            self._order.keys, create, [self._order])
        return self._order["order_id"]


class DeleteOrdersByUser(object):

    def __init__(self, email):
        """
        Constructor

        :param email:  Email uuid for the customer
        """
        self._email = email

    def delete(self):
        """
        Run the delete
        """
        delete = Delete("orders")
        delete.equals("email", self._email)
        delete_record(delete)


class DeleteOrders(object):

    def __init__(self):
        """
        Constructor
        """
        self.delete = Delete("orders")

    def with_product_id(self, product_id):
        """
        Delete orders with the product ID

        :param product_id:  The product id
        """
        self.delete.equals("product_id", product_id)

    def by_user(self, email):
        """
        Delete orders with the given user

        :param email:    The user email
        """
        self.delete.equals("email", email)

    def delete(self):
        """
        Run the delete
        """
        delete_record(self.delete)
        self.delete = Delete("orders")


class GetOrders(object):

    def __init__(self, email):
        """
        Constructor

        :param email:   Email user id to orders by
        """
        self._fields = ORDER_TABLE_MAPPING.keys()
        self.select = Select("orders", self._fields)
        self.select.equals("email", email)

    def by_user(self, email):
        """
        Get the user with the specific email

        :param email:   The user email
        """
        self.select.equals("email", email)
    
    def with_product_id(self, product_id):
        """
        The product id

        :param product_id:  Product id
        """
        self.select.equals("product_id", product_id)

    def query(self):
        """
        Perform the queries. Reset the selector for reuse.

        :return:    Dictionaries of objects
        """
        records = []
        # must use the for loop does not work otherwise
        for row in get_record(self.select):
            record = dict(zip(self._fields, row))
            records.append(record)
        self.select = Select("orders", self._fields)
        return records


def create_order_table():
    """
    Creates an order table
    """
    create = CreateTable("orders", ORDER_TABLE_MAPPING)
    create_table(create)


def drop_order_table():
    """
    Drop the order table
    """
    drop = DropTable("orders")
    drop_table(drop)
