# -*- coding: utf-8 -*-


class BaseUserPermission(object):
    """The interface for UserPermission backends to follow."""

    @classmethod
    def add_permission(cls, perm, user):
        """Adds a permissoin for the user."""
        raise NotImplementedError()

    @classmethod
    def remove_permission(cls, perm, user):
        """Removes a permission from the user."""
        raise NotImplementedError()

    @classmethod
    def has_permission(cls, perm, user):
        """Returns True if the user has the given permission False otherwise"""
        raise NotImplementedError()

    @classmethod
    def get_permissions(cls, user):
        """Returns a list of the users permissions."""
        raise NotImplementedError()
