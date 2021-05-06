"""
SQL Lite connector
"""

import sqlite3

from db.sql.query.utilities import get_create_table_statement


class Database(object):
    """
    Singleton database
    """
    _database = ":memory"
    _instance = None
    _instantiated = False

    def __init__(database):
        """
        Get a connection to sql lite connection
        """
        raise("Call Instance Instead of the constructor")

    @classmethod
    def instance(cls, database, table=None, mapping=None):
        """
        Returns an instance of the database instance. Executes the create statement
        if the table and column map is provided.

        :param database:    Name of the database
        :param table:   Create the table on instantiation if required
        :param mapping: Mapping to create table with
        :return:    The class instance
        """
        if cls._instance is None:
            print(database)
            cls._instance = sqlite3.connect(database, timeout=30)
            if mapping and table:
                sql = get_create_table_statement(table, mapping)
                cls._instance.execute(sql)
        return cls._instance
