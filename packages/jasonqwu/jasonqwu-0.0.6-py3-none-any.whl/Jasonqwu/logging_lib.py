import logging.config


class Logger:
    '''
    # 日志基本配置
    %(name)s                 Logger 的名字（getlogger 时指定的名字）
    %(levelno)s              数字形式的日志级别
    %(levelname)s            文本形式的日志级别
    %(pathname)s             调用日志输出日志的完整路径名
    %(filename)s             调用日志输出日志的文件名
    %(module)s               调用日志输出日志的模块名
    %(funcName)s             调用日志输出日志的函数名
    %(lineno)d               调用日志输出函数的语句所在的代码行
    %(created)f              当前时间，用 UNIX 标准的表示时间的浮点数表示
    %(relativeCreated)d      输出日志信息时的，自 Logger 创建以来的毫秒数
    %(asctime)s              字符串形式的当前时间，默认格式是“2022-07-30 22:15:53,394”
    %(thread)d               线程 ID，可能没有
    %(threadName)s           线程名，可能没有
    %(process)d              进程 ID，可能没有
    %(message)s              用户输出的消息
    '''
    LOGGING_DIC = {
        "version": 1.0,
        "disable_existing_loggers": False,

        # 日志格式
        "formatters": {
            "debug": {
                "fmt": None,
                "format": "[%(filename)15s line:%(lineno)5d] %(message)s",
                "datefmt": "%Y年%m月%d日 %H:%M:%S %p",
            },
            "warning": {
                "format":
                    "[%(filename)15s line:%(lineno)5d] - " +
                    "%(asctime)s %(name)s  %(levelname)-8s: %(message)s",
                "datefmt": "%Y年%m月%d日 %H:%M:%S %p",
            },
        },

        # 日志过滤器
        "filters": {},

        # 日志处理器
        "handlers": {
            "console_debug_handler": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                # "class": "logging.FileHandler",
                # "class": "logging.BaseRotatingHandler",
                # "class": "logging.RotatingHandler",
                # "class": "logging.TimedRotatingHandler",
                # "class": "logging.SocketHandler",
                # "class": "logging.DatagramHandler",
                # "class": "logging.SMTPHandler",
                # "class": "logging.SysLogHandler",
                # "class": "logging.NTEventLogHandler",
                # "class": "logging.HTTPHandler",
                # "class": "logging.WatchedFileHandler",
                # "class": "logging.QueueHandler",
                # "class": "logging.NullHandler",
                "formatter": "debug",
            },
            "console_warning_handler": {
                "level": "WARNING",
                "class": "logging.StreamHandler",
                "formatter": "warning",
            },
            "file_debug_handler": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "filename": "access.log",
                "mode": "w",
                "encoding": "utf-8",
                "delay": "False",
                "formatter": "debug",
            },
            "file_warning_handler": {
                "level": "WARNING",
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "access.log",
                "mode": "a",
                "maxBytes": 1024 * 1024 * 10,
                "backupCount": 10,
                "encoding": "utf-8",
                "formatter": "warning",
            },
        },

        # 日志记录器
        "loggers": {
            "show": {
                "handlers": ["console_debug_handler"],
                "level": "DEBUG",
                "propagate": False,
            },
            "file": {
                "handlers": ["file_debug_handler"],
                "level": "DEBUG",
                "propagate": False,
            },
        },
    }

    def __init__(self, logger="show"):
        logging.config.dictConfig(self.LOGGING_DIC)
        self._logger = logging.getLogger(logger)

    def get_level(self, level):
        if level == "debug":
            return self._logger.debug
        elif level == "info":
            return self._logger.info
        elif level == "warning":
            return self._logger.warning
        elif level == "error":
            return self._logger.error
        elif level == "critical":
            return self._logger.critical
        else:
            return lambda ign: ign


if __name__ == '__main__':
    # log = Logger("log00")
    # 10 详细信息，常用于调试。
    debug = Logger("show").get_level("debug")
    debug(f"调试信息")
    # 20 程序正常运行过程中产生的一些信息。
    info = Logger("show").get_level("info")
    info(f"正常信息")
    # 30 警告用户，虽然程序还在正常工作，但有可能发生错误。
    warning = Logger("show").get_level("warning")
    warning(f"警告信息")
    # 40 由于更严重的问题，程序已不能执行一些功能了。
    error = Logger("show").get_level("error")
    error(f"报错信息")
    # 50 严重错误，程序已不能继续运行。
    critical = Logger("show").get_level("critical")
    critical(f"崩溃信息")
