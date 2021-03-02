class Order():
    def __init__(self, email, address, city, state, zip):

        self.email = email

        self.address = address
        self.city = city
        self.state = state
        self.zip = zip

        self.products = []

    def add_product(self, product_id, qty):
        product = (product_id, qty)
        self.products.append(product)

    def del_product(self, product_id):
        self.products = [x for x in self.products if x[0] != product_id]

