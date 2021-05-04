"""
Serializes database from the API
"""

from rest_framework import serializers
from dashboard.models import AvailableProducts


class AvailableProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = AvailableProducts
        fields = ["product_id", "quantity", "wholesale_price", "sale_price", "supplier_id"]
