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
        else:
            self.connection.commit()

    def delete_log_procedure(self):
        self._execute_query('DROP PROCEDURE IF EXISTS delete_insertion_log;')
        sql = "CREATE PROCEDURE delete_insertion_log() BEGIN DELETE FROM insert_log; END"
        self._execute_query(sql)

    def scheduled_deletion(self, minutes):
        self._execute_query('SET @@global.event_scheduler = ON;')
        sql = "CREATE EVENT delete_log ON SCHEDULE AT CURRENT_TIMESTAMP + INTERVAL {} MINUTE DO " \
              "CALL delete_insertion_log();" \
              " END".format(minutes)
        try:
            self._execute_query(sql)
        except mdb.ProgrammingError as e:
            db_logger.exception(e)

    def log_on_insertion(self):
        sql = "CREATE TABLE IF NOT EXISTS insert_log (id INT NOT NULL AUTO_INCREMENT PRIMARY KEY," \
              "time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP," \
              "row_id INT NOT NULL)"
        self._execute_query(sql)
        self._execute_query("DROP TRIGGER IF EXISTS insert_logging")
        sql = "CREATE TRIGGER insert_logging " \
              "AFTER INSERT ON check_in FOR EACH ROW BEGIN " \
              "INSERT  INTO insert_log SET row_id=NEW.id;" \
              "END"
        self._execute_query(sql)