# File should remain unchangd.
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weatherreport.settings')

application = get_wsgi_application()
