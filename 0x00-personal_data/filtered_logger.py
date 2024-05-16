#!/usr/bin/env python3

"""
filtered_logger module

This module provides a function to obfuscate sensitive
information in log messages.
"""

import re
from typing import List


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """
    Obfuscate sensitive information in a log message.

    Args:
        fields: A list of strings representing all fields to obfuscate.
        redaction: A string representing by what the field will be obfuscated.
        message: A string representing the log line.
        separator: A string representing by which character is separating all
            fields in the log line.

    Returns:
        The log message with sensitive information obfuscated.
    """
    return re.sub(r'(?<={}=).*?(?={})'.format('|'.join(fields), separator),
                  redaction, message)
