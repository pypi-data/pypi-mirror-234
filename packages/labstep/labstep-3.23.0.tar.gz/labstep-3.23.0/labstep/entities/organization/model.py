#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Labstep <dev@labstep.com>

import labstep.entities.organizationUser.repository as organizationUserRepository
from labstep.generic.entity.model import Entity
import labstep.generic.entity.repository as entityRepository
import labstep.entities.workspace.repository as workspaceRepository
import labstep.entities.invitation.repository as invitationRepository
from labstep.constants import UNSPECIFIED


class Organization(Entity):
    __entityName__ = "organization"

    def edit(self, name, extraParams={}):
        """
        Edit Organization.

        Parameters
        ----------
        name (str)
            The name of the Organization.

        Returns
        -------
        :class:`~labstep.entities.organization.model.Organization`
            An object representing the organization.

        Example
        -------
        ::

            my_organization.edit(name='My new organization.')
        """
        import labstep.entities.organization.repository as organizationRepository

        return organizationRepository.editOrganization(self, name, extraParams=extraParams)

    def inviteUsers(self, emails, workspace_id=UNSPECIFIED):
        """
        Invite users to your organization.

        Parameters
        ----------
        emails (list)
            A list of email address to send invitations to.

        workspace_id (int)
            Optionally specifiy the id of a workspace to add the new users to.

        Example
        -------
        ::

            my_organization.inviteUsers(emails=['user1@labstep.com','user2@labstep.com'],
                workspace_id=123)
        """
        return invitationRepository.newInvitations(self.__user__,
                                                   invitationType='organization',
                                                   emails=emails,
                                                   organization_id=self.id,
                                                   workspace_id=workspace_id)

    def getWorkspaces(self, count=UNSPECIFIED, search_query=UNSPECIFIED):
        """
        Get the workspaces in your Organization

        Parameters
        ----------
        count (int)
            Number of workspaces to return.

        search_query (string)
            Search for specific workspaces by name.

        Returns
        -------
        List[:class:`~labstep.entities.workspace.model.Workspace`]
            A list of workspaces in the organization.

        Example
        -------
        ::

            workspaces = my_organization.getWorkspaces(search_query='R&D Workspace')
        """
        return workspaceRepository.getWorkspaces(self.__user__,
                                                 count=count,
                                                 search_query=search_query,
                                                 extraParams={'organization_id': self.id})

    def getUsers(self, count=UNSPECIFIED, extraParams={}):
        """
        Get the users in your Organization.

        Returns
        -------
        List[:class:`~labstep.entities.organizationUser.model.OrganizationUser`]
            A list of users in your organization

        Example
        -------
        ::

            users = my_organization.getUsers()
            user[0].disable()
        """
        return organizationUserRepository.getOrganizationUsers(self,
                                                               count=count,
                                                               extraParams=extraParams)

    def getPendingInvitations(self, extraParams={}):
        """
        Get pending invitations to your Organization.

        Returns
        -------
        List[:class:`~labstep.entities.invitation.model.Invitation`]
            A list of invitations sent

        Example
        -------
        ::

            invitations = my_organization.getPendingInvititations()
        """
        return invitationRepository.getInvitations(self.__user__,
                                                   self.id,
                                                   extraParams={'has_invited_user': False,
                                                                **extraParams})

    def newPermissionRole(self,
                          name,
                          data=None,
                          extraParams={}):
        """
        Create a new Permission Role in your Organization.

        Parameters
        ----------
        name (str)
            Name of the new Permission Role.
        data (obj)
            A JSON object representing permission role data.

        Returns
        -------
        :class:`~labstep.entities.permissionRole.model.PermissionRole`
            An object representing an Permission Role in Labstep.

        Example
        -------
        ::

            new_permission_role = my_organization.newPermissionRole(name='Inventory Manager')
        """
        if data == None:
            data = {
                'device':
                    {
                        'assign': 'all',
                        'comment': 'all',
                        'create': 'all',
                        'create_bookings': 'all',
                        'edit': 'all',
                        'send_data': 'all',
                        'share': 'none',
                        'soft_delete': 'all'
                    },
                'experiment_workflow':
                    {
                        'assign': 'all',
                        'comment': 'all',
                        'create': 'all',
                        'edit': 'all',
                        'lock': 'all',
                        'share': 'none',
                        'sign': 'all',
                        'soft_delete': 'all',
                        'unlock': 'none'
                    },
                'folder':
                    {
                        'create': 'all',
                        'edit': 'all',
                        'soft_delete': 'all'
                    },
                'group':
                    {
                        'comment': 'all'
                    },
                'order_request':
                    {
                        'assign': 'all',
                        'comment': 'all',
                        'create': 'all',
                        'edit': 'all',
                        'share': 'none',
                        'soft_delete': 'all'
                    },
                'protocol_collection':
                    {
                        'assign': 'all',
                        'comment': 'all',
                        'create': 'all',
                        'edit': 'all',
                        'share': 'none',
                        'soft_delete': 'all'
                    },
                'purchase_order':
                    {
                        'add_order_requests': 'all',
                        'assign': 'all',
                        'comment': 'all',
                        'create': 'all',
                        'edit': 'all',
                        'soft_delete': 'all'
                    },
                'resource':
                    {
                        'add_items': 'all',
                        'assign': 'all',
                        'comment': 'all',
                        'create': 'all',
                        'edit': 'all',
                        'share': 'none',
                        'soft_delete': 'all'
                    },
                'resource_item':
                    {
                        'assign': 'all',
                        'comment': 'all',
                        'edit': 'all',
                        'soft_delete': 'all'
                    },
                'resource_location':
                    {
                        'assign': 'all',
                        'comment': 'all',
                        'create': 'all',
                        'edit': 'all',
                        'soft_delete': 'all'
                    },
                'resource_template':
                    {
                        'assign': 'all',
                        'create': 'all',
                        'edit': 'all',
                        'share': 'none',
                        'soft_delete': 'all'
                    },
                'tag':
                    {
                        'create': 'all',
                        'delete': 'all',
                        'edit': 'all'
                    }
            }

        import labstep.entities.permissionRole.repository as PermissionRoleRepository
        self.__user__ = self.__user__.update()
        return PermissionRoleRepository.newPermissionRole(
            self.__user__, organization_id=self.guid, name=name, data=data, extraParams=extraParams
        )

    def getPermissionRoles(self, count=UNSPECIFIED, search_query=UNSPECIFIED, extraParams={}):
        """
        Retrieve a list of organizations's PermissionRoles on Labstep,
        which can be filtered using the parameters:

        Parameters
        ----------
        count (int)
            The number of PermissionRoles to retrieve.
        search_query (str)
            Search for PermissionRoles with this 'name'.

        Returns
        -------
        List[:class:`~labstep.entities.permissionRoles.model.PermissionRoles`]
            A list of permissionRoles objects.

        Example
        -------
        ::

            permission_roles = my_organization.getPermissionRoles(search_query='Inventory')
        """
        import labstep.entities.permissionRole.repository as PermissionRoleRepository
        self.__user__ = self.__user__.update()
        return PermissionRoleRepository.getPermissionRoles(
            self.__user__, count=count, search_query=search_query, extraParams=extraParams)

    def getPermissionRole(self, permission_role_guid):
        """
        Retrieve a specific Labstep PermissionRole.

        Parameters
        ----------
        resource_category_guid (str)
            The guid of the PermissionRole to retrieve.

        Returns
        -------
        :class:`~labstep.entities.permissionRole.model.PermissionRole`
            An object representing a PermissionRole on Labstep.

        Example
        -------
        ::

            permission_role = my_organization.getPermissionRole(17000)
        """
        import labstep.entities.permissionRole.repository as PermissionRoleRepository
        self.__user__ = self.__user__.update()
        return PermissionRoleRepository.getPermissionRole(
            self.__user__, permission_role_guid
        )
