from abc import ABC, abstractmethod
from typing import Callable, Coroutine, Optional

from aio_pika import IncomingMessage


class BaseAction(ABC):
    """
    Base class for actions called by routes

    :param action_name: Procedure name to indicate in routing
    """

    def __init__(self, action_name: str):
        self.action_name = action_name
        self.client: Optional[Callable[..., Coroutine[any, any, any]]] = None
        self._service_name: str | None = None

    @property
    def service_name(self):
        return self._service_name

    async def set_client(
        self, client: Callable[..., Coroutine[any, any, any]]
    ):
        self.client = client

    @service_name.setter
    def service_name(self, value: str):
        if isinstance(value, str):
            self._service_name = value
        else:
            raise ValueError("service_name must be str, not %s", type(value))

    @abstractmethod
    async def __call__(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def consume(self, message: IncomingMessage):
        raise NotImplementedError
