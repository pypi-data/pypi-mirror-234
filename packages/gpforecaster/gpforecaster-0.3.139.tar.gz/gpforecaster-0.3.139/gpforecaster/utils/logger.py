import logging
import os
import time
from gpforecaster import __version__


class Logger:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        name = kwargs.get('name', None)
        if name not in cls._instances:
            instance = super(Logger, cls).__new__(cls)
            cls._instances[name] = instance
        return cls._instances[name]

    def __init__(self, name, dataset, to_file=None, log_level=logging.INFO, log_dir="."):
        timestamp = time.strftime("%Y%m%d-%H%M%S", time.gmtime())

        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        handler = logging.StreamHandler()  # Outputs the log to the console
        if to_file:
            log_dir_path = os.path.join(log_dir, "logs")
            if not os.path.exists(log_dir_path):
                os.makedirs(log_dir_path)

            log_file = os.path.join(log_dir_path, f"gpf_{__version__}_{dataset}_log_{timestamp}.txt")
            handler = logging.FileHandler(log_file)  # Outputs the log to a file
        handler.setFormatter(formatter)

        self.logger.addHandler(handler)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def close(self):
        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)
