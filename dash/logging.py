
from logging import *

class ColorFormatter(Formatter):
    GREY = "\x1b[38;20m"
    YELLOW = "\x1b[33;20m"
    RED = "\x1b[31;20m"
    BOLD_RED = "\x1b[31;1m"
    CYAN = "\x1b[96m"
    RESET = "\x1b[0m"

    FORMAT_PREFIX = '[%(asctime)s] - <%(name)s> '
    FORMAT = '%(levelname)s: %(message)s'

    FORMATS = {
        NOTSET:   GREY + FORMAT_PREFIX            + FORMAT + RESET,
        DEBUG:    GREY + FORMAT_PREFIX            + FORMAT + RESET,
        INFO:     GREY + FORMAT_PREFIX + CYAN     + FORMAT + RESET,
        WARNING:  GREY + FORMAT_PREFIX + YELLOW   + FORMAT + RESET,
        ERROR:    GREY + FORMAT_PREFIX + RED      + FORMAT + RESET,
        CRITICAL: GREY + FORMAT_PREFIX + BOLD_RED + FORMAT + RESET,
    }

    def format(self, record: LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        return Formatter(log_fmt).format(record)

Console = StreamHandler()
Console.setFormatter(ColorFormatter())
