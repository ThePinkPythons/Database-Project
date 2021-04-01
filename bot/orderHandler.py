from random import randint

from db.crud.executor import get_record
from db.sql.query.utilities import create_select

order_id_min = 1
order_id_max = 999999

def create_order_line_items(message):
    pass


async def check_if_user_has_account(user_name):
    """ Function to  Check the user db to see if message.author is already in the system if so return true. """
    query = create_select("users", "*", "user_name = {}".format(user_name))
    if get_record(query) is not None:
        return True
    return False



async def create_new_order(message):
    """Function used to create a new order"""
    order_details = message.content.split(" ")
    # Used to create an order_id
    order_details.append(randint(order_id_min, order_id_max))
    create_order_line_items(message)
