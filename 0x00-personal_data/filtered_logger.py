#!/usr/bin/env python3
"""
logging module
"""

import logging
import re
from typing import List


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        formatting the data
        """
        msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields,  self.REDACTION,
                            message, self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    a func that returns the log message obfuscated
    """
    log_line = message
    for field in fields:
        log_line = re.sub(rf'{field}=([^{separator}]+){separator}',
                          f'{field}={redaction}{separator}', log_line)
    return log_line
