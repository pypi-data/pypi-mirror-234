from abc import ABC, abstractmethod
from typing import Callable, Coroutine, Optional

from aio_pika import IncomingMessage


class BaseAction(ABC):
    """
    Base class for actions called by routes

    :param action_name: Procedure name to indicate in routing
    """

    def __init__(self, action_name: str, service_name: str):
        self.action_name = action_name
        self.client: Optional[Callable[..., Coroutine[any, any, any]]] = None
        self._service_name = service_name

    async def set_client(
        self, client: Callable[..., Coroutine[any, any, any]]
    ):
        self.client = client

    @abstractmethod
    async def __call__(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def consume(self, message: IncomingMessage):
        raise NotImplementedError
