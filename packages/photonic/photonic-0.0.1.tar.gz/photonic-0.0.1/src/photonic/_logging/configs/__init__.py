from logging import getLogger, DEBUG, WARNING, Formatter, Handler


def console_config(
        logger_name: str, fmt: str = Format.brief_format.value, level=WARNING, propagate: bool = False, colors: bool = True
) -> None:
    formatter = ColorFormatter if colors else Formatter
    _formatter = formatter(fmt=fmt, datefmt=Format.date_format.value)

    console_handler = ConsoleHandler(level, _formatter)

    setup_logger(logger_name, level, console_handler, propagate)


def json_file_config(logger_name: str, fmt: str = Format.detailed_json_format.value, level=DEBUG, propagate: bool = False) -> None:
    file_handler = JsonFileHandler(log_file_path, level, Formatter(fmt=fmt, datefmt=Format.date_format.value))

    setup_logger(logger_name, level, file_handler, propagate)


def setup_logger(name: str, level, handler: Handler, propagate: bool) -> None:
    logger = getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = propagate
