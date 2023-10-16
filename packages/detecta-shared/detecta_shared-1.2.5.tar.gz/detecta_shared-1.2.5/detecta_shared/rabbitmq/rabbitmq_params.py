from typing import Optional


class RabbitMQConnectionParams:
    def __init__(self, host: str, login: str, password: str, port: int):
        self.password = password
        self.port = port
        self.login = login
        self.host = host


class RabbitMQListenerParams:
    def __init__(self, exchange_type: str, queue: str, exchange: str):
        self.exchange = exchange
        self.queue = queue
        self.exchange_type = exchange_type

class RabbitMQPublisherParams:
    def __init__(self, exchange_type: str, queue: str, exchange: str):
        self.exchange = exchange
        self.queue = queue
        self.exchange_type = exchange_type

class RabbitMQSendParams:
    def __init__(self, routing_key: str, message_live_milliseconds: Optional[int]):
        self.message_live_milliseconds = message_live_milliseconds
        self.routing_key = routing_key
