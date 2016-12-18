from logging import getLogger

import MySQLdb as mdb

from check_in.connection import close_connection
from lab3.settings import DATABASES

db_logger = getLogger("DBlogger")


class Session:
    def __init__(self, connection):
        self.connection = connection
        try:
            if self.connection:
                self.cur = self.connection.cursor(mdb.cursors.DictCursor)
            else:
                raise mdb.Error
        except mdb.Error:
            self.cur = None
            db_logger.exception('Error occurred while creating the cursor.')
            close_connection()
        else:
            self.cur.execute('USE {}'.format(DATABASES['default']['NAME']))

    def _execute_query(self, query):
        if not self.cur:
            db_logger.error('Missing cursor. Try reconnecting to the database.')
            raise mdb.Error
        try:
            self.cur.execute(query)
        except mdb.Error:
            db_logger.exception('Error occurred while executing query {}'.format(query))
            self.connection.rollback()
            raise
        else:
            self.connection.commit()
