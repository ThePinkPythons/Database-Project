"""
A product handler for good measure
"""
import uuid

from db.crud.executor import create_records, update_record, get_record, drop_table, create_table, delete_record
from db.sql.query.builder import Create, Update, Select, DropTable, CreateTable, Delete
from db.templates.dbobject import DatabaseObject


PRODUCT_MAPPING = {
    "product_id": "varchar",
    "quantity": "integer",
    "wholesale_price": "double precision",
    "sale_price": "double precision",
    "supplier_id": "varchar"
}


class Product(DatabaseObject):

    def __init__(self, quantity, wholesale_price, sale_price, supplier_id, product_id=None):
        """
        Constructor

        :param quantity:    Quantity available
        :param wholesale_price: Wholesale price
        :param sale_price:  Sale price
        :param supplier_id:     Supplier id
        :param product_id:  Product id
        """
        if product_id is None:
            product_id = uuid.uuid4()
        self._product = {
            "product_id": product_id,
            "quantity": quantity,
            "wholesale_price": wholesale_price,
            "sale_price": sale_price,
            "supplier_id": supplier_id
        }

    def save(self):
        """
        Save the product
        """
        create = Create("products", self._product.keys())
        create_records(
            self._product.keys, create, [self._product])
        return self._product["product_id"]


class UpdateProduct(object):

    def __init__(self):
        self._mapping = {}
        self._update = Update("products", None)

    def set_quantity(self, quantity):
        """
        Update the quantity

        :param quantity:    The quantity as an integer
        """
        self._mapping["quantity"] = quantity

    def set_sale_price(self, price):
        """
        Update the sale price

        :param price:   The new sale price
        """
        self._mapping["sale_price"] = price

    def set_wholesale_price(self, price):
        """
        Update the sale price

        :param price: The new wholesale price
        """
        self._mapping["wholesale_price"] = price

    def update(self):
        """
        Perform the update
        """
        if len(self._mapping.keys()) == 0:
            raise ValueError("No Update Keys Set")
        self._update.set_mapping(self._mapping)
        update_record(self._update)
        self._update = Update("products", {})


class GetProduct(object):

    def __init__(self):
        """
        Constructor
        """
        self._fields = PRODUCT_MAPPING.keys()
        self.select = Select("products", self._fields)

    def by_product_id(self, product_id):
        """
        Get by the product id

        :param product_id:  The product id
        """
        self.select.equals("product_id", product_id)

    def where_quantity_less_than(self, quantity):
        """
        Where the quantity is less than a given amount

        :param quantity:    The quantity
        """
        self.select.less_than("quantity", quantity)

    def where_quantity_greater_than(self, quantity):
        """
        Where the quantity is greater than

        :param quantity:    The quantity
        """
        self.select.greater_than("quantity", quantity)

    def sale_price_less_than(self, price):
        """
        Where the quantity is less than

        :param price: Price to match against
        """
        self.select.less_than("sale_price", price)

    def sale_price_greater_than(self, price):
        """
        Where the quantity is greater than

        :param price:   The price
        """
        self.select.greater_than("quantity", price)

    def query(self):
        """
        Query the tables
        """
        records = []
        # must use the for loop does not work otherwise
        for row in get_record(self.select):
            record = dict(zip(self._fields, row))
            records.append(record)
        self.select = Select("orders", self._fields)
        return records


class DeleteProduct(object):

    def __init__(self):
        """
        Delete a product
        """
        self._delete = Delete("products")

    def with_product_id(self, product_id):
        """
        Delete where prduct id equals

        :param product_id:  The product id
        """
        self._delete.equals("product_id", product_id)

    def delete(self):
        """
        Run the delete
        """
        delete_record(self._delete)
        self._delete = Delete("products")


def create_product_table():
    """
    Creates the product table
    """
    create = CreateTable("products", PRODUCT_MAPPING)
    create_table(create)


def drop_product_table():
    """
    Drops the product table
    """
    drop = DropTable("products")
    drop_table(drop)
