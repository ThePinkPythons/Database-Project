"""
User table handler. The UUID for a User is the email. User is not reusable.
"""
from db.crud.executor import create_records, get_record, delete_record, create_table
from db.sql.query.builder import Create, Select, Delete, CreateTable
from db.templates.dbobject import DatabaseObject
from db.io.manager import write_csv_to_sql
from db.sql.connection.singleton import Database
import os

USER_TABLE_MAPPING = {
    "email": "varchar",
    "address": "varchar",
    "city": "varchar",
    "state": "varchar",
    "zip": "varchar"
}

def start():

    fpath = os.getcwd()
    fpath = os.path.sep.join([fpath,"productdata","account_data.csv"])
    Database.instance("",'account_data',USER_TABLE_MAPPING)
    write_csv_to_sql(fpath,headers=USER_TABLE_MAPPING,has_headers=True)


class User(DatabaseObject):

    def __init__(self, email, address, city, state, zip):
        """
        Constructor

        :param email:   User email
        :param address: User address
        :param city:    User city:
        :param state:   User state
        :param zip: User zip
        """
        super().__init__()
        self._user = {
            "email": email,
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

    def by_email(self, email):
        """
        Sets the email condition.

        :param email:   Email to search by
        """
        self.select.equals("email", email)

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
        self.delete = Delete("orders")

    def by_email(self, email):
        """
        Deletes users with the given email

        :param email:   Email to delete by
        """
        self.delete.equals("email", email)

    def in_city(self, city):
        """
        Deletes users in the given city

        :param state:   The city
        """
        self.delete.equals("city", city)

    def in_state(self, state):
        """
        Deletes users in the given state

        :param state:   The state
        """
        self.delete.equals("state", state)

    def in_zip(self, zip):
        """
        Deletes users in the given zip code

        :param zip:   The zip code
        """
        self.delete.equals("zip", zip)

    def delete(self):
        """
        Delete the record
        """
        delete_record(self.delete)
        self.delete = Delete("users")


def create_users_table():
    """
    Creates the users table
    """
    query = CreateTable("users", USER_TABLE_MAPPING)
    create_table(query)
