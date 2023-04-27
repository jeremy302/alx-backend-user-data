#!/usr/bin/env python3
''' filtered logger '''
import logging
from typing import List, Any
import csv
import os
import mysql.connector
from mysql.connector import MySQLConnection
import re


dbuser = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
dbpasswd = os.environ.get('PERSONAL_DATA_DB_PASSWORD', '')
dbhost = os.environ.get('PERSONAL_DATA_DB_HOST', 'localhost')
dbname = os.environ.get('PERSONAL_DATA_DB_NAME', '')

PII_FIELDS = ['name', 'email', 'phone', 'ssn', 'password']
# with open('user_data.csv') as file:
#     headers = next(csv.reader(file))
#     PII_FIELDS = headers


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    ''' filter datum '''
    msg = message
    for field in fields:
        msg = re.sub(r'\b{}=[^{}]*'.format(field, separator),
                     r'{}={}'.format(field, redaction),
                     msg)
    return msg
    pairs = [s.split('=') for s in message.split(separator)]
    msgs = []
    for p in pairs:
        if len(p) == 1:
            msgs.append(p[0])
        elif p[0].split(' ')[-1] in fields:
            msgs.append(p[0] + '=' + redaction)
        else:
            msgs.append(p[0] + '=' + p[1])
    return separator.join(msgs)


def get_logger() -> logging.Logger:
    ''' gets logger '''
    formatter = RedactingFormatter(PII_FIELDS)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger('user_data')
    logger.propagate = False
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    return logger


def get_db() -> MySQLConnection:
    ''' gets db connector'''
    return mysql.connector.connect(user=dbuser, password=dbpasswd,
                                   host=dbhost, database=dbname)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields) -> None:
        ''' class constructor '''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        ''' format method '''
        return filter_datum(self.fields, '***', super(
            RedactingFormatter, self).format(record), ';')


def main() -> None:
    ''' main function'''
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    cols = cursor.column_names
    logger = get_logger()

    for row in cursor:
        params = {cols[i]: row[i] for i in range(len(row))}
        msg = ';'.join('{}={}'.format(v[0], v[1]) for v in params.items())
        # print(msg)
        record = logging.LogRecord('user_data', logging.INFO,
                                   None, None, msg, None, None)
        logger.handle(record)
        # logger.info('abc', **params)


if __name__ == '__main__':
    main()
