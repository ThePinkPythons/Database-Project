from django.db import models


class Order(models.Model):
    """
    Stores an order
    """
    order_id = models.CharField(max_length=125, primary_key=True)
    product_id = models.CharField(max_length=125)
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=8)
    total = models.DecimalField(decimal_places=2, max_digits=8)
    author_id = models.CharField(max_length=125)
    address = models.CharField(max_length=125)
    city = models.CharField(max_length=125)
    state = models.CharField(max_length=125)
    zip = models.CharField(max_length=125)
    status = models.CharField(max_length=125)


class AvailableProducts(models.Model):
    """
    Shows Available Products
    """
    product_id = models.CharField(max_length=125, primary_key=True)
    quantity = models.IntegerField()
    wholesale_price = models.DecimalField(decimal_places=2, max_digits=8)
    sale_price = models.DecimalField(decimal_places=2, max_digits=8)
    supplier_id = models.CharField(max_length=125)

    def __str__(self):
        self.product_id

    class Meta:
        db_table = "products"
