import threading
from logging import Logger
from threading import Lock

import pika
from pika import BlockingConnection
from pika.adapters.blocking_connection import BlockingChannel

from detecta_shared.rabbitmq.rabbitmq_params import RabbitMQConnectionParams


class RabbitMQConnection:
    def __init__(self, connection_params: RabbitMQConnectionParams, logger: Logger, retry_count: int = 5):
        self._logger = logger
        self._retry_count = retry_count
        self._connection_params = connection_params
        self._lock = Lock()
        self.connection: BlockingConnection = None

    def try_connect(self) -> bool:
        with self._lock:
            if self.is_connected():
                return True
            credentials = pika.PlainCredentials(username=self._connection_params.login,
                                                password=self._connection_params.password)
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self._connection_params.host, credentials=credentials,
                                          port=self._connection_params.port, heartbeat=600,
                                          retry_delay=self._retry_count, connection_attempts=self._retry_count,
                                          blocked_connection_timeout=300))
            if self.is_connected():
                self._logger.info(f"Rabbitmq connection by host: {self._connection_params.host}, port: "
                                  f"{self._connection_params.port} established")
                return True
            self._logger.critical("Can't connect to rabbit")
            return False

    def create_channel(self) -> BlockingChannel:
        if not self.is_connected():
            self.try_connect()
        return self.connection.channel()

    def is_connected(self):
        return self.connection is not None and self.connection.is_open

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
