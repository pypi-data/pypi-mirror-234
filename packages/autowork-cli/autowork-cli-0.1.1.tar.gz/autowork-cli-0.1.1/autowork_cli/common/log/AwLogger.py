import logging
import os.path
from collections import UserDict
from enum import Enum
from pathlib import Path

from autowork_cli.common.config.ClientConfig import LOG_FILE
from autowork_cli.common.config.LoginConfig import DefaultLoginConfig
from autowork_cli.repository.cybotron.service.log_accessor import LogAccessor


class LogModule(Enum):
    LOGIN = 'login'
    CF = 'cloud-function'
    FILE = 'file'
    FLOW = 'flow'


class LogLevel(Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class Log(UserDict):
    module: str
    level: str
    message: str


class AwLogger:
    """autowork log warapper"""
    def __init__(self, module: str, logger: logging.Logger):
        self.module = module
        self.logger = logger

    @classmethod
    def getLogger(cls, module: LogModule, filename: str, level: LogLevel = LogLevel.INFO):
        logger = logging.getLogger(filename)
        if level is None:
            logger.setLevel('INFO')
        else:
            logger.setLevel(level.value)

        logfile = Path().home().joinpath(LOG_FILE)
        logdir = logfile.parent
        if not logdir.exists():
            logdir.mkdir(parents=True, exist_ok=True)

        handler = logging.FileHandler(logfile)
        formatter = logging.Formatter(
            fmt="%(asctime)s.%(msecs)03d [%(levelname)s] %(filename)s:%(lineno)s - %(message)s"
            , datefmt='%Y-%m-%d %H:%M:%S')

        handler.setFormatter(formatter)

        logger.addHandler(handler)
        # 如果是debug模式，信息入库autowork.aw_operate_log
        if DefaultLoginConfig.get_debug():
            logger.addHandler(DBLogHandler(module))

        return cls(module.value, logger)

    def critical(self, msg: str):
        self.logger.critical(self.get_log_msg(msg))

    def error(self, msg: str):
        self.logger.error(self.get_log_msg(msg))

    def warn(self, msg: str):
        self.logger.warning(self.get_log_msg(msg))

    def info(self, msg: str):
        self.logger.info(self.get_log_msg(msg))

    def debug(self, msg: str):
        self.logger.debug(self.get_log_msg(msg))

    def get_log_msg(self, msg: str) -> str:
        return f"[{self.module}] {msg}"


class DBLogHandler(logging.Handler):
    def __init__(self, module):
        super().__init__()
        self.module = module
        formatter = logging.Formatter(
            fmt="%(asctime)s.%(msecs)03d [%(levelname)s] %(filename)s:%(lineno)s - %(message)s"
            , datefmt='%Y-%m-%d %H:%M:%S')
        self.setFormatter(formatter)

    def emit(self, record: logging.LogRecord):
        log = Log(
            module=self.module.value,
            level=record.levelno,
            message=record.getMessage(),
        )
        try:
            LogAccessor.send_log(log.data)
        except Exception as e:
            print(e)
