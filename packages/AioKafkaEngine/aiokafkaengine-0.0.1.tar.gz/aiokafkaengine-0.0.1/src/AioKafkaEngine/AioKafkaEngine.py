import asyncio
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from asyncio import Queue
import json
import logging

logger = logging.getLogger(__name__)


def retry_on_exception(max_retries=3, retry_interval=5):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    await func(*args, **kwargs)
                    return wrapper
                except Exception as e:
                    logger.error(f"Error: {e}")
                    await asyncio.sleep(retry_interval)
                retries += 1

        return wrapper

    return decorator


def async_background_task(func):
    async def wrapper(*args, **kwargs):
        task = asyncio.ensure_future(func(*args, **kwargs))
        return task

    return wrapper


class AioKafkaEngine:
    consumer = None
    producer = None

    def __init__(
        self,
        bootstrap_servers: list[str],
        topic: str,
        send_queue_size: int = 100,
        receive_queue_size: int = 100,
    ):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.receive_queue = Queue(maxsize=receive_queue_size)
        self.send_queue = Queue(maxsize=send_queue_size)

    async def start_consumer(self, group_id: str) -> Queue:
        self.consumer = AIOKafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        await self.consumer.start()

    async def start_producer(self):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode(),
        )
        await self.producer.start()

    @async_background_task
    @retry_on_exception()
    async def consume_messages(self):
        if self.consumer is None:
            raise ValueError("Consumer not started. Call start_consumer() first.")

        async for message in self.consumer:
            value = message.value
            await self.receive_queue.put(value)

    @async_background_task
    @retry_on_exception()
    async def produce_messages(self):
        if self.producer is None:
            raise ValueError("Producer not started. Call start_producer() first.")

        while True:
            message = await self.send_queue.get()
            await self.producer.send(self.topic, value=message)
            self.send_queue.task_done()

    async def stop_consumer(self):
        if self.consumer:
            await self.consumer.stop()

    async def stop_producer(self):
        if self.producer:
            await self.producer.stop()

    def is_ready(self):
        return self.consumer is not None or self.producer is not None
