import functools
import logging
import threading
import time
from typing import Optional

import jsonpickle
import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import ConnectionClosed

from detecta_shared.abstractions.integration_events import IntegrationEvent

from detecta_shared.rabbitmq.rabbitmq_connection import RabbitMQConnection

from detecta_shared.rabbitmq.rabbitmq_params import RabbitMQPublisherParams, RabbitMQSendParams


class RabbitMQPublisher(threading.Thread):

    def __init__(self, params: RabbitMQPublisherParams, connection: RabbitMQConnection, logger: logging.Logger):
        super().__init__()
        self._logger = logger
        self._connection = connection
        self._publisher_params = params
        self._channel: Optional[BlockingChannel] = None
        self.start()

    def run(self) -> None:
        while True:
            try:
                if not self._connection.is_connected():
                    self._connection.try_connect()
                self._connection.connection.process_data_events(time_limit=1)
            except Exception as ex:
                self._logger.warning(f"Connection rabbit publisher failed, reconnecting... Error: {ex}")
                time.sleep(3)

    def _publish(self, event: IntegrationEvent, message_params: RabbitMQSendParams, retry_count: int):
        if not self._channel or self._channel.is_closed:
            self._channel = self._connection.create_channel()
            self._logger.info(f"Channel RabbitMQ created to send: {type(event).__name__}")

        try:
            body = jsonpickle.dumps(event, unpicklable=False).encode()
            live_time = None
            if message_params.message_live_milliseconds:
                live_time = str(message_params.message_live_milliseconds)
            self._logger.info(f"Publishing to RabbitMQ {type(event).__name__} ")
            self._channel.basic_publish(exchange=self._publisher_params.exchange,
                                        routing_key=message_params.routing_key,
                                        body=body, properties=pika.BasicProperties(delivery_mode=2,
                                                                                   expiration=live_time))
        except (pika.exceptions.AMQPChannelError, pika.exceptions.AMQPConnectionError) as ex:
            if retry_count > 10:
                raise
            self._logger.warning(
                f"Can't send message to rabbitmq error: {ex}, trying again, retry count: {retry_count}")
            self._publish(event, message_params, retry_count + 1)

    def publish(self, event: IntegrationEvent, message_params: RabbitMQSendParams):
        if not self._connection.is_connected():
            is_connected = self._wait_to_connect(10)
            if not is_connected:
                raise Exception("Can't publish event. Error: connection time out")
        self._connection.connection.add_callback_threadsafe(lambda: self._publish(event, message_params, 0))
        # self._connection.connection.process_data_events(time_limit=0)
        # self._publish(event, message_params)

    def _wait_to_connect(self, secs: float) -> bool:
        wait_time = time.time() + secs
        while time.time() < wait_time:
            if self._connection.is_connected() or self._connection.try_connect():
                return True
        return False
