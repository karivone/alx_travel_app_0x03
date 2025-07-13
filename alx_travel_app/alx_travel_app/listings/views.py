from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Listing, ListingImage
from .serializers import ListingSerializer, ListingImageSerializer
from django.shortcuts import get_object_or_404
from .tasks import send_listing_notification

class ListingViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listings
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'city', 'country']
    ordering_fields = ['price_per_night', 'created_at']
    
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
    """
    queryset = ListingImage.objects.all()
    serializer_class = ListingImageSerializer
    
    def perform_create(self, serializer):
        listing_id = self.request.data.get('listing')
        listing = get_object_or_404(Listing, id=listing_id)
        # Check if this is the first image for the listing
        if not ListingImage.objects.filter(listing=listing).exists():
            serializer.save(listing=listing, is_primary=True)
        else:
            serializer.save(listing=listing)
