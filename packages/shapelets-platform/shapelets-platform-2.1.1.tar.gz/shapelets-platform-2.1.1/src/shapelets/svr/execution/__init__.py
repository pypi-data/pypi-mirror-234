# Copyright (c) 2022 Shapelets.io
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from rodi import Container

from .iexecutionrepo import IExecutionRepo
from .iexecutionservice import IExecutionService
from .executionhttp import ExecutionHttpProxy, ExecutionHttpServer
from .executionrepo import ExecutionRepo
from .executionservice import ExecutionService


def setup_remote_client(container: Container):
    container.add_singleton(IExecutionService, ExecutionHttpProxy)


def setup_services(container: Container):
    container.add_singleton(IExecutionRepo, ExecutionRepo)
    container.add_singleton(IExecutionService, ExecutionService)


__all__ = [
    'setup_remote_client', 'setup_services',
    'IExecutionRepo', 'IExecutionService', 'ExecutionHttpServer'
]
