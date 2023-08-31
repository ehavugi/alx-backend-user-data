#!/usr/bin/env python3
"""
Filter module part of personal data
module
"""
from typing import List
import re
import logging
import time
import datetime

conv = datetime.datetime.fromtimestamp


def filter_datum(fields: List[str], redaction: str,
                 message: str, seperator: str) -> str:
    """return a redacted test without values for fields
    """
    for field in fields:
        replacement = "{}={}{}".format(field, redaction, seperator)
        message = re.sub(r'{}=[^{}]+{}'.format(field, seperator, seperator),
                         replacement, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields) -> None:
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format a record record by redacting the fields and reformating the
        the log
        """
        r = record
        redactedmsg = filter_datum(self.fields, self.REDACTION,
                                   str(record.msg), self.SEPARATOR)
        ascii_time = conv(record.created).strftime('%Y-%m-%d %H:%M:%S')
        return str(self.FORMAT % {"name": r.name, "levelname": r.name,
                   "asctime": ascii_time, "message": redactedmsg})
