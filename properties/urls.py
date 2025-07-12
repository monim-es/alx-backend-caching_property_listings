from django.urls import path
from . import views

app_name = 'properties'

urlpatterns = [
    # Main property list endpoint
    path('', views.property_list, name='property_list'),
    
    # Optional HTML version
    path('html/', views.property_list_html, name='property_list_html'),
    
    # Cache management endpoints
    path('cache/stats/', views.cache_stats, name='cache_stats'),
    path('cache/warm/', views.warm_cache_view, name='warm_cache'),
]