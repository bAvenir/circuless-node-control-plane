import sys
import logging


class MyLogger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        stream_handler = logging.StreamHandler(sys.stderr)
        formatter = logging.Formatter(
            fmt='%(asctime)s - %(levelname)s - {%(module)s:%(lineno)d} - %(message)s'
        )
        stream_handler.setFormatter(formatter)

        stream_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(stream_handler)
        # self.logger.propagate = False

    def info(self, message):
        self.logger.info("{}".format(message))
    
    def warn(self, message):
        self.logger.warn("{}".format(message))
    
    def error(self, message):
        self.logger.error("{}".format(message))
    
    def debug(self, message):
        self.logger.debug("{}".format(message))