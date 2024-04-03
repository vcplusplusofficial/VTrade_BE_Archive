from rest_framework import serializers
from .models import Listing, Image, User


class CardViewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']


# Serializer for a basic representation of Listing
class CardViewListingSerializer(serializers.ModelSerializer):
    listing_images = ImageSerializer(many=True, read_only=True)
    user = CardViewUserSerializer()

    class Meta:
        model = Listing
        fields = ['id', 'title', 'price', 'create_date']


# Serializer for a detailed representation of Listing
class DetailedListingSerializer(serializers.ModelSerializer):
    listing_images = ImageSerializer(many=True, read_only=True)
    user = CardViewUserSerializer()

    class Meta:
        model = Listing
        fields = '__all__'
