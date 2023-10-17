from __future__ import absolute_import


import logging
import collections
import sys
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Dict

try:
    import colorama
except ImportError:
    pass
else:
    colorama.init()

__all__ = ("escape_codes", "parse_colors")


__all__ = [
    "escape_codes",
    "parse_colors",
    "root",
    "getLogger",
    "debug",
    "info",
    "warning",
    "error",
    "critical",
    "log",
    "exception",
    "vxLoggerFactory",
]


# Returns escape codes from format codes
def esc(*x):
    return "\033[" + ";".join(x) + "m"


# The initial list of escape codes
escape_codes = {
    "reset": esc("0"),
    "bold": esc("01"),
}

# The color names
COLORS = ["black", "red", "green", "yellow", "blue", "purple", "cyan", "white"]

PREFIXES = [
    # Foreground without prefix
    ("3", ""),
    ("01;3", "bold_"),
    # Foreground with fg_ prefix
    ("3", "fg_"),
    ("01;3", "fg_bold_"),
    # Background with bg_ prefix - bold/light works differently
    ("4", "bg_"),
    ("10", "bg_bold_"),
]

for prefix, prefix_name in PREFIXES:
    for code, name in enumerate(COLORS):
        escape_codes[prefix_name + name] = esc(prefix + str(code))


def parse_colors(sequence: str):
    """Return escape codes from a color sequence."""
    return "".join(escape_codes[n] for n in sequence.split(",") if n)


# The default colors to use for the debug levels
default_log_colors = {
    "DEBUG": "white",
    "INFO": "green",
    "WARNING": "yellow",
    "ERROR": "red",
    "CRITICAL": "bold_red",
}

# The default format to use for each style
default_formats = {
    "%": "%(log_color)s%(levelname)s:%(name)s:%(message)s",
    "{": "{log_color}{levelname}:{name}:{message}",
    "$": "${log_color}${levelname}:${name}:${message}",
}


class ColoredRecord:
    """
    Wraps a LogRecord and attempts to parse missing keys as escape codes.

    When the record is formatted, the logging library uses ``record.__dict__``
    directly - so this class replaced the dict with a ``defaultdict`` that
    checks if a missing key is an escape code.
    """

    class __dict(collections.defaultdict):
        def __missing__(self, key):
            try:
                return parse_colors(key)
            except Exception as err:
                raise KeyError(
                    f"{key} is not a valid record attribute or color sequence"
                ) from err

    def __init__(self, record):
        self.__dict__ = self.__dict()
        self.__dict__.update(record.__dict__)
        self.__record = record

    def __getattr__(self, name):
        return getattr(self.__record, name)


class ColoredFormatter(logging.Formatter):
    """
    A formatter that allows colors to be placed in the format string.

    Intended to help in creating more readable logging output.
    """

    def __init__(
        self,
        fmt: str = None,
        datefmt: str = None,
        style: str = "%",
        log_colors: Dict = None,
        reset: bool = True,
        secondary_log_colors: Dict = None,
    ):
        """
        Set the format and colors the ColoredFormatter will use.

        The ``fmt``, ``datefmt`` and ``style`` args are passed on to the
        ``logging.Formatter`` constructor.

        The ``secondary_log_colors`` argument can be used to create additional
        ``log_color`` attributes. Each key in the dictionary will set
        ``{key}_log_color``, using the value to select from a different
        ``log_colors`` set.

        :Parameters:
        - fmt (str): The format string to use
        - datefmt (str): A format string for the date
        - log_colors (dict):
            A mapping of log level names to color names
        - reset (bool):
            Implictly append a color reset to all records unless False
        - style ('%' or '{' or '$'):
            The format style to use. (*No meaning prior to Python 3.2.*)
        - secondary_log_colors (dict):
            Map secondary ``log_color`` attributes. (*New in version 2.6.*)
        """
        if fmt is None:
            if sys.version_info > (3, 2):
                fmt = default_formats[style]
            else:
                fmt = default_formats["%"]

        if sys.version_info > (3, 2):
            super(ColoredFormatter, self).__init__(fmt, datefmt, style)
        elif sys.version_info > (2, 7):
            super(ColoredFormatter, self).__init__(fmt, datefmt)
        else:
            logging.Formatter.__init__(self, fmt, datefmt)

        self.log_colors = log_colors if log_colors is not None else default_log_colors
        self.secondary_log_colors = secondary_log_colors
        self.reset = reset

    def color(self, log_colors: Dict, name: str):
        """Return escape codes from a ``log_colors`` dict."""
        return parse_colors(log_colors.get(name, ""))

    def format(self, record: logging.LogRecord):
        """Format a message from a record object."""
        record = ColoredRecord(record)
        record.log_color = self.color(self.log_colors, record.levelname)

        # Set secondary log colors
        if self.secondary_log_colors:
            for name, log_colors in self.secondary_log_colors.items():
                color = self.color(log_colors, record.levelname)
                setattr(record, f"{name}_log_color", color)

        # Format the message
        if sys.version_info > (2, 7):
            message = super(ColoredFormatter, self).format(record)
        else:
            message = logging.Formatter.format(self, record)

        # Add a reset code to the end of the message
        # (if it wasn't explicitly added in format str)
        if self.reset and not message.endswith(escape_codes["reset"]):
            message += escape_codes["reset"]

        return message


