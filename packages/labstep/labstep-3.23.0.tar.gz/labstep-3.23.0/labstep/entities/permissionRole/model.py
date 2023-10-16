#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Labstep <dev@labstep.com>

from labstep.generic.entity.model import Entity
from labstep.constants import UNSPECIFIED

class PermissionRole(Entity):
    __entityName__ = "permission-role"
    __hasGuid__ = True
    __unSearchable__=True

    def edit(self, name=UNSPECIFIED, 
             data=UNSPECIFIED, 
             extraParams={}):
        """
        Edit an existing Permission Role.

        Parameters
        ----------
        name (str)
            The name of the Protocol.
        data (dict):
            JSON representing permission data.

        Returns
        -------
        :class:`~labstep.entities.permissionRole.model.PermissionRole`
            An object representing the edited Permission Role.

        Example
        -------
        ::

            my_org = user.getOrganization()
            permission_role = my_org.getPermissionRole(10000)
            permission_role.edit(name='A New Protocol Name')
        """
        import labstep.entities.permissionRole.repository as PermissionRoleRepository

        return PermissionRoleRepository.editPermissionRole(
            self, name=name, data=data, extraParams=extraParams
        )
    
def delete(self):
    """
        Delete an existing Permission Role.

        Parameters
        ----------
        Permission role (obj)
            The Permission role to delete.

        Returns
        -------
        None
    """
    import labstep.entities.permissionRole.repository as PermissionRoleRepository

    return PermissionRoleRepository.deletePermissionRole(self)
    