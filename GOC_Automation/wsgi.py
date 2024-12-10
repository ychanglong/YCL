"""
WSGI config for GOC_Automation project.

It exposes the WSGI callable as a modules-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GOC_Automation.settings')

application = get_wsgi_application()
