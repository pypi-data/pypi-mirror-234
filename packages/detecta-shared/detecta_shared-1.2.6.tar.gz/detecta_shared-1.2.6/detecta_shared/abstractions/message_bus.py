import abc
from typing import Type

from detecta_shared.abstractions.integration_events import TEvent, IntegrationEventHandler, IntegrationEvent


class IMessageBus(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def subscribe(self, event_type: Type[TEvent], handler_type: Type[IntegrationEventHandler[TEvent]]):
        pass

    @abc.abstractmethod
    def publish(self, event: IntegrationEvent):
        pass
