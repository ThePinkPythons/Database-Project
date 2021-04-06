"""
Order class
"""
from uuid import uuid4

from db.crud.executor import create_table, create_records, delete_record, get_record, drop_table, update_record
from db.sql.query.builder import CreateTable, Delete, Create, Select, DropTable, Update
from db.templates.dbobject import DatabaseObject


# Table headers
ORDER_TABLE_MAPPING = {
    "product_id": "varchar",
    "quantity": "integer",
    "price": "double precision",
    "total": "double_precision",
    "author_id": "varchar",
    "order_id": "varchar",
    "address": "varchar",
    "city": "varchar",
    "state": "varchar",
    "zip": "varchar",
    "status": "varchar"
}


class Order(DatabaseObject):
    """
    Order Object. Allows users to reuse the object by
    setting new product ids repeatedly.
    """

    def __init__(self, author_id, order_id, status="active", address=None, city=None, state=None, zip=None):
        """
        Constructor

        :param author_id:   author_id
        :param order_id:    order_id
        :param status:    Status
        :param address:   Shipping address
        :param city:    Shipping city
        :param state:   Shipping state
        :param zip:     Shipping zip code
        """
        if address is None and city is None and state is None:
            print("CANNOT CREATE ORDER WITHOUT A CITY STATE OR ADDRESS")
        self._order = {
            "product_id": None,
            "quantity": None,
            "price": None,
            "author_id": author_id,
            "order_id": str(uuid4()),
            "status": status,
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
        if self._order.get("address", None) and self._order.get("city", None) and self._order.get("state"):
            if self._order.get("price", None) and self._order.get("quantity", None):
                self._order["total"] = self._order["price"] * self._order["quantity"]
            else:
                raise ValueError("Price and Quantity not Set")
            create = Create("orders", self._order.keys())
            create_records(
                self._order.keys, create, [self._order])
            return self._order["order_id"]
        else:
            print("CANNOT CREATE ORDER WITHOUT A CITY STATE OR ADDRESS")
            print("ORDER NOT SUBMITTED")
            return -1


class CancelOrder(object):

    def __init__(self, order_id):
        """
        Cancels an order

        :param the order id
        """
        self._order_id = order_id

    def cancel(self):
        """
        Create the cancellation from an update query and execute it.
        """
        mapping = {
            "order_id": self._order_id,
            "status": "cancelled"
        }
        update = Update("order", mapping)
        update_record(update)


class DeleteOrdersByUser(object):

    def __init__(self, author_id):
        """
        Constructor

        :param author_id:  Author_id uuid for the customer
        """
        self._author_id = author_id

    def delete(self):
        """
        Run the delete
        """
        delete = Delete("orders")
        delete.equals("author_id", self._author_id)
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

    def by_author_id(self, author_id):
        """
        Delete orders with the given user

        :param author_id:    The user author_id
        """
        self.delete.equals("author_id", author_id)

    def delete(self):
        """
        Run the delete
        """
        delete_record(self.delete)
        self.delete = Delete("orders")


class GetOrders(object):

    def __init__(self, author_id):
        """
        Constructor

        :param author_id:   author_id to orders by
        """
        self._fields = ORDER_TABLE_MAPPING.keys()
        self.select = Select("orders", self._fields)
        self.select.equals("author_id", author_id)

    def by_author_id(self, author_id):
        """
        Get the user with the specific author_id

        :param author_id:   The user author_id
        """
        self.select.equals("author_id", author_id)
    
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
