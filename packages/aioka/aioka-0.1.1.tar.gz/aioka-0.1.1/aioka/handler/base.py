from abc import ABC, abstractmethod
from typing import AsyncIterable, Callable, Coroutine, Optional, Type

from aio_pika import IncomingMessage
from pydantic import BaseModel

from aioka.server.base import BaseServer


class BaseAction(ABC):
    """
    Base class for actions called by routes

    :param action_name: Procedure name to indicate in routing
    """

    def __init__(self, action_name: str):
        self.action_name = action_name
        self.client: Optional[Callable[..., Coroutine[any, any, any]]] = None

    async def set_client(
        self, client: Callable[..., Coroutine[any, any, any]]
    ):
        self.client = client

    @abstractmethod
    async def __call__(self, payload: BaseModel):
        raise NotImplementedError

    @abstractmethod
    async def consume(self, message: IncomingMessage):
        raise NotImplementedError


class BaseHandler:
    """
    Basic implementation of the handler.
    Binds actions to rft_proxy calls and initializes the client
    """

    __slots__ = ("routes", "server")

    routes: dict[str, Type[BaseAction]]

    @classmethod
    async def create(cls, server: BaseServer):
        """
        Фабрика для асинхронного создания инстанса класса

        :param server: Кастомный сервер, базирующейся на BaseServer
        """
        self = BaseHandler()
        self.server = server
        self.routes = cls.routes
        return self

    async def _bind_procedures(self) -> AsyncIterable:
        for route, action in self.routes.items():
            action_instance: BaseAction = action(route)
            yield action_instance

    async def bind(self):
        """Метод для биндинга процедур к серверу"""
        async for procedure in self._bind_procedures():
            await self.server.bind(procedure.action_name, procedure)
