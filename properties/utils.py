""" Utility functions for property caching and data operations. """

from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property
import logging

logger = logging.getLogger(__name__)


def get_all_properties():
    """
    Retrieve all properties with low-level caching.
    
    This function implements a cache-aside pattern:
    1. Check Redis cache for 'all_properties' key
    2. If found, return cached queryset
    3. If not found, fetch from database
    4. Store in cache for 1 hour (3600 seconds)
    5. Return the queryset
    
    Returns:
        QuerySet: All Property objects ordered by creation date (newest first)
    """
    cache_key = 'all_properties'
    
    # Step 1: Try to get data from cache
    cached_properties = cache.get(cache_key)
    
    if cached_properties is not None:
        logger.info(f"Cache HIT for key: {cache_key}")
        return cached_properties
    
    # Step 2: Cache miss - fetch from database
    logger.info(f"Cache MISS for key: {cache_key} - fetching from database")
    
    # Fetch all properties from database
    queryset = Property.objects.all().order_by('-created_at')
    
    # Convert queryset to list to make it serializable for cache
    properties_list = list(queryset)
    
    # Step 3: Store in cache for 1 hour (3600 seconds)
    cache.set(cache_key, properties_list, 3600)
    logger.info(f"Cached {len(properties_list)} properties for 1 hour")
    
    return properties_list


def invalidate_properties_cache():
    """
    Invalidate the all_properties cache.
    
    This function should be called when properties are created, updated, or deleted
    to ensure cache consistency.
    """
    cache_key = 'all_properties'
    cache.delete(cache_key)
    logger.info(f"Invalidated cache for key: {cache_key}")


def get_property_by_id(property_id):
    """
    Get a specific property by ID with caching.
    
    Args:
        property_id (int): The ID of the property to retrieve
        
    Returns:
        Property: The property object or None if not found
    """
    cache_key = f'property_{property_id}'
    
    # Try to get from cache first
    cached_property = cache.get(cache_key)
    
    if cached_property is not None:
        logger.info(f"Cache HIT for property ID: {property_id}")
        return cached_property
    
    # Cache miss - fetch from database
    try:
        property_obj = Property.objects.get(id=property_id)
        
        # Cache for 30 minutes (1800 seconds)
        cache.set(cache_key, property_obj, 1800)
        logger.info(f"Cached property ID: {property_id} for 30 minutes")
        
        return property_obj
    except Property.DoesNotExist:
        logger.warning(f"Property with ID {property_id} not found")
        return None


def get_cache_stats():
    """
    Get cache statistics for monitoring purposes.
    
    Returns:
        dict: Cache statistics including hit/miss info
    """
    cache_key = 'all_properties'
    
    # Check if cache exists
    cached_data = cache.get(cache_key)
    
    stats = {
        'all_properties_cached': cached_data is not None,
        'all_properties_count': len(cached_data) if cached_data else 0,
        'cache_key': cache_key,
        'cache_timeout': 3600,  # 1 hour in seconds
    }
    
    return stats


def warm_cache():
    """
    Warm up the cache by preloading all properties.
    
    This function can be called to proactively load data into cache,
    useful for application startup or after cache invalidation.
    """
    logger.info("Warming up properties cache...")
    
    # This will fetch from database and cache the results
    properties = get_all_properties()
    
    logger.info(f"Cache warmed up with {len(properties)} properties")
    
    return len(properties)


def get_redis_cache_metrics():
    """
    Retrieve and analyze Redis cache hit/miss metrics.
    
    This function connects to Redis via django_redis and retrieves keyspace
    statistics to calculate cache performance metrics.
    
    Returns:
        dict: Dictionary containing cache metrics including hits, misses, and hit ratio
    """
    try:
        # Get Redis connection using django_redis
        redis_conn = get_redis_connection("default")
        
        # Get Redis INFO statistics
        info = redis_conn.info()
        
        # Extract keyspace hits and misses
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        
        # Calculate total requests
        total_requests = keyspace_hits + keyspace_misses
        
        # Calculate hit ratio (avoid division by zero)
        if total_requests > 0:
            hit_ratio = keyspace_hits / total_requests
        else:
            hit_ratio = 0.0
        
        # Prepare metrics dictionary
        metrics = {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'total_requests': total_requests,
            'hit_ratio': hit_ratio,
            'hit_ratio_percentage': round(hit_ratio * 100, 2)
        }
        
        # Log the metrics
        logger.info(f"Redis Cache Metrics:")
        logger.info(f"  - Keyspace Hits: {keyspace_hits}")
        logger.info(f"  - Keyspace Misses: {keyspace_misses}")
        logger.info(f"  - Total Requests: {total_requests}")
        logger.info(f"  - Hit Ratio: {hit_ratio:.4f} ({metrics['hit_ratio_percentage']}%)")
        
        return metrics
        
    except Exception as e:
        logger.error(f"Error retrieving Redis cache metrics: {str(e)}")
        return {
            'error': str(e),
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'total_requests': 0,
            'hit_ratio': 0.0,
            'hit_ratio_percentage': 0.0
        }