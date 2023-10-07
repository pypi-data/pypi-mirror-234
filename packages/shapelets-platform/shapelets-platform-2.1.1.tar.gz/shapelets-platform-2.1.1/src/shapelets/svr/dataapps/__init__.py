# Copyright (c) 2022 Shapelets.io
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from rodi import Container

from .idataappsrepo import IDataAppsRepo
from .idataappsservice import IDataAppsService
from .dataappshttp import DataAppsHttpProxy, DataAppsHttpServer
from .dataappsrepo import DataAppsRepo
from .dataappsservice import DataAppsService


def setup_remote_client(container: Container):
    container.add_singleton(IDataAppsService, DataAppsHttpProxy)


def setup_services(container: Container):
    container.add_singleton(IDataAppsRepo, DataAppsRepo)
    container.add_singleton(IDataAppsService, DataAppsService)


__all__ = [
    'setup_remote_client', 'setup_services',
    'IDataAppsRepo', 'IDataAppsService', 'DataAppsHttpServer'
]
