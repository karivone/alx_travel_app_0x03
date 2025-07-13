from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import ListingViewSet, ListingImageViewSet, BookingViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'listings', ListingViewSet, basename='listing')
router.register(r'images', ListingImageViewSet, basename='listingimage')
router.register(r'bookings', BookingViewSet, basename='booking')

# Schema view for Swagger/OpenAPI documentation
schema_view = get_schema_view(
   openapi.Info(
      title="ALX Travel App API",
      default_version='v1',
      description="API documentation for ALX Travel App",
      terms_of_service="https://www.example.com/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    # API documentation
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # API endpoints
    path('', include(router.urls)),
]

# Include authentication URLs for the browsable API
urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
]
