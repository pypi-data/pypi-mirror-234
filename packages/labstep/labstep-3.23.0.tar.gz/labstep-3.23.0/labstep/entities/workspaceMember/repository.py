#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: Labstep <dev@labstep.com>

from labstep.entities.workspaceMember.model import WorkspaceMember
import labstep.generic.entity.repository as entityRepository
from labstep.service.helpers import url_join, getHeaders
from labstep.service.config import configService
from labstep.service.request import requestService
from labstep.constants import UNSPECIFIED


def getMembers(user, workspace_id, count=UNSPECIFIED, search_query=UNSPECIFIED, extraParams={}):

    params = {"group_id": workspace_id,
              "search_query": search_query, **extraParams}

    return entityRepository.getEntities(user, WorkspaceMember, count, params)


def addMember(user, workspace_id, user_id):
    params = {
        "group_id": workspace_id,
        "user_id": user_id,
    }
    return entityRepository.newEntity(user, WorkspaceMember, params)


def editMemberPermission(member, permission):
    params = {
        "type": permission,
    }
    return entityRepository.editEntity(member, params)

def setMemberPermissionRole(member, role_name:str):
    lower_case_role_name=role_name.lower()
    params={}
    org=member.__user__.getOrganization()
    permission_role = org.getPermissionRoles().get(role_name)
    if lower_case_role_name == 'viewer':
        params['type']='view'
    elif lower_case_role_name == 'editor':
        params['type']='edit'
    elif lower_case_role_name == 'owner':
        params['type']='owner'
    elif permission_role != None:
        params['permission_role_guid']=permission_role.guid
    elif permission_role == None:
        raise ValueError(f'Role name "{role_name}" does not exist.')

    return entityRepository.editEntity(member, params)


def removeMember(member):
    url = url_join(configService.getHost(), 'api/generic',
                   'user-group', str(member.id))
    headers = getHeaders(member.__user__)
    return requestService.delete(url, headers)
