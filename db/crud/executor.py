"""
Executes CRUD operations on the sqlite database.
"""
from db.sql.connection.singleton import Database


def create_records(keys, query, batch):
    """
    Create a batch of records

    :para db:   The databas
    :param keys:    Keys to us
    :param query:   The query to use
    :param batch:   Batch to update
    """
    db = Database.instance(None)
    query = str(query)
    data = [tuple([record[x] for x in keys]) for record in batch]
    c = db.cursor()
    c.executemany(query, data)
    db.commit()
    c.close()


def update_record(query):
    """
    Update a record

    :param query:   Query to update with
    """
    query = str(query)
    db = Database.instance(None)
    c = db.cursor()
    c.execute(query)
    db.commit()
    c.close()


def get_record(query, generator=False):
    """
    Select records

    :param query:   The query object
    :param generator:   Whether to turn this fetch into a generator
    :return: records
    """
    query = str(query)
    db = Database.instance(None)
    c = db.cursor()
    it = c.execute(query)
    if generator:
        for row in it:
            yield row
        c.close()
    else:
        return it.fetchall()


def delete_record(query):
    """
    Delete a record

    :param query:   The delete query
    """
    query = str(query)
    db = Database.instance(None)
    c = db.cursor()
    c.execute(query)
    db.commit()
    c.close()
