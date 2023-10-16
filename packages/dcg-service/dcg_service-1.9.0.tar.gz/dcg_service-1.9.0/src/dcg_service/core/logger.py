import json
import logging


def logging_override(name: str, extra=None):
    if extra is None:
        extra = {}
    c_logger = logging.getLogger(name)
    c_logger.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()

    stream_formatter = {
        "time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}
    stream_formatter = logging.Formatter(json.dumps(stream_formatter))
    stream_handler.setFormatter(stream_formatter)

    c_logger.addHandler(stream_handler)
    c_logger = logging.LoggerAdapter(c_logger, extra)
    return c_logger


logger = logging_override("json")
