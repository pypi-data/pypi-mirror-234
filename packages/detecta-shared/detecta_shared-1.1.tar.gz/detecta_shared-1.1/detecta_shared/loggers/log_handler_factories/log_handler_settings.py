import logging


class LogHandlerSettings:
    def __init__(self, formatter: logging.Formatter, log_level: int):
        self.log_level = log_level
        self.formatter = formatter
