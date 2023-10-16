import setuptools

setuptools.setup(
    name='detecta_shared',
    version='1.2.5',
    description='Shared libs for detecta.',
    author='TaKi',
    install_requires=['numpy', 'pika', 'jsonpickle', 'elasticsearch'],
    python_requires='>=3.9',
    packages=['detecta_shared.rabbitmq', 'detecta_shared.abstractions', 'detecta_shared.loggers',
              'detecta_shared.loggers.log_handler_factories', 'detecta_shared.loggers.log_handlers']
)