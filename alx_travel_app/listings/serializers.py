from rest_framework import serializers
from .models import Listing, ListingImage, Booking
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

class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    listing = serializers.PrimaryKeyRelatedField(queryset=Listing.objects.all())


    class Meta:
        model = Booking
        fields = ['id', 'listing', 'user', 'check_in', 'check_out', 'guests', 'created_at', 'updated_at']
