from typing import List, Dict

from detecta_shared.abstractions.integration_events import IntegrationEventHandler


class HandlerFactory:
    def __init__(self, provider):
        self.provider = provider

    def create_event_handlers(self) -> List[IntegrationEventHandler]:
        return self.provider()


class SubscriptionManager:
    def __init__(self, handler_providers):
        self._event_handler_providers = handler_providers
        self._event_handler_factories: Dict[str, HandlerFactory] = dict()

    def has_event_handlers(self, event_name: str) -> bool:
        handlers_factory = self._event_handler_factories.get(event_name, None)
        return handlers_factory is not None

    def get_event_handlers_by_name(self, event_name: str) -> List[IntegrationEventHandler]:
        return self._event_handler_providers.get(event_name)()

    def add_subscription(self, event_name: str):
        provider = self._event_handler_providers.get(event_name)
        if not provider:
            raise ValueError(f"This provider does not exist. Event name: {event_name}")
        self._event_handler_factories[event_name] = HandlerFactory(provider)

    def remove_subscription(self, event_name: str):
        self._event_handler_factories.pop(event_name)

    def get_all_events(self) -> List:
        return self._event_handler_factories.keys()
