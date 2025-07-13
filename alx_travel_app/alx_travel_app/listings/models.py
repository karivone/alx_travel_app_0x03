from django.db import models
from django.contrib.auth.models import User

class Listing(models.Model):
    LISTING_TYPES = (
        ('hotel', 'Hotel'),
        ('apartment', 'Apartment'),
        ('villa', 'Villa'),
        ('cottage', 'Cottage'),
        ('resort', 'Resort'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    listing_type = models.CharField(max_length=20, choices=LISTING_TYPES)
    max_guests = models.PositiveIntegerField()
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    
    def __str__(self):
        return self.title

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='listings/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.listing.title}"
