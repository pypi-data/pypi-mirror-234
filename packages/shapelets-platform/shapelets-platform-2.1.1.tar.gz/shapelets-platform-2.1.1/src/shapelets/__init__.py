from __future__ import annotations
from ._relations import DataSet, CSVCompression, SandBox, sandbox, ParquetCodec
from ._cli import cli
from ._api import (
    add_server,
    add_user_to_group,
    create_group,
    delete_group,
    forget_me,
    get_ID,
    list_available_servers,
    list_current_groups,
    list_current_users,
    login,
    register,
    remove_user_from_group,
    unregister
)
from ._uom import *
from ._version import version as __version__
from . import apps
from . import svr
from . import functions
from . import _uom

svr.get_service(svr.ITelemetryService).library_loaded()

__all__ = ["__version__", "svr", "apps"]
__all__ += ["cli"]
__all__ += ['DataSet', 'CSVCompression', 'SandBox', 'sandbox', 'ParquetCodec', 'functions']
__all__ += ['add_user_to_group', 'add_server', 'create_group', 'delete_group' 'forget_me', 'list_current_groups',
            'list_current_users', 'login', 'register', 'remove_user_from_group', 'unregister']
__all__ += _uom.__all__
