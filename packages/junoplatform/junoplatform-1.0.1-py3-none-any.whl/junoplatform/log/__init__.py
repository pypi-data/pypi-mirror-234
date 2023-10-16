import logging
from junoplatform.io import Storage
from junoplatform.io.utils import junoconfig

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(filename)s %(lineno)d - %(message)s')


class RTLogHandler(logging.Handler):
    def __init__(self):
        super(RTLogHandler, self).__init__()
        self.io = Storage().cloud

    def emit(self, record):
        log_entry = {
            'level': record.levelname,
            'message': record.getMessage(),
            'et': record.created,
            'logger_name': record.name,
            'file': record.filename,
            'line_number': record.lineno,
            'function_name': record.funcName
        }

        self.io.write('rtlog', log_entry)


# try:
#     logger = logging.getLogger('rtlog')
#     logger.addHandler(RTLogHandler())
#     logger.setLevel(logging.INFO)
# except:
#     pass

logger = logging