class LevelFormatter(ColoredFormatter):
    """An extension of ColoredFormatter that uses per-level format strings."""

    def __init__(
        self,
        fmt: str = None,
        datefmt: str = None,
        style: str = "%",
        log_colors: Dict = None,
        reset: bool = True,
        secondary_log_colors: Dict = None,
    ):
        """
        Set the per-loglevel format that will be used.

        Supports fmt as a dict. All other args are passed on to the
        ``colorlog.ColoredFormatter`` constructor.

        :Parameters:
        - fmt (dict):
            A mapping of log levels (represented as strings, e.g. 'WARNING') to
            different formatters. (*New in version 2.7.0)
        (All other parameters are the same as in colorlog.ColoredFormatter)

        Example:

        formatter = colorlog.LevelFormatter(fmt={
            'DEBUG':'%(log_color)s%(msg)s (%(module)s:%(lineno)d)',
            'INFO': '%(log_color)s%(msg)s',
            'WARNING': '%(log_color)sWARN: %(msg)s (%(module)s:%(lineno)d)',
            'ERROR': '%(log_color)sERROR: %(msg)s (%(module)s:%(lineno)d)',
            'CRITICAL': '%(log_color)sCRIT: %(msg)s (%(module)s:%(lineno)d)',
        })
        """
        if sys.version_info > (2, 7):
            super(LevelFormatter, self).__init__(
                fmt=fmt,
                datefmt=datefmt,
                style=style,
                log_colors=log_colors,
                reset=reset,
                secondary_log_colors=secondary_log_colors,
            )
        else:
            ColoredFormatter.__init__(
                self,
                fmt=fmt,
                datefmt=datefmt,
                style=style,
                log_colors=log_colors,
                reset=reset,
                secondary_log_colors=secondary_log_colors,
            )
        self.style = style
        self.fmt = fmt

    def format(self, record: logging.LogRecord):
        """Customize the message format based on the log level."""
        if isinstance(self.fmt, dict):
            self._fmt = self.fmt[record.levelname]
            if sys.version_info > (3, 2):
                # Update self._style because we've changed self._fmt
                # (code based on stdlib's logging.Formatter.__init__())
                if self.style not in logging._STYLES:
                    raise ValueError(
                        f'Style must be one of: {",".join(logging._STYLES.keys())}'
                    )
                self._style = logging._STYLES[self.style][0](self._fmt)

        return (
            super(LevelFormatter, self).format(record)
            if sys.version_info > (2, 7)
            else ColoredFormatter.format(self, record)
        )


__COLOR_BASIC_FORMAT__ = (
    "%(asctime)s [%(process)s:%(threadName)s - %(funcName)s@%(filename)s:%(lineno)d]"
    " %(log_color)s%(levelname)s%(reset)s: %(message)s"
)

__BASIC_FORMAT__ = (
    "%(asctime)s [%(process)s:%(threadName)s - %(funcName)s@%(filename)s:%(lineno)d]"
    " %(levelname)s: %(message)s"
)


class vxLoggerFactory:
    """日志工厂类，用于创建日志类"""

    def __init__(
        self,
        root: str = "vxroot",
        level: int = logging.INFO,
        log_dir: str = None,
        log_file: str = None,
    ):
        """
        :param root: 基础logger的名称，默认为: vxlogger
        :params level: log的级别，默认为INFO
        :param log_dir: log文件的存放目录，默认为当前目录
        :param log_file: 日志文件名称
        """
        self._root = root
        self._root_level = level
        self._log_dir = Path(log_dir or "./")

        if len(logging.root.handlers) == 0:
            self._add_console()

        if log_file:
            self._add_filehandler(
                logging.getLogger(self._root),
                filename=log_file,
                level=self._root_level,
                encoding="utf8",
            )

    def _add_console(self):
        logging.basicConfig(
            force=True,
            level=self._root_level,
        )

        try:
            logging._acquireLock()
            for handler in logging.root.handlers:
                if isinstance(handler, logging.StreamHandler):
                    handler.setFormatter(ColoredFormatter(fmt=__COLOR_BASIC_FORMAT__))
        finally:
            logging._releaseLock()

    def _add_filehandler(self, logger, filename, level=logging.INFO, encoding="utf8"):
        """添加日志文件

        Arguments:
            logger {日志类} -- 日志类
            filename {str} -- 文件名称
            level {int} -- 日志登记 (default: {None})
            encoding {str} -- 文件编码 (default: {"utf8"})

        """
        if not filename:
            raise ValueError("未指定log文件名")

        level = level or logging.INFO
        self._log_dir.mkdir(parents=True, exist_ok=True)
        filename = self._log_dir.joinpath(filename).as_posix()

        try:
            logging._acquireLock()
            filehandler = TimedRotatingFileHandler(
                filename, when="D", backupCount=20, encoding=encoding
            )
            filehandler.setFormatter(logging.Formatter(__BASIC_FORMAT__))
            filehandler.setLevel(level)
            filehandler.createLock()
            logger.addHandler(filehandler)
            logging.debug("添加日志文件: %s", filehandler)
        finally:
            logging._releaseLock()

    def getLogger(self, logger_name="", level=logging.INFO, filename=""):
        """获取一个logger的实例

        Keyword Arguments:
            logger_name -- _description_ (default: {""})
            level -- _description_ (default: {logging.INFO})
            filename -- _description_ (default: {""})

        Returns:
            _description_
        """
        if logger_name == self._root or not logger_name:
            return logging.getLogger(self._root)

        logger_name = f"{self._root}.{logger_name}"
        child_logger = logging.getLogger(logger_name)
        child_logger.setLevel(level)
        if len(child_logger.handlers) == 0 and filename and self._log_dir:
            self._add_filehandler(child_logger, filename, level)
        return child_logger


vxLogging = vxLoggerFactory(
    root="vxroot", level=logging.INFO, log_dir="log/", log_file="message.log"
)
root = vxLogging.getLogger()
getLogger = vxLogging.getLogger
debug = root.debug
info = root.info
warning = root.warning
error = root.error
critical = root.critical
log = root.log
exception = root.exception
