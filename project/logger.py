# mypy: disable-error-code=union-attr
import logging.handlers
from abc import ABC, abstractmethod
from logging.handlers import RotatingFileHandler


class AbstractLogger(ABC):
    Logger: logging.Logger | None = None

    @abstractmethod
    def __getattr__(self, name: str):
        return lambda *args, **kwargs: None


class DummyLogger(AbstractLogger):
    def __init__(self):
        self.Logger = logging.getLogger(__name__)
        self.Logger.addHandler(logging.NullHandler())
        self.Logger.propagate = False

    def __getattr__(self, name: str):
        super().__getattr__(name)


class Logger(AbstractLogger):
    def __init__(self, logging_service: str):
        self.Logger = logging.getLogger(logging_service)
        self.Logger.setLevel(logging.DEBUG)
        self.Logger.propagate = False

        # Initialize formatter
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # Initialize file handler
        fh = RotatingFileHandler(f"logs/{logging_service}.log", maxBytes=1000000, backupCount=5)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        self.Logger.addHandler(fh)

        # Initialize console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        self.Logger.addHandler(ch)

    def __getattr__(self, name: str):
        return self.Logger.__getattribute__(name)

    def critical(self, msg: str):
        print(flush=True)
        self.Logger.critical(msg)
