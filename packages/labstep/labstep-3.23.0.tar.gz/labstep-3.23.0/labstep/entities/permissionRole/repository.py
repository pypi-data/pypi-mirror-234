import json
from labstep.service.helpers import url_join, getHeaders
from labstep.service.config import configService
from labstep.service.request import requestService
from labstep.entities.permissionRole.model import PermissionRole
from labstep.generic.entity.repository import getEntities, newEntity, editEntity, getEntity
from labstep.constants import UNSPECIFIED


def newPermissionRole(user, organization_id, name, data, extraParams):
    params = {
        "name": name,
        "data": data,
        'organization_id': organization_id,
        **extraParams}
    return newEntity(user, PermissionRole, params)


def getPermissionRole(user,
                      permissionRole_guid,):
    return getEntity(user, PermissionRole, guid=permissionRole_guid)


def editPermissionRole(permissionRole,
                       name=UNSPECIFIED,
                       data=UNSPECIFIED,
                       extraParams={}):

    params = {"name": name,
              "data": data,
              **extraParams}

    return editEntity(permissionRole, params)


def getPermissionRoles(user,
                       count=UNSPECIFIED,
                       search_query=UNSPECIFIED,
                       extraParams={},):

    params = {
        "search_query": search_query,
        **extraParams,
    }
    return getEntities(user, PermissionRole, count, params)


def deletePermissionRole(permissionRole):
    from labstep.generic.entity.repository import deleteEntity
    
    deleteEntity(permissionRole)
    
    return None
