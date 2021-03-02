"""
User table handler. The UUID for a User is the email.
"""
from db.templates.dbobject import DatabaseObject


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
        self._email = email
        self._address = address
        self._city = city
        self._state = state
        self._zip = zip

    def delete(self):
        """
        Delete a user. Only the email is considered
        """
        pass

    def save(self):
        """
        Saves the user to the database
        """
        pass


def get_users():
    """
    Get the users
    """
    pass
