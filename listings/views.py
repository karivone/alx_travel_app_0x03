from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Listing, ListingImage, Booking
from .serializers import ListingSerializer, ListingImageSerializer, BookingSerializer
from django.shortcuts import get_object_or_404
from .tasks import send_listing_notification
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ListingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listings
    
    list:
    Return all listings, optionally filtered by search parameters.
    
    create:
    Create a new listing. Requires authentication.
    
    retrieve:
    Return a specific listing by ID.
    
    update:
    Update a listing. Only the owner can update.
    
    partial_update:
    Partially update a listing. Only the owner can update.
    
    destroy:
    Delete a listing. Only the owner can delete.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'city', 'country']
    ordering_fields = ['price_per_night', 'created_at']
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        """
        Optionally filter by availability and owner
        """
        queryset = Listing.objects.all()
        available = self.request.query_params.get('available', None)
        owner = self.request.query_params.get('owner', None)
        
        if available is not None:
            queryset = queryset.filter(available=available.lower() == 'true')
        if owner is not None:
            queryset = queryset.filter(owner__username=owner)
            
        return queryset
    
    def perform_create(self, serializer):
        listing = serializer.save(owner=self.request.user)
        # Send notification using Celery task
        send_listing_notification.delay(listing.id, listing.title)
    
    @action(detail=True, methods=['get'])
    def images(self, request, pk=None):
        listing = self.get_object()
        images = ListingImage.objects.filter(listing=listing)
        serializer = ListingImageSerializer(images, many=True)
        return Response(serializer.data)

class ListingImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing images
    
    list:
    Return all images for listings.
    
    create:
    Upload a new image for a listing. Requires authentication.
    
    retrieve:
    Return a specific image by ID.
    
    destroy:
    Delete an image. Only the listing owner can delete.
    """
    queryset = ListingImage.objects.all()
    serializer_class = ListingImageSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        listing_id = self.request.data.get('listing')
        listing = get_object_or_404(Listing, id=listing_id)
        # Check if the user is the owner of the listing
        if listing.owner != self.request.user:
            raise serializers.ValidationError({"error": "You do not have permission to add images to this listing."})
        # Check if this is the first image for the listing
        if not ListingImage.objects.filter(listing=listing).exists():
            serializer.save(listing=listing, is_primary=True)
        else:
            serializer.save(listing=listing)


class BookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for bookings
    
    list:
    Return all bookings. Users can only see their own bookings unless they are staff.
    
    create:
    Create a new booking. Requires authentication.
    
    retrieve:
    Return a specific booking. Users can only see their own bookings unless they are staff.
    
    update:
    Update a booking. Only the booking owner can update.
    
    partial_update:
    Partially update a booking. Only the booking owner can update.
    
    destroy:
    Cancel a booking. Only the booking owner can cancel.
    """
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return only the user's bookings, or all bookings for staff
        """
        if self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """
        Automatically set the user to the current user when creating a booking
        """
        listing_id = self.request.data.get('listing')
        listing = get_object_or_404(Listing, id=listing_id)
        
        # Check if the listing is available
        if not listing.available:
            raise serializers.ValidationError({"error": "This listing is not available for booking."})
            
        # Check for overlapping bookings
        check_in = self.request.data.get('check_in')
        check_out = self.request.data.get('check_out')
        
        if check_in and check_out:
            overlapping_bookings = Booking.objects.filter(
                listing=listing,
                check_out__gt=check_in,
                check_in__lt=check_out
            )
            
            if overlapping_bookings.exists():
                raise serializers.ValidationError({"error": "This listing is already booked for the selected dates."})
        
        serializer.save(user=self.request.user, listing=listing)
