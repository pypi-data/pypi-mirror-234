import copy
from logging import FileHandler, Formatter, LogRecord
from logging.handlers import TimedRotatingFileHandler, RotatingFileHandler
from typing import Callable


class EnhancedFileHandler(FileHandler):
    def __init__(
            self,
            filename,
            mode='a',
            encoding=None,
            delay=False,
            errors=None,
            level: int = 0,
            strict_level: bool = False,
            formatter: Formatter | None = None,
            msg_func: Callable[[str], str] | None = None):
        super().__init__(filename, mode, encoding, delay, errors)
        self.setFormatter(formatter)
        self.setLevel(level)
        self.strict_level = strict_level
        self.msg_func = msg_func

    def emit(self, record: LogRecord) -> None:
        if not isinstance(record.msg, str):
            try:
                record.msg = str(record.msg) or repr(record.msg)
            except Exception:
                raise Exception("Cannot convert object of type", type(record.msg), "to string")
        if not self.strict_level or record.levelno == self.level:
            modified_record = copy.deepcopy(record)
            if self.msg_func:
                modified_record.msg = self.msg_func(modified_record.msg)
            super().emit(modified_record)


class EnhancedTimedRotatingFileHandler(TimedRotatingFileHandler):
    def __init__(
            self,
            filename,
            when='h',
            interval=1,
            backupCount=0,
            encoding=None,
            delay=False,
            utc=False,
            atTime=None,
            errors=None,
            level: int = 0,
            strict_level: bool = False,
            formatter: Formatter | None = None,
            msg_func: Callable[[str], str] | None = None):
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc, atTime, errors)
        self.setFormatter(formatter)
        self.setLevel(level)
        self.strict_level = strict_level
        self.msg_func = msg_func

    def emit(self, record: LogRecord) -> None:
        if not self.strict_level or record.levelno == self.level:
            modified_record = copy.deepcopy(record)
            if self.msg_func:
                modified_record.msg = self.msg_func(modified_record.msg)
            super().emit(modified_record)


class EnhancedSizeRotatingFileHandler(RotatingFileHandler):
    def __init__(
            self,
            filename,
            mode='a',
            maxBytes=0,
            backupCount=0,
            encoding=None,
            delay=False,
            errors=None,
            level: int = 0,
            strict_level: bool = False,
            formatter: Formatter | None = None,
            msg_func: Callable[[str], str] | None = None):
        super().__init__(filename, mode, maxBytes, backupCount, encoding, delay, errors)
        self.setFormatter(formatter)
        self.setLevel(level)
        self.strict_level = strict_level
        self.msg_func = msg_func

    def emit(self, record: LogRecord) -> None:
        if not self.strict_level or record.levelno == self.level:
            modified_record = copy.deepcopy(record)
            if self.msg_func:
                modified_record.msg = self.msg_func(modified_record.msg)
            super().emit(modified_record)
