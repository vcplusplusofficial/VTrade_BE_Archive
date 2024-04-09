from rest_framework import serializers
from .models import Transaction, User, Listing
from django.core.validators import MinValueValidator


# Assuming you have these serializers defined
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']  # Adjust fields as needed


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = ['id', 'title']  # Adjust fields as needed


class TransactionSerializer(serializers.ModelSerializer):
    listing_id = ListingSerializer(read_only=True)
    buyer_id = UserSerializer(read_only=True, source='buyer')
    seller_id = UserSerializer(read_only=True, source='seller')

    class Meta:
        model = Transaction
        fields = ['id', 'price', 'listing_id', 'buyer_id', 'seller_id', 'time_posted', 'time_sold']
        extra_kwargs = {
            'price': {'validators': [MinValueValidator(0)]},
        }
