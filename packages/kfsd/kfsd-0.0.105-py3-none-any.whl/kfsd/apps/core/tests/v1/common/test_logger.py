from kfsd.apps.core.tests.base_api import BaseAPITestCases
from kfsd.apps.core.common.logger import Logger, LogLevel

import io


class LoggerTests(BaseAPITestCases):

    def test_logger_info(self):
        stream = io.StringIO()
        logger = Logger.getSingleton(__name__, LogLevel.INFO, stream)

        # info
        logger.info('This is a info message')
        stream_contents = stream.getvalue()
        self.assertIn('This is a info message', stream_contents)

        # warning
        logger.warn('This is a warning message')
        stream_contents = stream.getvalue()
        self.assertIn('This is a warning message', stream_contents)

        # error
        logger.error('This is a error message')
        stream_contents = stream.getvalue()
        self.assertIn('This is a error message', stream_contents)

        # critical
        logger.critical('This is a critical message')
        stream_contents = stream.getvalue()
        self.assertIn('This is a critical message', stream_contents)

        # debug
        logger.debug('This is a debug message')
        stream_contents = stream.getvalue()
        self.assertNotIn('This is a debug message', stream_contents)

    def test_logger_debug(self):
        stream = io.StringIO()
        logger = Logger.getSingleton(__name__, LogLevel.DEBUG, stream)

        logger.debug('This is a debug message')
        stream_contents = stream.getvalue()
        self.assertIn('This is a debug message', stream_contents)
