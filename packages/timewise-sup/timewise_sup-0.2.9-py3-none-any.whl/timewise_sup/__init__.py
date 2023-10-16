import logging

__version__ = "0.2.9"

main_logger = logging.getLogger('timewise_sup')
logger_format = logging.Formatter('%(levelname)s:%(name)s:%(funcName)s - %(asctime)s: %(message)s', "%H:%M:%S")
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logger_format)
main_logger.addHandler(stream_handler)
main_logger.propagate = False  # do not propagate to root logger
