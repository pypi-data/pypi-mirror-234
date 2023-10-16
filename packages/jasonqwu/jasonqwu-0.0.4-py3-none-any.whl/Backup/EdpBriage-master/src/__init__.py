

__version__ = '0.1.0'


from logging import getLogger, StreamHandler, Formatter, DEBUG

DEBUG_LOG_FORMAT = (
    '-' * 80 + '\n' +
    '%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n' +
    '%(message)s\n' +
    '-' * 80
)

logger = getLogger('EdpBriage')
logger.setLevel(DEBUG)

ch = StreamHandler()
ch.setLevel(DEBUG)

# 创建格式器，加到日志处理器中
ch.setFormatter(Formatter(DEBUG_LOG_FORMAT))

logger.addHandler(ch)