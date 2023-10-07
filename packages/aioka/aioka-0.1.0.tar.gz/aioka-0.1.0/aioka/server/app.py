import asyncio
import contextlib
import logging
import threading
import time
from typing import Optional, Type

import uvicorn
from aio_pika import Connection
from uvicorn._types import ASGIApplication

from aioka.handler.base import BaseHandler
from aioka.server.base import BaseServer

logger = logging.getLogger(__name__)


class UvicornServer(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    @contextlib.contextmanager
    def run_in_thread(self):
        thread = threading.Thread(target=self.run)
        thread.start()
        try:
            while not self.started:
                time.sleep(1e-3)
            yield
        finally:
            self.should_exit = True
            thread.join()


def get_handlers() -> dict[str, Type[BaseHandler]]:
    return {
        subclass.__name__: subclass
        for subclass in set(BaseHandler.__subclasses__())
    }


class AsyncApp:
    def __init__(
        self,
        server: BaseServer,
        enable_handlers: list[str] | None = None,
        log_config: dict | None = None,
    ):
        self.server = server
        self._handlers: dict[str, Type[BaseHandler]] = get_handlers()
        self.handlers: list[str] = []
        self._loop = asyncio.get_event_loop()

        self.uvicorn_asgi: Optional[uvicorn.Server] = None
        self.rq_conn: Optional[Connection] = None
        self._enable_handlers = enable_handlers
        self._log_config = log_config

    def run(self):
        logger.info("%s try start", self.server.service_name)
        try:
            self._loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            logger.info("%s stopped", self.server.service_name)

    async def bind(self):
        logger.debug(self._handlers)
        if self._enable_handlers is None:
            self.handlers = list(self._handlers.values())
        elif len(self._enable_handlers) > 0:
            self.handlers = [
                self._handlers[name] for name in self._enable_handlers
            ]

        for handler in self.handlers:
            logging.info("binding handler: %s" % handler.__name__)
            handler = await handler.create(self.server)
            await handler.bind()

    def add_uvicorn_asgi(self, app: Type[ASGIApplication], **kwargs):
        config = uvicorn.Config(
            app, log_config=self._log_config, lifespan="on", **kwargs
        )
        server = UvicornServer(config=config)
        with server.run_in_thread():
            self._loop.create_task(server.serve())
            self.uvicorn_asgi = server

    async def shutdown(self):
        """
        try to shut down gracefully
        """
        # if self.uvicorn_asgi:  # type: uvicorn.Server
        #     await self.uvicorn_asgi.shutdown()
        await self.server.shutdown()

        logger.info("Stopping server")


async def async_create_app(server: Type[BaseServer], **kwargs) -> AsyncApp:
    server = await server.create(**kwargs)
    app = AsyncApp(server)
    await app.bind()
    return app


def create_app_contextmanager(
    server: Type[BaseServer],
    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop(),
    **kwargs,
):
    app = loop.run_until_complete(async_create_app(server, **kwargs))
    return app


def create_app(server: Type[BaseServer]):
    return create_app_contextmanager(server)
