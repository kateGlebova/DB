from logging import getLogger

import MySQLdb as mdb

from app.connection import close_connection
from lab2.settings import DATABASES

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

    def create_table(self, entity):
        """

        :type entity: BaseModel subclass
        """
        sql = "CREATE TABLE IF NOT EXISTS {} (".format(entity.table_name)
        for column, type in sorted(entity.columns.items()):
            sql += "{} {} ".format(column, type)
            if column == entity.primary_key:
                sql += "AUTO_INCREMENT "
            if column in entity.null:
                sql += " NULL,"
            else:
                sql += " NOT NULL,"
        sql += "PRIMARY KEY ({}))".format(entity.primary_key)
        self._execute_query(sql)

    def get_list(self, entity):
        """

        :rtype: tuple of dictionaries
        :type entity: BaseModel subclass
        """
        sql = "SELECT * FROM {}".format(entity.table_name)
        self._execute_query(sql)
        return self.cur.fetchall()

    def create(self, entity, dict_values):
        """

        :type values: dictionary
        :type entity: BaseModel subclass
        """
        columns = values = ''
        for column in sorted(entity.columns):
            if column not in entity.null or column in entity.null and column in dict_values:
                if column != entity.primary_key:
                    columns += "{},".format(column)
                    values += "'{}',".format(dict_values[column])

        sql = "INSERT INTO {} ({}) VALUES ({})".format(entity.table_name, columns[:-1], values[:-1])
        self._execute_query(sql)

    def get(self, entity, id):
        sql = "SELECT * FROM {} WHERE {} = {}".format(entity.table_name, entity.primary_key, id)
        self._execute_query(sql)
        return self.cur.fetchone()

    def update(self, entity, id, dict_values):
        updates = ''
        for column in dict_values:
            updates += "{} = '{}',".format(column, dict_values[column])

        sql = "UPDATE {} SET {} WHERE {} = {}".format(entity.table_name, updates[:-1], entity.primary_key, id)
        self._execute_query(sql)

    def delete(self, entity, id):
        sql = "DELETE FROM {} WHERE {} = {}".format(entity.table_name, entity.primary_key, id)
        self._execute_query(sql)
