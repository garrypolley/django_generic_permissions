# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


# Get the user permission based on the backend setting
backend_db = getattr(settings, 'DJANGO_GENERIC_PERMISSIONS_DB', None)
if backend_db is None:
    from .sql_models import UserPermission
elif  backend_db == "mongo":
    from .mongo_models import UserPermission
else:
    # We do not support anythign other than mongo and sql
    raise ImproperlyConfigured("DJANGO_GENERIC_PERMISSIONS_DB only accepts 'mongo' for configuration")
