import abc
import logging


class LogHandlerFactory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def create_handler(self) -> logging.Handler:
        pass
