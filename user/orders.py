"""
A handler that stores the orders and their product id.
"""

# TODO Complete this class

import uuid

from db.crud.executor import drop_table, create_table
from db.sql.query.builder import Select, DropTable, CreateTable
from db.templates.dbobject import DatabaseObject

ORDER_MAPPING = {
    "author_id": "varchar",
    "order_id": "integer",
    "product_id": "varchar",
    "quantity": "integer",
    "sale_price": "integer",
    "order_status": "varchar"
}


class Order(DatabaseObject):

    def __init__(self, author_id, order_id, product_id, order_status, quantity=None, sale_price=None):
        if order_id is None:
            order_id = uuid.uuid4()

        self._order_id = {
            "author_id": author_id,
            "order_id": order_id,
            "product_id": product_id,
            "quantity": quantity,
            "sale_price": sale_price,
            "order_status": order_status
        }


class UpdateOrder(object):
    """Class used to update an order"""
    pass


class DeleteOrder(object):
    """Class to delete an order"""


class GetOrder(object):
    def __init__(self):
        """
        Constructor
        """
        self._fields = ORDER_MAPPING.keys()
        self.select = Select("order_id", self._fields)

    def by_order_id(self, order_id):
        """
        Get product based of order id

        :param order_id:  The product id
        """
        self.select.equals("order_id", order_id)


def create_user_order_table():
    """
    Creates the product table
    """
    create = CreateTable("user_orders", ORDER_MAPPING)
    create_table(create)


def drop_user_order_table():
    """
    Drops the product table
    """
    drop = DropTable("orders")
    drop_table(drop)