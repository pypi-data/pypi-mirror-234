import copy
from logging import StreamHandler, Formatter, LogRecord
from typing import Callable


class EnhancedStreamHandler(StreamHandler):
    def __init__(
            self,
            stream=None,
            level: int = 0,
            strict_level: bool = False,
            formatter: Formatter | None = None,
            msg_func: Callable[[str], str] | None = None):
        super().__init__(stream)
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
