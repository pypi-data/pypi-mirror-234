import logging
import threading
from typing import Optional

import jsonpickle
import pika
from pika.adapters.blocking_connection import BlockingChannel

from detecta_shared.abstractions.integration_events import IntegrationEvent

from detecta_shared.rabbitmq.rabbitmq_connection import RabbitMQConnection

from detecta_shared.rabbitmq.rabbitmq_params import RabbitMQPublisherParams, RabbitMQSendParams


class RabbitMQPublisher:

    def __init__(self, params: RabbitMQPublisherParams, connection: RabbitMQConnection,
                 logger: logging.Logger, multithread_mode=False):
        self.multithread_mode = multithread_mode
        self._logger = logger
        self._connection = connection
        self._publisher_params = params
        self._channel: Optional[BlockingChannel] = None
        self._lock = threading.Lock()

    def _publish(self, event: IntegrationEvent, message_params: RabbitMQSendParams):
        if not self._connection.is_connected():
            self._connection.try_connect()
        with self._lock:
            if not self._channel or self._channel.is_closed or self.multithread_mode:
                self._channel = self._connection.create_channel()
            channel = self._channel
        try:
            self._logger.info(f"Channel RabbitMQ created to send: {type(event).__name__}")
            body = jsonpickle.dumps(event, unpicklable=False).encode()
            live_time = None
            if message_params.message_live_milliseconds:
                live_time = str(message_params.message_live_milliseconds)
            self._logger.info(f"Publishing to RabbitMQ {type(event).__name__} ")
            channel.basic_publish(exchange=self._publisher_params.exchange,
                                  routing_key=message_params.routing_key,
                                  body=body, properties=pika.BasicProperties(delivery_mode=2,
                                                                             expiration=live_time))
        finally:
            if self.multithread_mode:
                channel.close()

    def publish(self, event: IntegrationEvent, message_params: RabbitMQSendParams):
        try:
            self._publish(event, message_params)
        except (pika.exceptions.ConnectionClosed, pika.exceptions.ChannelWrongStateError):
            self._logger.warning("Connection closed, reconnecting to rabbitmq")
            self._connection.try_connect()
            self._publish(event, message_params)
