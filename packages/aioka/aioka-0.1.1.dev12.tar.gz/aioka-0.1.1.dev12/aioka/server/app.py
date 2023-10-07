import asyncio
import logging
import threading
import time
from contextlib import asynccontextmanager, contextmanager
from typing import Optional, Type

import uvicorn
from aio_pika import Connection
from uvicorn._types import ASGIApplication

from aioka.action.base import BaseAction
from aioka.handler.base import BaseHandler
from aioka.server.base import BaseServer
from aioka.server.master import AsyncRqMasterServer

logger = logging.getLogger(__name__)


class UvicornServer(uvicorn.Server):
    def install_signal_handlers(self):
        pass

    @contextmanager
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


class AsyncApp:
    def __init__(self, server: BaseServer):
        self.server = server
        self._handlers: list[BaseHandler] = []
        self.default_handler = BaseHandler()
        self._loop = asyncio.get_event_loop()

        self.uvicorn_asgi: Optional[uvicorn.Server] = None
        self.rq_conn: Optional[Connection] = None

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

        all_handlers = [self.default_handler] + self._handlers

        for handler in all_handlers:
            logging.info("binding handler: %s" % handler)
            handler.set_server(self.server)
            await handler.bind()

    def add_handler(self, handler: BaseHandler):
        self._handlers.append(handler)

    def add_action(self, name: str, action: BaseAction):
        self.default_handler.add_action(action_name=name, action=action)

    def add_uvicorn_asgi(self, app: Type[ASGIApplication], **kwargs):
        config = uvicorn.Config(app, lifespan="on", **kwargs)
        server = UvicornServer(config=config)
        self._uvicorn_asgi_flag = server.run_in_thread()
        self._loop.create_task(server.serve())
        self.uvicorn_asgi = server

    async def shutdown(self):
        """
        try to shut down gracefully
        """
        if self.uvicorn_asgi:  # type: uvicorn.Server
            await self.uvicorn_asgi.shutdown()
            next(self._uvicorn_asgi_flag)
        await self.server.shutdown()

        logger.info("Stopping server")


@asynccontextmanager
async def create_app(
    server: Type[BaseServer] = AsyncRqMasterServer, **kwargs
) -> AsyncApp:
    server = await server.create(**kwargs)
    app = AsyncApp(server=server)
    yield app
    await app.bind()
