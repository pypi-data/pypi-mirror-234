from rodi import Container

from .iusersrepo import IUsersRepo
from .iusersservice import IUsersService, UserDoesNotBelong, WritePermission
from .usershttp import UsersHttpProxy, UsersHttpServer
from .usersrepo import UsersRepo
from .usersservice import UsersService


def setup_remote_client(container: Container):
    container.add_singleton(IUsersService, UsersHttpProxy)


def setup_services(container: Container):
    container.add_singleton(IUsersRepo, UsersRepo)
    container.add_singleton(IUsersService, UsersService)


__all__ = [
    'setup_remote_client', 'setup_services',
    'IUsersRepo', 'IUsersService', 'UsersHttpServer',
    'UserDoesNotBelong', 'WritePermission'
]
