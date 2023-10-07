import logging
from typing import Type, Dict, Optional

from detecta_shared.abstractions.integration_events import TEvent, IntegrationEvent, IntegrationEventHandler
from detecta_shared.abstractions.message_bus import IMessageBus
from detecta_shared.rabbitmq.rabbitmq_event_listener import RabbitmqEventListener
from detecta_shared.rabbitmq.rabbitmq_params import RabbitMQSendParams
from detecta_shared.rabbitmq.rabbitmq_publisher import RabbitMQPublisher

class RabbitMQMessageBus(IMessageBus):
    def __init__(self, publisher: RabbitMQPublisher, listener: RabbitmqEventListener,
                 events_live_time: Dict[Type[TEvent], Optional[int]], logger: logging.Logger):
        self._logger = logger
        self._events_live_time = events_live_time
        self._listener = listener
        self._publisher = publisher

    # TODO на данный момент нужно сначала добавить события, потом уже стартовать слушателя. Иначе появятся ошибки
    # Причина это невозможность либы pika работать в многопоточной среде. Стоит либо лучше разобраться в многопоточности
    # Либо перейти на более низкоуровневые библиотеки
    # Также текущий подход заставляет создавать подключение как на слушателя, так и отправителя
    def subscribe(self, event_type: Type[TEvent], handler_type: Type[IntegrationEventHandler[TEvent]] = None):
        if not event_type.__bases__[0] == IntegrationEvent:
            raise ValueError(F"Added incorrect event type: {handler_type.__name__}")
        event_name = event_type.__name__
        self._listener.add_event(event_name)
        self._logger.info(f"Event {event_name} subscribed")

    def publish(self, event: IntegrationEvent):
        try:
            message_live_time = self._events_live_time.get(type(event), None)
            self._publisher.publish(event, RabbitMQSendParams(type(event).__name__, message_live_time))
        except Exception as ex:
            self._logger.error(f"Can't publish {type(event).__name__} event error: {ex}")
            raise
