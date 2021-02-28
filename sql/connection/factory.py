"""
SQL Lite connector
"""

import sqlite3


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
            cls._instance = sqlite3.connect(database, timeout=30)
            sql = get_create_statement(table, mapping)
            if mapping and table:
                cls._instance.execute(sql)
        return cls._instance


def get_create_statement(table, mapping):
    """
    Creates the sql table create statement
    
    :param table:   Table to create 
    :param mapping:   Mapping of attributes and values
    :return:    The SQL statement
    """
    sql = "CREATE TABLE {} (".format(table)
    columns = []
    for (k, v) in mapping.items():
        columns.append("{} {}".format(k, v))
    sql = "{}{})".format(sql, ",".join(columns))
    return sql
