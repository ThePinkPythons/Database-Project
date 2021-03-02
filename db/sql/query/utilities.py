"""
Utilities for building queries
"""


def create_select(table, fields=["*"], where=None, group=None, order=None, limit=None):
    """
    Creates a select statement
    :param table: The table to select from
    :param where:   Where clause
    :param group:   Group by
    :param order:   Order by clause
    :param limit:   Maximum number of records to return
    :param fields: Fields to select from
    """
    sql = "SELECT {} FROM {}".format(",".join(fields), table)
    if where:
        sql = "{} WHERE {}".format(sql, where)
    if group:
        sql = "{} GROUP BY {}".format(sql, group)
    if order:
        sql = "{} ORDER BY {}".format(sql, order)
    if limit:
        sql = "{} LIMIT {}".format(sql, limit)
    return sql


def create_insert_sql(table, value_dict):
    """
    Create an insert statement for batch insertion

    :param table:   The table to insert into
    :param value_dict:  Value dictionary
    :return:    Insert query
    """
    keys = value_dict.keys()
    values = ",".join(["?" for x in keys])
    sql = "INSERT INTO {}".format(table)
    sql = "{}({}) ({})".format(sql, ",".join(keys), values)
    return sql


def create_update_sql(table, value_dict, where=None):
    """
    Create  and update sql command from the given value

    :param table:  Table to insert into
    :param value_dict: The value dict
    :param where:   Where clause
    :return: Update sql
    """
    updates = []
    for key in value_dict.keys():
        data = value_dict[key]
        if type(data) is str:
            updates.append("{} = '{}'".format(key, data))
        else:
            updates.append("{} = {}".format(key, data))
    sql = "UPDATE {} SET {}".format(table, ",".join(updates))
    if where:
        sql = "{} WHERE {}".format(sql, where)
    return sql


def delete_record_query(table, where):
    """
    Create a delete statement using the table and where clause.
    
    :param table: Table to delete from
    :param where: Where clause
    :return: The sql
    """
    return "DELETE FROM {} WHERE {}".format(table, where)


def create_insert(table, keys):
    """
    Create an insert statement

    :param table:   The table to insert into
    :param keys:    The keys
    :return:    The query
    """
    conditions = ["?" for x in keys]
    query = "INSERT INTO {} ({})".format(table, ",".join(keys))
    query = "{} VALUES({})".format(query, ",".join(conditions))
    return query


def get_create_table_statement(table, mapping):
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
