import logging
import traceback
from pathlib import Path

LOG_FILENAME = 'dicomselect.log'


class Logger:
    CRITICAL = 50
    FATAL = CRITICAL
    ERROR = 40
    WARNING = 30
    WARN = WARNING
    INFO = 20
    DEBUG = 10
    NOTSET = 0

    def __init__(self):
        self._log: logging.Logger = None
        self._log_path: Path = None
        self._errors: int = 0
        self._error = set()

    @property
    def errors(self) -> int:
        return self._errors

    @property
    def path_log(self) -> Path:
        return self._log_path

    def init_logger(self, file: Path):
        self._errors = 0
        self._log = logging.getLogger(file.name)
        self._log.setLevel(logging.WARN)
        [self._log.removeHandler(h) for h in self._log.handlers]
        self._log_path = file
        self._log_path.parent.mkdir(parents=True, exist_ok=True)

        formatter = logging.Formatter('--- %(levelname)s ---\n%(message)s')
        handler = logging.FileHandler(file.as_posix())
        handler.setFormatter(formatter)
        self._log.addHandler(handler)

    def log(self, exc: Exception | str, level: int = logging.ERROR, **kwargs):
        if self._errors == 0:
            with open(self.path_log, 'w'):
                pass

        self._errors += 1

        if kwargs:
            name = kwargs.pop('name', '')
            text = [f'\nError during {name}:'] if name else []
            for key, val in kwargs.items():
                text.append(f'\t{key}:\n\t\t{str(val)}\n')
            text.append('\t' + '\t'.join(traceback.format_exception(exc)))
            exc = '\n'.join(text)

        if isinstance(exc, Exception):
            self._log.log(level, traceback.format_exception(exc))
        else:
            self._log.log(level, str(exc))
