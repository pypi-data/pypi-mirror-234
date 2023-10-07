from typing import AsyncIterable, Type

from aioka.action.base import BaseAction
from aioka.server.base import BaseServer


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
