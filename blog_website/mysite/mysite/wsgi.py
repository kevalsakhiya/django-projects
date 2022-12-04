***REMOVED***
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

***REMOVED***
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
***REMOVED***

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_wsgi_application()
