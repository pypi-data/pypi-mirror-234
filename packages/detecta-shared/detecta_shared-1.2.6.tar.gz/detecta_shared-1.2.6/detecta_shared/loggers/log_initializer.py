import logging
from typing import List

from detecta_shared.loggers.log_handler_factories.console_log_factory import ConsoleLogHandlerFactory
from detecta_shared.loggers.log_handler_factories.elk_log_factory import ELKLogHandlerFactory
from detecta_shared.loggers.log_handler_factories.file_log_factory import FileLogHandlerFactory
from detecta_shared.loggers.log_handler_factories.log_handler_factory import LogHandlerFactory
from detecta_shared.loggers.log_handler_factories.log_handler_settings import LogHandlerSettings


class LogInitializer:
    def __init__(self, logger_name: str, log_level: int, log_handler_factories: List[LogHandlerFactory]):
        self.log_handler_factories = log_handler_factories
        self.log_level = log_level
        self.logger_name = logger_name

    def init_logger(self):
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.log_level)
        for handler_factory in self.log_handler_factories:
            logger.addHandler(handler_factory.create_handler())


class LogInitializerByConfig:
    log_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }

    def __init__(self, logger_name: str, log_config):
        self.logger_name = logger_name
        self.log_config = log_config

    def init_logger(self):
        usings: list = [logger_name.strip().lower() for logger_name in self.log_config['usings'].split(',')]
        handler_factories = list()

        app_name = self.log_config['application_name']
        for handler in self.log_config['handlers']:
            handler_name: str = handler['name'].lower()
            if not (handler_name in usings):
                continue
            self._append_handler(app_name, handler, handler_factories, handler_name)

        default_level = self.log_levels.get(self.log_config['global_level'].upper(), 10)
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(default_level)
        for log_factory in handler_factories:
            logger.addHandler(log_factory.create_handler())

    def _append_handler(self, app_name, handler, handler_factories, handler_name):
        settings = LogHandlerSettings(logging.Formatter(handler['formatter']),
                                      self.log_levels.get(handler['level'].upper(), 10))
        # TODO лучше вынести это в более сложную логику, например подхватывать из метаданных
        if handler_name == 'console':
            handler_factories.append(ConsoleLogHandlerFactory(settings))

        elif handler_name == 'elk':
            handler_factories.append(ELKLogHandlerFactory(handler['elastic_address'], handler['login'],
                                                          handler['password'], settings, app_name))
        elif handler_name == 'file':
            handler_factories.append(FileLogHandlerFactory(handler['directory'], app_name, settings))
