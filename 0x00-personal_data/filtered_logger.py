#!/usr/bin/env python3
"""
logging module
"""

import logging
import re


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
