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
import os
import mysql
import mysql.connector.connection as connectori

conv = datetime.datetime.fromtimestamp
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'ip')


def filter_datum(fields: List[str], reda: str, msg: str, sep: str) -> str:
    """return a redacted test without values for fields."""
    for field in fields:
        rep = "{}={}{}".format(field, reda, sep)
        msg = re.sub(r'{}=[^{}]+{}'.format(field, sep, sep), rep, msg)
    return msg


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class.
    Class initializer
    format function
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> None:
        """Initialization of redactionFormatter.
        with fields
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """format a record record by redacting the fields and reformating"""
        r, f = record, filter_datum
        rm = f(self.fields, self.REDACTION, str(record.msg), self.SEPARATOR)
        ascii_time = conv(r.created).strftime('%Y-%m-%d %H:%M:%S,%f3')
        return str(self.FORMAT % {"name": r.name, "levelname": r.levelname,
                   "asctime": ascii_time, "message": rm})


def get_logger() -> logging.Logger:
    """get logger function rerurns logging.Logger
    with redactingformatter class initialized with PII_fields
    """
    logger = logging.Logger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(RedactingFormatter(list(PII_FIELDS)))
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    user = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', "")
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db = os.environ.get('PERSONAL_DATA_DB_NAME')

    conn = connectori.MySQLConnection(user=user, database=db,
                                      host=host, password=password)
    return conn


def main() -> None:
    conn = get_db()
    cur = conn.cursor(buffered=True)
    cur.execute("SELECT * from users;")
    print(cur.fetchone())
    cur.close()
    conn.close()
    print("hello")
    return None


if __name__ == "__main__":
    main()
