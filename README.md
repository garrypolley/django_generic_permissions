django_generic_permissions
========================

A simple Authentication Backend to manage specific permissions.


### Use Cases

* View specific permissions
* Easy to manage multiple model permissions
* Custom permissions applied at any layer in the application

## Usage

```python
# -*- coding: utf-8 -*-
## views.py

from django.auth.decorators import permission_required


@permission_required('super-duper-user')
def show_all_user_data(request):
    # Do stuff
    return ALL_USER_DATA
```

You will need to manually add/remove permissions to a user.  Example:


## Configuration

You will need to include the authentication middleware supplied by this package.  If
you wish to use mongo as your backend then follow the config info mentioned below.

```python
# -*- coding: utf-8 -*-
## settings.py

AUTHENTICATION_BACKENDS = [..., 'django_generic_permissions.backends.Permission']
```

### Mongo
```python
# settigns.py
DJANGO_GENERIC_PERMISSIONS_DB = 'mongo'
```

### SQL
This library will default to using a SQL backend if you do not override and supply mongo
as listed above.
