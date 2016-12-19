from logging import getLogger

import MySQLdb as mdb
from lab3.settings import DATABASES as DB

db_logger = getLogger("DBlogger")

CONNECTION = None


def get_connection():
    global CONNECTION
    if CONNECTION:
        return CONNECTION
    config = DB['default']
    try:
        CONNECTION = mdb.connect(config['HOST'], config['USER'], config['PASSWORD'])
    except mdb.Error:
        db_logger.exception('Error occurred while connecting to the database.')
        close_connection()
    else:
        return CONNECTION


def close_connection():
    global CONNECTION
    if CONNECTION:
        CONNECTION.close()
        CONNECTION = None
