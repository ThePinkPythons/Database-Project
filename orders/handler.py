"""
Order class
"""


class Order(object):
    """
    Order Object
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
        self.email = email

        self.address = address
        self.city = city
        self.state = state
        self.zip = zip

        self.products = []

    def add_product(self, product_id, qty):
        """
        Add a product to the order

        :param product_id:  Product id
        :param qty:     Quantity of the
        :return:
        """
        product = (product_id, qty)
        self.products.append(product)

    def del_product(self, product_id):
        self.products = [x for x in self.products if x[0] != product_id]
