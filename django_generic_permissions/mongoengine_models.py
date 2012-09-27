# -*- coding: utf-8 -*-

from mongoengine.document import Document
from mongoengine.fields import StringField
from mongoengine.fields import ListField

from .base_models import BaseUserPermission


class UserPermission(Document, BaseUserPermission):
    user_id = StringField(db_field='ui', primary_key=True)
    permission_list = ListField(StringField(), db_field='pl')

    meta = {
        'collection': 'user_permission',
        'index_types': False,
    }

    @classmethod
    def add_permission(cls, perm, user):
        """Add the given permission to the user."""

        # Ensure we do not create duplicate users
        try:
            user_perm = cls.objects.get(user_id=str(user.id))
            new_user = False
        except cls.DoesNotExist:
            user_perm = cls(user_id=str(user.id), permission_list=[perm])
            new_user = True

        if new_user:
            user_perm.save()
        else:
            # Make sure the usr does not already have the given permission
            if perm not in user_perm.permission_list:
                user_perm.permission_list.append(perm)
                user_perm.save()

    @classmethod
    def get_permissions(cls, user):
        """Return a list of user permissions.  If user does not exist return empty list"""

        try:
            user_perm = UserPermission.objects.get(user_id=str(user.id))
            return user_perm.permission_list
        except UserPermission.DoesNotExist:
            return []

    @classmethod
    def remove_permission(cls, perm, user):
        """Removes the given permission from the user if it exists.
        Raises an exception if the permission does not exist."""
        user_perm = cls.objects.get(user_id=str(user.id))

        # Verify the user has the given permission
        if perm in user_perm.permission_list:
            user_perm.permission_list.remove(perm)
            user_perm.save()

    @classmethod
    def has_permission(cls, perm, user):
        """Returns true if the user has the given permission. False otherwise."""
        return perm in cls.get_permissions(user)
