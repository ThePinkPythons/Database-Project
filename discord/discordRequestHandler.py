import sqlite3

from db.crud.executor import create_table, create_records, get_record, delete_record
from db.sql.connection.singleton import Database
from db.sql.query.builder import CreateTable, Create
from db.sql.query.utilities import create_select, delete_record_query
from random import randint

CURRENTUSERACTION = None
NEWORDER = None
CANCELLING = None
MIN = 1
MAX = 999999


async def handle(message):
    if CURRENTUSERACTION is True:
        add_user_to_the_system(message)
        await message.channel.send("User has been created!")
        CURRENTUSERACTION = None

    if NEWORDER is True:
        create_new_order(message)
        await message.channel.send("Your order has been created!")
        NEWORDER = False

    if CANCELLING is True:
        cancel_order(message.content)
        await message.channel.send("Your order has been cancelled!")
        CANCELLING = False

    if message.content.startswith('!HELP'):
        await message.channel.send(
            'To place an order type: !new'
            '\nFor past orders type: !orders'
            '\nFor recommended products type: !recommended'
            '\nFor products that cost less than $20 type: !below20'
            '\nTo cancel an order type: !cancel'
            '\nFor the status of an order type: !status')

    if message.content.startswith('!NEW'):
        # New Order Function
        if check_if_user_has_account(message.author):
            await message.channel.send('Please enter the product_id and quantity you would like, separated by spaces')
            # wait for the user's next message
            NEWORDER = True
            create_new_order(message)
        else:
            await message.channel.send(
                'You must have a user to create an order.\n To do this enter your email, address, city, state, and zip separated by spaces')
            # wait for the user's next message
            CURRENTUSERACTION = True

    if message.content.startswith('!CANCEL'):
        await message.channel.send('Please enter the order number you wish to cancel:')
        CANCELLING = True

    if message.content.startswith("!STATUS"):
        # Status function
        await message.channel.send("The status of this order is...")

    if message.content.startswith('!ORDERS'):
        await message.channel.send('Your past orders were: ')

    if message.content.startswith('!RECOMMENDED'):
        await message.channel.send('This functionality currently does not exist. '
                                   'Please check during a later sprint. ')

    if message.content.startswith('!BELOW20'):
        await message.channel.send('The products below $20 are: ')


async def check_if_user_has_account(user_name):
    # Check the user db to see if message.author is already in the system if so return true.
    query = create_select("users", "*", "user_name = " + user_name)
    if get_record(query) is not None:
        return True
    return False


async def create_new_order(message):
    order_details = message.content.split(" ")
    order_details.add(randint(MIN, MAX))
    create_order_line_items(message)


async def add_user_to_the_system(message):
    """ Function used to add the new user to the system."""
    user_data = message.content.split(" ")
    user_data.add(message.author)
    add_user_to_system(user_data)


async def add_user_to_system(new_user):
    """Used to write new user to the system."""
    # Array that stores the user's details such as user_name
    print(new_user)
    # email = newUser[0]
    # Needs to include message.author as the username!
    mapping = {
        "email": "varchar",
        "address": "varchar",
        "city": "varchar",
        "state": "varchar",
        "zip": "integer",
        "user_name": "varchar"
    }
    keys = mapping.keys()
    _db = Database.instance(":memory:", "users", mapping)
    create = Create("users", keys)
    # do we create table here to be able to put the records into?
    create_records(keys, create, new_user)


# creates intermediary table on fly
# will this overwrite these files everytime
def create_order_line_items(data):
    # creates entirety of database
    # this has to run when application starts
    mapping = {
        "product_id": "varchar",
        "quantity": "integer",
        "order_id": "integer"
    }

    keys = mapping.keys()
    _db = Database.instance(":memory:", "order_line_items", mapping)
    create = Create("order_line_items", keys)

    # TODO -- looking for a list of dictionaries that map the column name to the value
    # do we create table here to be able to put the records into?
    create_records(keys, create, data)


def cancel_order(order_id):
    query = delete_record_query("orders", "id = " + order_id)
    delete_record(query)

