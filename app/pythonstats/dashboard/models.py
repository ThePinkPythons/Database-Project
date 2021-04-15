from django.db import models


class AvailableProducts(models.Model):
    product_id = models.CharField(max_length=125)
    quantity = models.IntegerField()
