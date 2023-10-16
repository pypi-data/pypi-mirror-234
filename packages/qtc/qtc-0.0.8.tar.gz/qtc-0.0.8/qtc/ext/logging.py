import sys
import logging
from qtc.ext.inspect import inspect_caller


# DEFAULT_FORMAT = '[%(levelname).1s %(asctime)s %(module)s:%(funcName)s] - %(message)s'
DEFAULT_FORMAT = '[%(levelname).1s %(asctime)s %(filename)s:%(lineno)d] - %(message)s'


def set_logger(name: str = None,
               format: str = DEFAULT_FORMAT,
               logfile: str = None):
    """Create an easy logging interface. By default it prints logging messages to stderr (not stdout).

    :param name: Logging name with period-separated hierarchy. Default: module.__name__ .
    :param format: Logging format str.
    :param logfile: If provided, logging will be directed to it.
    :return: None

    >>> from qtc.ext.logging import set_logger
    >>> import os
    >>> logger = set_logger(logfile=os.path.join(os.environ['HOME'], 'logs', 'test_logger.log'))
    >>> logger.debug('This helps debugging')
    >>> logger.info('This is running')
    >>> logger.warning('This is a warning')
    >>> logger.error('This is an error')
    >>> logger.critical('This is a critical situation')

    .. note::
        To suppress logging messages at certain level, do something like:
        logging.getLogger('module.full.hierarchy').setLevel(logging.CRITICAL)
    """

    formatter = logging.Formatter(fmt=format)

    stream_handler = logging.StreamHandler(stream=sys.stderr)
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(name or inspect_caller(skip=2, return_info=['MODULE'])['MODULE'])
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        logger.addHandler(stream_handler)

    # File logging
    if logfile:
        file_handler = logging.FileHandler(logfile, mode='a')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


if __name__ == '__main__':
    logger = set_logger()
    logger.info('This is a test')
    print(logging.getLogger('__main__'))

    import os
    logger = set_logger(logfile=os.path.join(os.environ['HOME'], 'logs', 'test_logger.log'))
    logger.info('This is running')