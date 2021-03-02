"""
A basic database object 'interface'
"""


class DatabaseObject(object):
    """
    Database Object to extend and overwrite
    """

    def __init__(self):
        """
        Empty Constructor
        """
        pass

    def save(self):
        """
        Save Function
        """
        raise ValueError("Save is Not Implemented")
