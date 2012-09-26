# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

backend_db = getattr(settings, 'DJANGO_GENERIC_PERMISSIONS_DB', None)
ACCEPTABLE_BACKENDS = ('mongoengine')

# Need to verify that configuration is correct in settings.py
if backend_db is not None and backend_db not in ACCEPTABLE_BACKENDS:
    raise ImproperlyConfigured("{0} is not an accpetable backend only use one of thses: {1}"
                                .format(backend_db, ACCEPTABLE_BACKENDS))


# Define the location of the backends
sql_backend = 'django_generic_permissions.sql_models'
mongoengine_backend = 'django_generic_permissions.mongoengine_models'

backend_module = (import_module(mongoengine_backend) if backend_db == 'mongoengine'
                  else import_module(sql_backend))

# Django's syncdb command will fail without this weirdness
this_module = globals()
for key in dir(backend_module):
    this_module[key] = getattr(backend_module, key)
