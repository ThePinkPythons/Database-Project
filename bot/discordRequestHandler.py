"""
Discord Message Handler
"""
from bot import orderHandler
from db.crud.executor import get_record
from db.sql.connection.singleton import Database
from db.sql.query.builder import Select
from db.sql.query.utilities import create_select

CURRENTUSERACTION = None
NEWORDER = None
CANCELLING = None


async def handle(message):
    if message.content.startswith('!CANCEL'):
        # Cancel function
        pass

    if message.content.startswith("!STATUS"):
        # Status function
        await message.author.send("The status of this order is...")

    if message.content.startswith('!NEW'):
        # New Order Function
        if await orderHandler.check_if_user_has_account(message.author):
            await message.author.send('Please enter the product_id and quantity you would like, separated by spaces')
            # wait for the user's next message
            NEWORDER = True
            await orderHandler.create_new_order(message)
        else:
            await message.author.send(
                'You must have a user to create an order.'
                '\n To do this enter your email, address, city, state, and zip separated by spaces')
            # wait for the user's next message
            CURRENTUSERACTION = True

    if message.content.startswith('!HELP'):
        await message.author.send(
            'To create an account type: account'
            '\nFor past orders type: orders'
            '\nFor recommended products type: recommended'
            '\nFor products that cost less than $20 type: below20'
            '\nTo create a new order type: new')

    if message.content.startswith('!ORDERS'):
        await message.author.send('This functionality currently does not exist. '
                                  '\nPlease check during a later sprint. ')

    if message.content.startswith('!RECOMMENDED'):
        """This function currently checks to see if the user has previous orders. If they do not it returns a list of
           five items by their product Id.
        """
        users_orders = create_select("orders", ["*"], "user_name = {}".format(message.author.name))
        list_orders = get_record(users_orders)
        if list_orders.size == 0:
            _db = Database.instance(None)
            sel = Select("products", ["product_id"], None, None, 5)
            products = get_record(sel)
            if products:
                msg = "I would like to recommend {}".format(str(products))
                await message.author.send(msg)

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
            if products:
                msg = "The products below ", below, " are: {}".format(str(products[:10]))
                await message.author.send(msg)
            else:
                await message.author.send("Server side error. Try again later.")
        else:
            # Simple help response if the user inputs something other than a digit.
            await message.author.send(
                'Please type a integer after !BELOW'
                '\n Example !BELOW20'
                '\n this will return the first ten items below $20')
