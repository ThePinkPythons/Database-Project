"""
A query using the decorator pattern
"""
from db.sql import create_select, create_update_sql, delete_record, create_insert


class BaseQuery(object):
    """
    Base Query
    """

    def __init__(self):
        self._conditions = []

    def greater_than(self, field, value):
        """
        Add a greater than condition to the query

        :param field:   The file
        :param value:   Value to be greater than
        :return:
        """
        if type(value) is not str:
            self._conditions.append("{} > {}".format(field, value))

    def less_than(self, field, value):
        """
        Add a greater than codition to the query

        :param field:   The file
        :param value:   Value to be greater than
        :return:
        """
        if type(value) is not str:
            self._conditions.append("{} < {}".format(field, value))

    def greater_than_or_equal_to(self, field, value):
        """
        Add a greater than condition to the query

        :param field:   The file
        :param value:   Value to be greater than
        :return:
        """
        if type(value) is not str:
            self._conditions.append("{} >= {}".format(field, value))

    def less_than_or_equal_to(self, field, value):
        """
        Add a greater than condition to the query

        :param field:   The file
        :param value:   Value to be greater than
        :return:
        """
        if type(value) is not str:
            self._conditions.append("{} <= {}".format(field, value))

    def equals(self, field, value):
        """
        Adds an equals condition to the query.

        :param field:   The field to compare
        :param value:   The value to compare against
        :return:
        """
        if type(value) is str:
            condition = "{} LIKE '{}'".format(field, value)
        else:
            condition = "{} = {}".format(field, value)
        self._conditions.append(condition)

    def __str__(self):
        raise ValueError("Unimplemented")


class Select(BaseQuery):
    """
    Select Statement Query
    """

    def __init__(self, table, fields=["*"], group=None, order=None, limit=None):
        """
        Constructor

        :param table:   Name of the table
        :param fields:  Fields list
        :param group:   Group by clause
        :param order:   Order clause
        :param limit:   Maximum number of records to reurn
        """
        super().__init__(self)
        self._table = table
        self._fields = fields
        self._group = group
        self._order = order
        self._limit = limit

    def __str__(self):
        """
        Stringify the query

        :return:    Query string
        """
        if len(self._conditions) > 0:
            where = " AND ".join(self._conditions)
        else:
            where = None
        return create_select(self._table, self._fields, where, self._group, self._order, self._limit)


class Update(BaseQuery):
    """
    Update Query
    """

    def __init__(self, table, mapping):
        """
        Constructor

        The update mapping is of the form {"key": "value"}

        :param table:   Table to update
        :param mapping: Update mapping
        """
        self._table = table
        self._mapping = mapping

    def __str__(self):
        """
        Creates a string

        :return:    Query String
        """
        if len(self._conditions) > 0:
            where = " AND ".join(self._conditions)
        else:
            where = None
        return create_update_sql(self._table, self._mapping, where)  


class Delete(BaseQuery):
    """
    A Delete Query
    """

    def __init__(self, table):
        """
        Constructor

        :param table:   The table to insert into
        """
        self._table = table

    def __str__(self):
        """
        Delete query

        :return:    The query string
        """
        if len(self._conditions):
            where = " AND ".format(self._conditions)
        else:
            where = None
        return delete_record(self._table, where)


class Create(BaseQuery):
    """
    Create query
    """

    def __init__(self, table, keys):
        """
        Constrcutor

        :param table:   The table
        :param keys:    The keys to insert
        """
        self._table = table
        self._keys = keys

    def __str__(self):
        """
        Generates a create query

        :return:    The query
        """
        return create_insert(self._table, self._keys)