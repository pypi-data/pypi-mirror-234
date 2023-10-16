import logging


class AlertHandler(logging.Handler):
    # тут надо добавить ссылку или какие-то параметры для отправки алерта куда надо
    def __init__(self):
        super().__init__()
        pass

    def emit(self, record):
        pass