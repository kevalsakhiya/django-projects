***REMOVED***
ASGI config for mysite project.

It exposes the ASGI callable as a module-level variable named ``application``.

***REMOVED***
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
***REMOVED***

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_asgi_application()
