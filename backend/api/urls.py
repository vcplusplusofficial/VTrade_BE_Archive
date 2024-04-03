
from django.urls import path
from .view import listing_operations, modify_listing
from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('listing_operations/', listing_operations, name='listing_operations'),
    path('modify_listing/', modify_listing, name='modify_listing'),
]
