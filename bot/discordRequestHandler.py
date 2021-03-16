"""
Discord Message Handler
"""
from db.crud.executor import get_record
from db.sql.connection.singleton import Database
from db.sql.query.builder import Select
from db.sql.query.builder import CreateTable, Create, Select
from db.sql.query.utilities import create_select, delete_record
import user.handler
from random import randint

CURRENTUSERACTION = None
NEWORDER = None
CANCELLING = None
MIN = 1
MAX = 999999


async def check_if_user_has_account(user_name):
    # Check the user db to see if message.author is already in the system if so return true.
    #TODO: Connect to dB.
    query = create_select("users", "*", ("user_name = " , user_name))
    if get_record(query) is not None:
        return True
    return False


async def create_new_order(message):
    order_details = message.content.split(" ")
    order_details.add(randint(MIN, MAX))
    create_order_line_items(message)


async def handle(message):
    if message.content.startswith('!CANCEL'):
        # Cancel function
        pass

    if message.content.startswith("!STATUS"):
        # Status function
        await message.channel.send("The status of this order is...")

    if message.content.startswith('!NEW'):
        # New Order Function
        if await check_if_user_has_account(message.author):
            await message.channel.send('Please enter the product_id and quantity you would like, separated by spaces')
            # wait for the user's next message
            NEWORDER = True
            await create_new_order(message)
        else:
            await message.channel.send(
                'You must have a user to create an order.'
                '\n To do this enter your email, address, city, state, and zip separated by spaces')
            # wait for the user's next message
            CURRENTUSERACTION = True

    if message.content.startswith('!HELP'):
        await message.channel.send(
            'To create an account type: account'
            '\nFor past orders type: orders'
            '\nFor recommended products type: recommended'
            '\nFor products that cost less than $20 type: below20'
            '\nTo create a new order type: new')

    if message.content.startswith('!ORDERS'):
        await message.chnnel.send('This functionality currently does not exist. '
                                  '\nPlease check during a later sprint. ')

    if message.content.startswith('!RECOMMENDED'):
        await message.channel.send('This functionality currently does not exist. '
                                   '\nPlease check during a later sprint. ')

    if message.content.startswith('!BELOW'):
        """This function should now be able to handle more than just $20.
            This function searches the product dB and displays the first
            ten values under the price input by the user.
        """
        # Substring the user's input to get the integer value.
        below = message.content[6:]
        # Check if the Substring contains a digit.
        if below.isdigit():
            _db = Database.instance(None)
            sel = Select("products", ["product_id"])
            sel.less_than_or_equal_to("sale_price", below)
            products = []
            for product in get_record(sel):
                products.append(product[0])
            msg = "The products below ", below, " are: {}".format(str(products[:10]))
            await message.channel.send(msg)
        else:
            # Simple help response if the user inputs something other than a digit.
            await message.channel.send(
                'Please type a integer after !BELOW'
                '\n Example !BELOW20'
                '\n this will return the first ten items below $20')
