from logging import getLogger

import MySQLdb as mdb

from app.connection import close_connection
from lab2.settings import DATABASES
import xml.etree.ElementTree as ET

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

    def general_select(self, entities, columns=['*'], condition=""):
        """

        :type columns: list of str
        :type entities: list of BaseModel subclasses
        """
        table_names = ''
        for entity in entities:
            table_names += "{},".format(entity.table_name)
        column_names = ''
        for column in columns:
            column_names += "{},".format(column)
        sql = "SELECT {} FROM {} {}".format(column_names[:-1], table_names[:-1], condition)
        self._execute_query(sql)

    def get_by_condition(self, entity, condition=""):
        self.general_select([entity], condition=condition)

    def get_list(self, entity):
        """

        :rtype: tuple of dictionaries
        :type entity: BaseModel subclass
        """
        self.general_select([entity])
        self.get_by_condition(entity)
        return self.cur.fetchall()

    def get_one(self, entity, id):
        self.get_by_condition(entity, "WHERE {} = {}".format(entity.primary_key, id))
        return self.cur.fetchone()

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
                    if entity.columns[column] == 'BOOLEAN':
                        values += "{},".format(dict_values[column])
                    else:
                        values += "'{}',".format(dict_values[column])

        sql = "INSERT INTO {} ({}) VALUES ({})".format(entity.table_name, columns[:-1], values[:-1])
        self._execute_query(sql)
        arbitrary_key = list(dict_values.keys())[0]
        self.get_by_condition(entity, condition="WHERE {}={}".format(arbitrary_key, dict_values[arbitrary_key]))
        return self.cur.fetchone()

    def update(self, entity, id, dict_values):
        updates = ''
        for column in dict_values:
            updates += "{} = '{}',".format(column, dict_values[column])

        sql = "UPDATE {} SET {} WHERE {} = {}".format(entity.table_name, updates[:-1], entity.primary_key, id)
        self._execute_query(sql)

    def delete(self, entity, id):
        for ref, fk in entity.ref.items():
            self.get_by_condition(ref, "WHERE {} = {}".format(fk, id))
            referenced = self.cur.fetchall()
            for row in referenced:
                self.delete(ref, row[ref.primary_key])
        sql = "DELETE FROM {} WHERE {} = {}".format(entity.table_name, entity.primary_key, id)
        self._execute_query(sql)

    def make_fulltext(self, entity, column):
        sql = "ALTER TABLE {} ADD FULLTEXT({})".format(entity.table_name, column)
        self._execute_query(sql)

    def fill_from_xml(self, entity, xml_file):
        old = self.get_list(entity)
        for entry in old:
            self.delete(entity, entry[entity.primary_key])
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for child in root:
            self.create(entity, {column.tag: column.text for column in child})
