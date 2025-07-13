from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ListingViewSet, ListingImageViewSet

router = DefaultRouter()
router.register(r'listings', ListingViewSet)
router.register(r'images', ListingImageViewSet)

urlpatterns = [
    # Add additional URL patterns here if needed
]

urlpatterns += router.urls
