from elasticsearch import Elasticsearch

from detecta_shared.loggers.log_handlers.elasticsearch_handler import ElasticsearchHandler
from detecta_shared.loggers.log_handler_factories.log_handler_factory import LogHandlerFactory
from detecta_shared.loggers.log_handler_factories.log_handler_settings import LogHandlerSettings


class ELKLogHandlerFactory(LogHandlerFactory):

    def __init__(self, elastic_address: str, login: str, password: str,
                 settings: LogHandlerSettings, application_name: str):
        self.application_name = application_name
        self._password = password
        self._login = login
        self.elastic_address = elastic_address
        self.settings = settings

    def create_handler(self):
        es = Elasticsearch([self.elastic_address],
                           basic_auth=(self._login, self._password))
        handler = ElasticsearchHandler(es, self.application_name)
        handler.setFormatter(self.settings.formatter)
        handler.setLevel(self.settings.log_level)
        return handler

