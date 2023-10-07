# Copyright (c) 2022 Shapelets.io
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from rodi import Container

from .igroupsrepo import IGroupsRepo
from .groupsrepo import GroupsRepo
from .igroupsservice import IGroupsService, InvalidGroupName
from .groupservice import GroupsService
from .groupshttp import GroupsHttpProxy, GroupsHttpServer


def setup_remote_client(container: Container):
    container.add_singleton(IGroupsService, GroupsHttpProxy)


def setup_services(container: Container):
    container.add_singleton(IGroupsRepo, GroupsRepo)
    container.add_singleton(IGroupsService, GroupsService)


__all__ = [
    'setup_remote_client', 'setup_services', 'IGroupsRepo',
    'IGroupsService', 'GroupsHttpServer', 'InvalidGroupName'
]
