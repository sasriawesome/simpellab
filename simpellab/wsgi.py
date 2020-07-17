"""
WSGI config for Simpellab project.

"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simpellab.settings')
application = get_wsgi_application()
