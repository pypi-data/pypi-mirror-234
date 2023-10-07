import asyncio
import logging
from typing import Optional

import aio_pika
from aio_pika import Channel, DeliveryMode, Message
from aio_pika.abc import (
    AbstractExchange,
    AbstractQueue,
    AbstractRobustConnection,
    ExchangeType,
)
from aio_pika.pool import Pool
from aiormq.tools import awaitable

from aioka.action.base import BaseAction
from aioka.server.base import BaseServer

logger = logging.getLogger(__name__)


class Worker:
    __slots__ = (
        "queue",
        "consumer_tag",
        "loop",
    )

    def __init__(self, queue: AbstractQueue, consumer_tag: str, loop):
        self.queue = queue
        self.consumer_tag = consumer_tag
        self.loop = loop

    def close(self) -> asyncio.Task:
        """Cancel subscription to the channel"""

        async def closer():
            await self.queue.cancel(self.consumer_tag)

        return self.loop.create_task(closer())


class Master:
    """
    Change serialize/deserialize methods for json messages
    """

    __slots__ = (
        "channel",
        "_loop",
        "proxy",
        "_workers",
        "default_exchange",
        "service_name",
        "queue_error_name",
        "exchange",
        "exchange_type",
    )

    def __init__(
        self,
        service_name: str,
        queue_error_name: str,
        channel: Channel,
        exchange: str,
        exchange_type: ExchangeType,
    ):
        self.service_name = service_name
        self.queue_error_name = queue_error_name
        self.channel = channel
        self._workers: list[Worker] = []
        self._loop = asyncio.get_event_loop()
        self.exchange = exchange
        self.exchange_type = exchange_type

    async def create_queue(self, channel_name, **kwargs) -> AbstractQueue:
        return await self.channel.declare_queue(channel_name, **kwargs)

    async def create_worker(
        self, channel_name: str, action: BaseAction, **kwargs
    ) -> Worker:
        queue = await self.create_queue(channel_name, **kwargs)

        await action.set_client(self.publish)
        if hasattr(action.consume, "_is_coroutine"):
            fn = action.consume
        else:
            fn = awaitable(action.consume)

        consumer_tag = await queue.consume(fn)
        worker = Worker(queue, consumer_tag, self._loop)
        await worker.queue.bind(
            self.default_exchange, routing_key=channel_name
        )
        self._workers.append(worker)
        return worker

    async def publish(
        self,
        message: bytes,
        routing_key: Optional[str] = None,
        delivery_mode: DeliveryMode = DeliveryMode.PERSISTENT,
        content_type: str = "application/json",
        mandatory: bool = False,  # Check routing_key exists
        immediate: bool = False,  # Request immediate delivery
        exchange_name: str = None,
        **message_kwargs,
    ):
        if not exchange_name:
            exchange: AbstractExchange = self.default_exchange
        else:
            exchange: AbstractExchange = await self.channel.get_exchange(
                exchange_name
            )

        message = Message(
            body=message,
            content_type=content_type,
            delivery_mode=delivery_mode,
            **message_kwargs,
        )

        if routing_key is None:
            routing_key = f"{self.service_name}.{self.queue_error_name}"
        await exchange.publish(
            message=message,
            routing_key=routing_key,
            mandatory=mandatory,
            immediate=immediate,
        )

    async def __aenter__(self):
        self.default_exchange = await self.channel.declare_exchange(
            self.exchange,
            self.exchange_type,
            durable=True,
        )
        error_queue_name = f"{self.service_name}" f".{self.queue_error_name}"
        error_queue = await self.create_queue(error_queue_name)
        await error_queue.bind(
            self.default_exchange, routing_key=error_queue_name
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        for worker in self._workers:
            worker.close()

    @property
    def workers(self):
        return self._workers


class AsyncRqMasterServer(BaseServer):
    """
    Asynchronous server for working with queues
     using the Master-Worker pattern
    """

    def __init__(
        self,
        rmq_urls: list[str],
        service_name: str,
        connection_pool_size: int = 2,
        channel_pool_size: int = 10,
    ):
        super().__init__(rmq_urls, service_name)
        self.default_exchange: AbstractExchange | None = None
        self.master: Master | None = None
        self.connection_pool_size = connection_pool_size
        self.channel_pool_size = channel_pool_size

    @classmethod
    async def create(
        cls,
        exchange: str = "",
        exchange_type: ExchangeType = ExchangeType.DIRECT,
        prefetch_count: int = 0,
        prefetch_size: int = 0,
        durable: bool = True,
        **kwargs,
    ):
        """Fabric for async init class"""
        self = AsyncRqMasterServer(**kwargs)

        async def get_connection() -> AbstractRobustConnection:
            return await aio_pika.connect_robust(self.rmq_urls[0])

        async def get_channel() -> aio_pika.Channel:
            async with self.connection_pool.acquire() as connection:
                return await connection.channel()

        self.connection_pool = Pool(
            get_connection, max_size=self.connection_pool_size
        )
        self.channel_pool = Pool(get_channel, max_size=self.channel_pool_size)

        async with self.channel_pool.acquire() as channel:  # type: Channel
            await channel.set_qos(
                prefetch_count=prefetch_count, prefetch_size=prefetch_size
            )
            async with Master(
                channel=channel,
                service_name=self.service_name,
                queue_error_name=self.queue_error_name,
                exchange=exchange,
                exchange_type=exchange_type,
            ) as master:  # type: Master
                self.master = master
                self.default_exchange = (
                    await self.master.channel.declare_exchange(
                        name=exchange,
                        type=exchange_type,
                        durable=durable,
                    )
                )
                error_queue = await self.master.create_queue(
                    f"{self.service_name}.{self.queue_error_name}"
                )
                await error_queue.bind(self.default_exchange)
                return self

    async def bind(self, method_name: str, procedure: BaseAction):
        """Method for creating queue and binding actions"""
        worker = await self.master.create_worker(
            f"{self.service_name}.{method_name}", procedure
        )
        await worker.queue.bind(self.default_exchange)

    async def shutdown(self):
        for worker in self.master.workers:
            worker.close()
