import abc
from typing import Type, TypeVar, Generic


class IntegrationEvent:
    pass


TEvent = TypeVar("TEvent", bound=IntegrationEvent)


class IntegrationEventHandler(Generic[TEvent]):
    @abc.abstractmethod
    def handle(self, event: TEvent):
        pass

