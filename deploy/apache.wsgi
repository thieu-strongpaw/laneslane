"""Dedicated entry point: do not change the existing site's WSGI script."""
import os
from django.core.wsgi import get_wsgi_application

os.environ["DJANGO_SETTINGS_MODULE"] = "laneslane.production"
application = get_wsgi_application()
