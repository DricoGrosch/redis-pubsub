"""
WSGI config for django_redis_example project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_redis_example.settings')

application = get_wsgi_application()

import redis
_redis = redis.Redis(host='localhost', port=6379)