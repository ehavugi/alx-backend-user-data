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
import mysql.connector as connectori

conv = datetime.datetime.fromtimestamp
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, seperator: str) -> str:
    """return a redacted test without values for fields."""
    msg = message
    for field in fields:
        msg = re.sub(r'{}=[^{}]+{}'.format(field, seperator, seperator),
                     "{}={}{}".format(field, redaction, seperator), msg)
    return msg


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class.
    Class initializer
    format function
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
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
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logger.addHandler(stream_handler)
    return logging.getLogger('user_data')


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Get db connection and return a connect to be used
    """
    user = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.environ.get('PERSONAL_DATA_DB_PASSWORD', "")
    host = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
    db = os.environ.get('PERSONAL_DATA_DB_NAME')

    conn = connectori.connect(user=user, database=db,
                              host=host, password=password)
    return conn


def main() -> None:
    """DB connection and data formatting.
    """
    conn = get_db()
    cur = conn.cursor(buffered=True)
    cur.execute("""SELECT name, email, phone, ssn, password, ip,
                last_login, user_agent from users;""")
    for row in cur.fetchall():
        (name, email, phone, ssn, password, ip, last_login, user_agent) = row
        f = "[HOLBERTON] user_data INFO: name=***; email=***; phone=***; "
        f2 = "ssn=***; password=***; ip={}; last_login={}; user_agent={}"
        print(f + f2.format(ip, last_login, user_agent))
    cur.close()
    conn.close()
    return None


if __name__ == "__main__":
    main()
