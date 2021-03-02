import sqlite3

from db.crud.executor import create_table, create_records
from db.sql.connection.singleton import Database
from db.sql.query.builder import CreateTable, Create

CURRENTUSERACTION = None

async def handle(message):


    if message.content.startswith('!Cancel'):
         #Cancel function
         pass
    if message.content.startswith("!Status"):
        #Status function
        await message.channel.send("The status of this order is...")

    if message.content.startswith("!New"):
        #New Order Function
        create_new_order(message)

        await message.channel.send("The new order is...")

    if CURRENTUSERACTION == "newUser":
        add_user_to_the_system(message)

async def check_if_user_has_account(message):
    #Check the user db to see if message.author is already in the system if so return true.
    return False

async def create_new_order(message):
    """Create the order.
    Needs user to create account."""
    #Check if the user is already in the system.
    #if not create new user.
    if(check_if_user_has_account(message.author)):
        create_order_line_items()
    else:
        prompt_user_to_add_account(message)

async def add_user_to_the_system(message):
    """ Function used to add the new user to the system."""
    userData = message.content.split()
    add_user_to_system(userData)

async def prompt_user_to_add_account(message):
    await message.channel.send("It looks like you have not placed an order before.")
    await message.channel.send("Enter your email, address, city, state, and zip: ")
    #wait for the usr's next message
    CURRENTUSERACTION = "newUser"

async def add_user_to_system(newUser):
    """Used to write new user to the system."""
    #Array that stores the user's details such as order-id
    print(newUser)
    #order_id = newUser[0]
    #email = newUser[1]
    #Needs to include message.author as the username!
    mapping = {
        "order_id": "integer",
        "email": "varchar",
        "address": "varchar",
        "city": "varchar",
        "state": "varchar",
        "zip": "integer"
    }
    keys = mapping.keys()
    _db = Database.instance(":memory:", "orders", mapping)
    create = Create("orders", keys)

    # TODO -- looking for a list of dictionaries that map the column name to the value
    data = [{"a": 1}, {"a": 2}]
    create_records(keys, create, data)


#creates intermediary table on fly
#will this overwrite these files everytime
def create_order_line_items(order_id):

    # creates entirety of database
    # this has to run when application starts

    mapping = {
        "order_id": "integer",
        "product_id": "varchar",
        "quantity": "integer"

    }

    keys = mapping.keys()
    _db = Database.instance(":memory:", "order_line_items", mapping)
    create = Create("order_line_items", keys)

    # TODO -- looking for a list of dictionaries that map the column name to the value
    data = [{"a": 1}, {"a": 2}]
    create_records(keys, create, data)
