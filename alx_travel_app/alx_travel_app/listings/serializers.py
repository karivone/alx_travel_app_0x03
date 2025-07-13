from rest_framework import serializers
from .models import Listing, ListingImage
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ListingImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListingImage
        fields = ['id', 'image', 'caption', 'is_primary', 'uploaded_at']

class ListingSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    images = ListingImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'address', 'city', 'country',
            'price_per_night', 'listing_type', 'max_guests', 'bedrooms',
            'bathrooms', 'available', 'created_at', 'updated_at', 'owner', 'images'
        ]
