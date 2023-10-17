import logging
from logging.handlers import RotatingFileHandler

from .json_formatter import JsonFormatter
from .stream import HTTPSINK, Consol, Stream
from .tracer import CustomStreamHandler


class Logging:
    def __init__(
        self,
        log_file_enabled: bool = True,
        log_console_enabled: bool = True,
        log_httpsink_enabled: bool = False,
        log_httpsink_url: str = None,
        log_level: str = 'INFO',
        log_buffer_size_file: int = 5 * 10**7,
        backupCount: int = 1,
        stream: list[Stream] = [],
        log_location: str = 'log.log',
        base_json_fields: dict = None,
        custon_json_fields: dict = None,
        log_structured_datetimeformat: str = '%Y-%m-%d %H:%M:%S',
    ):
        body_handlers = list()
        if log_file_enabled:
            body_handlers.append(
                RotatingFileHandler(log_location, maxBytes=log_buffer_size_file, backupCount=backupCount)
            )
        if log_console_enabled:
            stream.append(Consol())
        if log_httpsink_enabled and log_httpsink_url:
            stream.append(HTTPSINK(log_httpsink_url))
        body_handlers.append(CustomStreamHandler(stream))
        json_formatter = JsonFormatter(
            fmt_dict=base_json_fields, custom_dict=custon_json_fields, time_format=log_structured_datetimeformat
        )
        [i.setFormatter(json_formatter) for i in body_handlers]
        logging.basicConfig(
            level=log_level,
            handlers=body_handlers,
        )

    def get_logger(self):
        return logging
