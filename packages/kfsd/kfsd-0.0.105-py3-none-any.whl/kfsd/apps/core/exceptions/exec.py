from functools import wraps


class ExecException(Exception):
    def __init__(self, logger, msg):
        logger.exception(msg)


def ExecExceptionHandler(logger):
    def exception(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                raise ExecException(logger, e.__str__())
        return wrapper
    return exception
