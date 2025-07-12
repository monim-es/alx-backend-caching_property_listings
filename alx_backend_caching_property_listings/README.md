# ALX Backend Caching Property Listings

A Django web application demonstrating advanced caching strategies using Redis for property listings. This project implements various caching patterns including page-level caching, low-level caching, cache invalidation using signals, and performance metrics analysis.

## 🚀 Features

- **Property Management**: CRUD operations for property listings
- **Page-Level Caching**: Cached property list views for improved performance
- **Low-Level Caching**: Custom queryset caching with Redis
- **Automatic Cache Invalidation**: Signal-based cache invalidation on data changes
- **Performance Monitoring**: Redis cache hit/miss metrics analysis
- **Dockerized Infrastructure**: PostgreSQL and Redis services via Docker Compose

## 🛠️ Tech Stack

- **Backend**: Django 4.x
- **Database**: PostgreSQL
- **Cache**: Redis
- **Containerization**: Docker & Docker Compose
- **Python**: 3.8+

## 📋 Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Git

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/alx-backend-caching_property_listings.git
cd alx-backend-caching_property_listings
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install django django-redis psycopg2-binary
```

### 4. Start Docker Services

```bash
docker-compose up -d
```

This will start:
- PostgreSQL on port 5432
- Redis on port 6379

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DB_NAME=property_listings
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
REDIS_URL=redis://localhost:6379/1
```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 8. Start Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000/properties/` to view the application.

## 📁 Project Structure

```
alx-backend-caching_property_listings/
├── alx_backend_caching_property_listings/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── properties/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── utils.py
│   ├── signals.py
│   └── migrations/
├── docker-compose.yml
├── requirements.txt
├── manage.py
└── README.md
```

## 🔄 Caching Strategy

### 1. Page-Level Caching
- **Location**: `properties/views.py`
- **Implementation**: `@cache_page(60 * 15)` decorator
- **Duration**: 15 minutes
- **Purpose**: Cache entire property list view responses

### 2. Low-Level Caching
- **Location**: `properties/utils.py`
- **Function**: `get_all_properties()`
- **Duration**: 1 hour
- **Purpose**: Cache database queryset results

### 3. Cache Invalidation
- **Location**: `properties/signals.py`
- **Triggers**: Property create/update/delete operations
- **Method**: Django signals (`post_save`, `post_delete`)
- **Purpose**: Maintain cache consistency

### 4. Performance Monitoring
- **Location**: `properties/utils.py`
- **Function**: `get_redis_cache_metrics()`
- **Metrics**: Hit ratio, total requests, cache performance
- **Purpose**: Monitor and optimize caching effectiveness

## 📊 Available Endpoints

- `GET /properties/` - List all properties (cached)
- `GET /admin/` - Django admin interface

## 🔍 Cache Management Functions

### Core Functions

```python
# Get all properties with caching
properties = get_all_properties()

# Invalidate cache manually
invalidate_properties_cache()

# Get cache statistics
stats = get_cache_stats()

# Get Redis performance metrics
metrics = get_redis_cache_metrics()

# Warm up cache
warm_cache()
```

### Sample Cache Metrics Response

```python
{
    'keyspace_hits': 1250,
    'keyspace_misses': 75,
    'total_requests': 1325,
    'hit_ratio': 0.9434,
    'hit_ratio_percentage': 94.34
}
```

## 🐳 Docker Configuration

The `docker-compose.yml` file defines:

```yaml
services:
  postgres:
    image: postgres:latest
    environment:
      POSTGRES_DB: property_listings
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
  
  redis:
    image: redis:latest
    ports:
      - "6379:6379"
```

## 🧪 Testing Cache Functionality

### 1. Test Cache Population
```bash
# Make initial request (cache miss)
curl http://localhost:8000/properties/

# Make subsequent request (cache hit)
curl http://localhost:8000/properties/
```

### 2. Test Cache Invalidation
```bash
# Add a property via admin or API
# Cache should automatically invalidate
```

### 3. Monitor Cache Performance
```python
from properties.utils import get_redis_cache_metrics
metrics = get_redis_cache_metrics()
print(f"Hit ratio: {metrics['hit_ratio_percentage']}%")
```

## 🔧 Configuration

### Django Settings

Key caching configurations in `settings.py`:

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Session engine
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
```

## 📈 Performance Benefits

- **Reduced Database Load**: Cached queries reduce database hits
- **Faster Response Times**: Cached views serve content instantly
- **Scalability**: Better handling of concurrent requests
- **Monitoring**: Real-time cache performance insights

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- ALX Software Engineering Program
- Django Documentation
- Redis Documentation
- Docker Documentation

## 📧 Contact

Your Name - your.email@example.com
Project Link: https://github.com/yourusername/alx-backend-caching_property_listings

---

⭐ If you found this project helpful, please consider giving it a star!