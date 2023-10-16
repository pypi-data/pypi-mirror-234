import logging

from detecta_shared.loggers.log_handler_factories.log_handler_factory import LogHandlerFactory
from detecta_shared.loggers.log_handler_factories.log_handler_settings import LogHandlerSettings


class ConsoleLogHandlerFactory(LogHandlerFactory):
    def __init__(self, settings: LogHandlerSettings):
        self.settings = settings

    def create_handler(self):
        formatter = self.settings.formatter
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.setLevel(self.settings.log_level)
        return handler
