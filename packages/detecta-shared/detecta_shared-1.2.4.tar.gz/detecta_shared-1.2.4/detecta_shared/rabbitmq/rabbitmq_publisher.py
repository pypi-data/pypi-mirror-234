import logging
import threading
from typing import Optional

import jsonpickle
import pika
from pika.adapters.blocking_connection import BlockingChannel
from pika.exceptions import ConnectionClosed

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

    def _publish(self, event: IntegrationEvent, message_params: RabbitMQSendParams):
        if not self._connection.is_connected():
            self._connection.try_connect()
        if not self._channel or self._channel.is_closed or self.multithread_mode:
            channel = self._connection.create_channel()
            self._channel = channel
            self._logger.info(f"Channel RabbitMQ created to send: {type(event).__name__}")
        else:
            channel = self._channel
        try:
            body = jsonpickle.dumps(event, unpicklable=False).encode()
            live_time = None
            if message_params.message_live_milliseconds:
                live_time = str(message_params.message_live_milliseconds)
            self._logger.info(f"Publishing to RabbitMQ {type(event).__name__} ")
            channel.basic_publish(exchange=self._publisher_params.exchange,
                                  routing_key=message_params.routing_key,
                                  body=body, properties=pika.BasicProperties(delivery_mode=2,
                                                                             expiration=live_time))
        except Exception:
            if channel.is_open:
                channel.close()
            raise
        finally:
            if self.multithread_mode:
                if channel.is_open:
                    channel.close()

    def publish(self, event: IntegrationEvent, message_params: RabbitMQSendParams):
        try:
            self._publish(event, message_params)
        except (pika.exceptions.AMQPChannelError, pika.exceptions.AMQPConnectionError) as ex:
            self._logger.warning(f"Can't send message to rabbitmq error: {ex}, trying again")
            self._publish(event, message_params)
