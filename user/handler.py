"""
User table handler. The UUID for a User is the author_id. User is not reusable.
"""

from db.crud.executor import create_records, get_record, delete_record, create_table, drop_table

from db.sql.query.builder import Create, Select, Delete, CreateTable, DropTable
from db.templates.dbobject import DatabaseObject


USER_TABLE_MAPPING = {
    "author_id": "varchar",
    "address": "varchar",
    "city": "varchar",
    "state": "varchar",
    "zip": "varchar"
}


class User(DatabaseObject):

    def __init__(self, author_id, address, city, state, zip):
        """
        Constructor

        :param author_id:   User name
        :param address: User address
        :param city:    User city:
        :param state:   User state
        :param zip: User zip
        """
        super().__init__()
        self._user = {
            "author_id": author_id,
            "address": address,
            "city": city,
            "state": state,
            "zip": zip
        }
        self._keys = USER_TABLE_MAPPING.keys()

    def save(self):
        """
        Saves the user to the database
        """
        create = Create("users", self._keys)
        create_records(self._keys, create, [self._user])


class GetUsers(object):

    def __init__(self):
        """
        Constructor
        """
        self._fields = USER_TABLE_MAPPING.keys()
        self.select = Select("users", self._fields)

    def by_author_id(self, author_id):
        """
        Sets the author_id condition.

        :param author_id:   author_id to search by
        """
        self.select.equals("author_id", author_id)

    def by_address(self, address):
        """
        Get by the address

        :param address: Address to search by
        """
        self.select.equals("address", address)

    def in_city(self, city):
        """
        Get by the city

        :param city:    City to search by
        """
        self.select.equals("city", city)

    def in_state(self, state):
        """
        Get by the state

        :param state:   The state to search by
        """
        self.select.equals("state", state)

    def in_zip(self, zip):
        """
        Get by the zip code

        :param zip: Zip code to get by
        """
        self.select.equals("zip", zip)

    def query(self):
        """
        Get the users

        :return:    Dictionaries of objects
        """
        records = []
        # must use the for loop does not work otherwise
        for row in get_record(self.select):
            record = dict(zip(self._fields, row))
            records.append(record)
        self.select = Select("users", self._fields)
        return records


class DeleteUser(object):
    """
    ORM for deleting a user
    """

    def __init__(self):
        """
        Constructor
        """
<<<<<<< HEAD
        self.delete = Delete("orders")
=======
        self._delete = Delete("users")
>>>>>>> discord

    def by_author_id(self, author_id):
        """
        Deletes users with the given author_id

        :param author_id:   author_id to delete by
        """
<<<<<<< HEAD
        self.delete.equals("author_id", author_id)
=======
        self._delete.equals("author_id", author_id)
>>>>>>> discord

    def in_city(self, city):
        """
        Deletes users in the given city

        :param city:   The city
        """
<<<<<<< HEAD
        self.delete.equals("city", city)
=======
        self._delete.equals("city", city)
>>>>>>> discord

    def in_state(self, state):
        """
        Deletes users in the given state

        :param state:   The state
        """
<<<<<<< HEAD
        self.delete.equals("state", state)
=======
        self._delete.equals("state", state)
>>>>>>> discord

    def in_zip(self, zip):
        """
        Deletes users in the given zip code

        :param zip:   The zip code
        """
<<<<<<< HEAD
        self.delete.equals("zip", zip)
=======
        self._delete.equals("zip", zip)
>>>>>>> discord

    def delete(self):
        """
        Delete the record
        """
<<<<<<< HEAD
        delete_record(self.delete)
        self.delete = Delete("users")
=======
        delete_record(self._delete)
        self._delete = Delete("users")
>>>>>>> discord


def create_users_table():
    """
    Creates the users table
    """
    query = CreateTable("users", USER_TABLE_MAPPING)
    create_table(query)
<<<<<<< HEAD
=======


def drop_users_table():
    """
    Drops the users table
    """
    query = DropTable("users")
    drop_table(query)
>>>>>>> discord
