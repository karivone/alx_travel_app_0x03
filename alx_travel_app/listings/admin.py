from django.contrib import admin
from .models import Listing, ListingImage

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'country', 'price_per_night', 'listing_type', 'available')
    list_filter = ('listing_type', 'available', 'city', 'country')
    search_fields = ('title', 'description', 'address', 'city', 'country')
    inlines = [ListingImageInline]

@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ('listing', 'caption', 'is_primary', 'uploaded_at')
    list_filter = ('is_primary', 'uploaded_at')
    search_fields = ('listing__title', 'caption')
