# -*- coding: utf-8 -*-

from django.db import models

from .base_models import BaseUserPermission


class UserPermission(models.Model, BaseUserPermission):
    user_id = models.CharField(max_length=225, primary_key=True)
    permission_list = models.TextField()  # A comma separated string of permissions

    class Meta():
        db_table = "django_generic_userpermission"

    @classmethod
    def add_permission(cls, perm, user):
        """Add the given permission to the user."""

        # Ensure we do not create duplicate users
        try:
            user_perm = cls.objects.get(user_id=user.id)
            new_user = False
        except cls.DoesNotExist:
            user_perm = cls(user_id=user.id, permission_list=str(perm))
            new_user = True

        if new_user:
            user_perm.save(force_insert=True)
        else:
            # Make sure the usr does not already have the given permission
            existing_perms = cls.get_permissions(user)
            if perm not in existing_perms:
                existing_perms.append(perm)

            user_perm.permission_list = ",".join(existing_perms)
            user_perm.save(force_update=True)

    @classmethod
    def get_permissions(cls, user):
        """Return a list of user permissions.  If user does not exist return empty list"""
        try:
            user_perm = UserPermission.objects.get(user_id=user.id)
            return user_perm.permission_list.split(',')
        except UserPermission.DoesNotExist:
            return []

    @classmethod
    def remove_permission(cls, perm, user):
        """Removes the given permission from the user if it exists."""
        current_permissions = cls.get_permissions(user)

        # Verify the user has the given permission
        if perm in current_permissions:
            current_permissions.remove(perm)
            user_perm = cls.objects.get(user_id=user.id)

            user_perm.permission_list = ",".join(current_permissions)
            user_perm.save(force_update=True)

    @classmethod
    def has_permission(cls, perm, user):
        """Returns true if the user has the given permission. False otherwise."""
        return perm in cls.get_permissions(user)
