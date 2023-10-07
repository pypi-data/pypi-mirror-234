from abc import ABC, abstractmethod


class BaseMiddleware(ABC):
    @classmethod
    @abstractmethod
    async def create(cls):
        ...

    @abstractmethod
    async def run(self):
        ...
