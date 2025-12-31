import json, logging
from logging import Logger

from config import BASE_DIR


class LoggingConfig:
    path = BASE_DIR.joinpath("logger", "config.json")
    logger_name = "payments"

    @property
    def logger(self) -> Logger:
        return logging.getLogger(self.logger_name)

    def load(self) -> None:
        with open(self.path) as json_config:
            config_file = json.load(json_config)
        return config_file
