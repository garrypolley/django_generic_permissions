# -*- coding: utf-8 -*-


class BaseUserPermission(object):
    """The interface for UserPermission backends to follow."""

    @classmethod
    def add_permission(user):
        """Adds a permissoin for the user."""
        raise NotImplementedError()

    @classmethod
    def remove_permission(user):
        """Removes a permission from the user."""
        raise NotImplementedError()

    @classmethod
    def has_permission(user):
        """Returns True if the user has the given permission False otherwise"""
        raise NotImplementedError()
