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
    def instance(cls, database):
        """
        Returns an instance of the database instance

        :param database:    Name of the database
        :return:    The class instance
        """
        if cls._instance is None:
            cls._instance = sqlite3.connect(database, timeout=30)
        return cls._instance
