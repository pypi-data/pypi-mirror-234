import unittest
import logging
from rich.logging import RichHandler

#import pytest

from scoamp.utils.logger import get_logger, lib_name

class TestLogger(unittest.TestCase):
    def test_get_logger(self):
        # Test get default logger
        logger = get_logger()
        self.assertEqual(logger.name, lib_name)
    
        # Test default logger settings
        logger = get_logger(lib_name)
        self.assertEqual(logger.level, logging.INFO)
        self.assertEqual(len(logger.handlers), 1)
        handler = logger.handlers[0]
        self.assertIsInstance(handler, RichHandler)

        # Test any other logger
        name = 'other'
        logger = get_logger(name)
        self.assertEqual(logger.name, name)
        self.assertEqual(len(logger.handlers), 0)
        self.assertEqual(logger.level, logging.NOTSET)