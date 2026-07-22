# Role: Entry point for WSGI-compatible web servers (e.g., Gunicorn, uWSGI) to serve synchronous Django application.
"""
WSGI config for coursemanager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coursemanager.settings')

application = get_wsgi_application()
