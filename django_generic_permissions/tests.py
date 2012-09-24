# -*- coding: utf-8 -*-

import uuid

from django.test import TestCase

from .backends import add_permission
from .backends import get_permissions
from .backends import remove_permission


class ModelBackendTest(TestCase):

    to_add_perm_1 = 'to_add_perm_1'
    to_add_perm_2 = 'to_add_perm_2'
    to_add_perm_3 = 'to_add_perm_3'

    def test_adding_one_permission(self):
        "UNIT makes sure a permission is added correctly for a user."
        temp_user = FakeUser()
        add_permission(self.to_add_perm_1, temp_user)

        # Should have our added permission
        self.assertIn(self.to_add_perm_1, get_permissions(temp_user))

        # Should only have the one added permission
        self.assertTrue(len(get_permissions(temp_user)) == 1, "Should have added 1 permission")

    def test_adding_multiple_permissions(self):
        "UNIT make sure multiple permissions can be added correctly."
        temp_user = FakeUser()
        add_permission(self.to_add_perm_1, temp_user)
        add_permission(self.to_add_perm_2, temp_user)
        add_permission(self.to_add_perm_3, temp_user)

        added_permissions = get_permissions(temp_user)

        # Verify all permissions where added correctly and there are no extras
        self.assertIn(self.to_add_perm_1, added_permissions)
        self.assertIn(self.to_add_perm_2, added_permissions)
        self.assertIn(self.to_add_perm_3, added_permissions)

        self.assertTrue(len(added_permissions) == 3, "Should have added 3 permissions")

    def test_remove_permission(self):
        "UNIT make sure removing a permission actually removes the permission."
        temp_user = FakeUser()
        add_permission(self.to_add_perm_1, temp_user)
        add_permission(self.to_add_perm_2, temp_user)
        add_permission(self.to_add_perm_3, temp_user)

        remove_permission(self.to_add_perm_2, temp_user)

        current_permissions = get_permissions(temp_user)

        # Verify the removed permission is not in the current list
        self.assertNotIn(self.to_add_perm_2, current_permissions)
        self.assertTrue(len(current_permissions) == 2, "Only 2 permissions should remain.")


class AuthBackendTest(TestCase):
    # TODO test out authbackend
    pass


def gen_id():
    return uuid.uuid4().hex


class FakeUser(object):
    id = gen_id()
