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

You will need to manually add/remove permissions to a user.  Permissions are
case insensitive.  Example:


```python

from django_generic_permissions.backends import add_permission
from django_generic_permissions.backends import remove_permission
from django_generic_permissions.backends import get_permissions

def do_stuff(request):
    user = request.user

    # Give user permissions needed
    add_permission('duper-user', user)

    # Remove the old super user permission
    remove_permission('super-duper-user', user)

    # List out the current users permissions
    get_permissions(user)
```


## Configuration

You will need to include the authentication backend supplied by this package.  If
you wish to use mongo as your database then follow the config info mentioned in the
mongoengine section.

```python
# -*- coding: utf-8 -*-
## settings.py

AUTHENTICATION_BACKENDS = [..., 'django_generic_permissions.backends.Permission']

# Only needed for SQL version
INSTALLED_APPS = (..., 'django_generic_permissions')
```

### MongoEngine
Note: This requires [mongoengine](https://github.com/hmarr/mongoengine)

```python
# settings.py
DJANGO_GENERIC_PERMISSIONS_DB = 'mongoengine'
```

### SQL
This library will default to using a SQL backend if you do not override and supply mongo
as listed above.


## Testing

To test this app it is as simple as `python manage.py test django_generic_permissions`.  Note
you need the following installed:

* Django
* mock
* mongoengine (If you use mongoengine)
