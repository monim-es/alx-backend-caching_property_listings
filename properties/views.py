from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.core import serializers
from django.utils import timezone
from .models import Property
from .utils import get_all_properties, get_cache_stats
import json

@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    """
    View to return all properties with caching enabled for 15 minutes.
    Now uses low-level caching via get_all_properties() function.
    Returns JSON response with all property data.
    """
    # Get all properties using low-level caching
    properties = get_all_properties()
    
    # Convert to list of dictionaries for JSON serialization
    properties_data = []
    for property_obj in properties:
        properties_data.append({
            'id': property_obj.id,
            'title': property_obj.title,
            'description': property_obj.description,
            'price': str(property_obj.price),  # Convert Decimal to string for JSON
            'location': property_obj.location,
            'created_at': property_obj.created_at.isoformat(),
        })
    
    # Get cache statistics
    cache_stats = get_cache_stats()
    
    # Return JSON response
    return JsonResponse({
        'properties': properties_data,
        'count': len(properties_data),
        'cached': True,  # Indicator that this view uses caching
        'cache_info': {
            'view_cache_duration': '15 minutes',
            'queryset_cache_duration': '1 hour',
            'low_level_cache_active': cache_stats['all_properties_cached']
        }
    })

# Alternative HTML view (optional)
@cache_page(60 * 15)
def property_list_html(request):
    """
    HTML version of property list view with caching.
    Now uses low-level caching via get_all_properties() function.
    """
    properties = get_all_properties()
    
    context = {
        'properties': properties,
        'cached': True,
    }
    
    return render(request, 'properties/property_list.html', context)

# New view to show cache statistics
def cache_stats(request):
    """
    View to display cache statistics for monitoring purposes.
    """
    stats = get_cache_stats()
    
    return JsonResponse({
        'cache_statistics': stats,
        'timestamp': str(timezone.now()),
    })

# New view to manually warm cache
def warm_cache_view(request):
    """
    View to manually warm up the cache.
    Useful for testing or after cache invalidation.
    """
    from .utils import warm_cache
    from django.utils import timezone
    
    count = warm_cache()
    
    return JsonResponse({
        'message': 'Cache warmed up successfully',
        'properties_cached': count,
        'timestamp': str(timezone.now()),
    })