from abc import ABC, abstractmethod


class BaseServer(ABC):
    def __init__(
        self,
        rmq_urls: list[str],
        service_name: str,
        queue_error_name: str = "error",
    ):
        self.rmq_urls = rmq_urls
        self.service_name = service_name
        self.queue_error_name = queue_error_name

    @classmethod
    @abstractmethod
    async def create(
        cls,
        rmq_urls: list[str],
        service_name: str,
        queue_error_name: str = "error",
        **kwargs,
    ):
        """
        The method should be a factory for asynchronous
        initialization of the class
        """
        raise NotImplementedError

    @abstractmethod
    async def bind(self, *args, **kwargs):
        """
        The method should bind
        methods to abstract routing
        """
        raise NotImplementedError

    @abstractmethod
    async def shutdown(self):
        raise NotImplementedError
