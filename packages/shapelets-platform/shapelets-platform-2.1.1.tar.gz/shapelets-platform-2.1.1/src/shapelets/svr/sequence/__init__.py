from rodi import Container

from .isequencerepo import ISequenceRepo
from .isequenceservice import ISequenceService
from .sequencehttp import SequenceHttpProxy, SequenceHttpServer
from .sequencerepo import SequenceRepo
from .sequenceservice import SequenceService


def setup_remote_client(container: Container):
    container.add_singleton(ISequenceService, SequenceHttpProxy)


def setup_services(container: Container):
    container.add_singleton(ISequenceRepo, SequenceRepo)
    container.add_singleton(ISequenceService, SequenceService)


__all__ = [
    'setup_remote_client', 'setup_services',
    'ISequenceRepo', 'ISequenceService', 'SequenceHttpServer'
]
