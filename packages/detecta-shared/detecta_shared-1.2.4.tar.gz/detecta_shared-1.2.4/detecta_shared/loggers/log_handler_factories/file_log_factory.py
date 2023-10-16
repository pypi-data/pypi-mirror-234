import os

from detecta_shared.loggers.log_handlers.timed_file_handler import TimedPatternFileHandler
from detecta_shared.loggers.log_handler_factories.log_handler_factory import LogHandlerFactory
from detecta_shared.loggers.log_handler_factories.log_handler_settings import LogHandlerSettings


class FileLogHandlerFactory(LogHandlerFactory):
    def __init__(self, directory: str, file_name: str, settings: LogHandlerSettings):
        self.file_name = file_name
        self.settings = settings
        self.directory = directory

    def create_handler(self):
        directory = self.__create_logger_directory(self.directory)
        file_name_pattern = os.path.join(directory, self.file_name) + "-%d-%m-%Y.log"
        file_handler = TimedPatternFileHandler(file_name_pattern, when="MIDNIGHT", backupCount=13)
        file_handler.setFormatter(self.settings.formatter)
        file_handler.setLevel(self.settings.log_level)
        return file_handler


    @staticmethod
    def __create_logger_directory(logger_directory=None):
        if not logger_directory:
            logger_directory = os.path.join(os.getcwd(), "Logs")
        if not os.path.exists(logger_directory):
            os.makedirs(logger_directory)
        return logger_directory
