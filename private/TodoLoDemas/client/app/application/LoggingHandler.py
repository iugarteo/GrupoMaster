import logging
import traceback
from datetime import datetime

from .publisher import publish_log


class LoggingHandler(logging.Handler):
    def __init__(self):
        super(LoggingHandler, self).__init__(level=logging.DEBUG)

    def emit(self, record):
        timestamp = datetime.fromtimestamp(record.created).strftime("%d-%b-%Y %H:%M:%S:%f")
        if record.levelname == 'CRITICAL':  # 50
            trace = traceback.format_exc()
            publish_log(timestamp, record.levelname, trace)
        elif record.levelname == 'ERROR':  # 40
            trace = traceback.format_exc()
            publish_log(timestamp, record.levelname, trace)
        elif record.levelname == 'WARNING':  # 30
            publish_log(timestamp, record.levelname, record.msg, record.filename, record.funcName)
        elif record.levelname == 'INFO':  # 20
            publish_log(timestamp, record.levelname, record.msg, record.filename, record.funcName)
        elif record.levelname == 'DEBUG':  # 10
            publish_log(timestamp, record.levelname, record.msg, record.filename, record.funcName)
