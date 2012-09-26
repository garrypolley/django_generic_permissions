# -*- coding: utf-8 -*-

import uuid

from django.contrib.auth.decorators import permission_required
# underscore import is done so these tests can run under mongo and sql backends
from django.contrib.auth.models import _user_has_perm
from django.core.exceptions import PermissionDenied
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.test import TestCase
from django.test.client import FakePayload
from mock import patch

from .backends import add_permission
from .backends import get_permissions
from .backends import has_permission
from .backends import Permission
from .backends import remove_permission

sample_perm = "sample-perm"


class ModelBackendTest(TestCase):
    """Tests that the UserPermission backend works. These tests can be ran with either
    mongoengine or sql as your backend.
    """

    perm_1 = 'perm_1'
    perm_2 = 'perm_2'
    perm_3 = 'perm_3'

    def test_adding_one_permission(self):
        """UNIT makes sure a permission is added correctly for a user."""
        temp_user = FakeUser()
        add_permission(self.perm_1, temp_user)

        # Should have our added permission
        self.assertIn(self.perm_1, get_permissions(temp_user))

        # Should only have the one added permission
        self.assertTrue(len(get_permissions(temp_user)) == 1, "Should have added 1 permission")

    def test_adding_multiple_permissions(self):
        """UNIT make sure multiple permissions can be added correctly."""
        temp_user = FakeUser()
        add_permission(self.perm_1, temp_user)
        add_permission(self.perm_2, temp_user)
        add_permission(self.perm_3, temp_user)

        added_permissions = get_permissions(temp_user)

        # Verify all permissions were added correctly and there are no extras
        self.assertIn(self.perm_1, added_permissions)
        self.assertIn(self.perm_2, added_permissions)
        self.assertIn(self.perm_3, added_permissions)

        self.assertTrue(len(added_permissions) == 3, "Should have added 3 permissions")

    def test_remove_permission(self):
        """UNIT make sure removing a permission actually removes the permission."""
        temp_user = FakeUser()
        add_permission(self.perm_1, temp_user)
        add_permission(self.perm_2, temp_user)
        add_permission(self.perm_3, temp_user)

        remove_permission(self.perm_2, temp_user)

        current_permissions = get_permissions(temp_user)

        # Verify the removed permission is not in the current list
        self.assertNotIn(self.perm_2, current_permissions)
        self.assertTrue(len(current_permissions) == 2, "Only 2 permissions should remain.")

    def test_has_permission(self):
        """UNIT make sure the has_permission function works."""
        temp_user = FakeUser()
        add_permission(self.perm_1, temp_user)

        self.assertTrue(has_permission(self.perm_1, temp_user))


class AuthBackendTest(TestCase):

    def setUp(self):
        """initialize a basic djagno wsgi request."""

        # copied from django.test.client
        self.environ = {
            'HTTP_COOKIE':       '',
            'PATH_INFO':         '/',
            'REMOTE_ADDR':       '127.0.0.1',
            'REQUEST_METHOD':    'GET',
            'SCRIPT_NAME':       '',
            'SERVER_NAME':       'testserver',
            'SERVER_PORT':       '80',
            'SERVER_PROTOCOL':   'HTTP/1.1',
            'wsgi.version':      (1, 0),
            'wsgi.url_scheme':   'http',
            'wsgi.input':        FakePayload(b''),
            'wsgi.errors':       '',
            'wsgi.multiprocess': True,
            'wsgi.multithread':  False,
            'wsgi.run_once':     False,
        }
        self.request = WSGIRequest(self.environ)

    @patch('django.contrib.auth.models.auth')
    def test_no_permission_403(self, mockauth):
        """UNIT if a user lacks permissoin a 403 should be returned."""
        # build up request
        mockauth.get_backends.return_value = [Permission]
        temp_user = FakeUser()
        self.request.user = temp_user

        with self.assertRaises(PermissionDenied):
            sample_view(self.request)

    @patch('django.contrib.auth.models.auth')
    def test_has_permission(self, mockauth):
        """UNIT user with pemrission should be granted access."""
        # build up request
        mockauth.get_backends.return_value = [Permission]
        temp_user = FakeUser()
        add_permission(sample_perm, temp_user)
        self.request.user = temp_user

        response = sample_view(self.request)

        self.assertEquals(response.status_code, 200)


class FakeUser(object):
    """Mocked out as much is needed for standard django user."""
    # These class variables are lambda functions because they need to be callable
    is_active = lambda x: True
    is_authenticated = lambda x: True
    is_anonymous = lambda x: False
    get_all_permissions = lambda x: []

    def __init__(self):
        self.id = uuid.uuid4().hex

    def has_perm(self, perm, obj=None):
        """Near complete coppy of the django.auth.contrib.models.User has_perm method."""
        return _user_has_perm(self, perm, None)


@permission_required(sample_perm, raise_exception=True)
def sample_view(fake_request):
    """Simple view used to validate that permission required decorator works with our
    Permission backend."""
    return HttpResponse()
