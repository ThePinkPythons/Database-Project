from django.db import models


class AvailableProducts(models.Model):
    product_id = models.CharField(max_length=125)
    quantity = models.IntegerField()
    wholesale_price = models.DecimalField(decimal_places=2, max_digits=8)
    sale_price = models.DecimalField(decimal_places=2, max_digits=8)
    supplier_id = models.CharField(max_length=125)

    def __str__(self):
        self.product_id

    class Meta:
        db_table = "products"
