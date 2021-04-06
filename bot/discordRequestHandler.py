"""
Discord Message Handler
"""

from bot import orderHandler, user_functions
from bot import recommend

CURRENTUSERACTION = None
NEWORDER = None
CANCELLING = None


# TODO: Split file into other files.


async def handle(message):
    """Handler user message"""
    if message.content.startswith('!ADD'):
        """This function creates a new user. """
        await user_functions.add_user(message)

    if message.content.startswith('!CANCEL'):
        """This function will set the status of an order to cancelled."""
        await orderHandler.cancel(message)

    if message.content.startswith("!STATUS"):
        # Status function
        await message.author.send("The status of this order is...")

    if message.content.startswith('!NEW'):
        # New Order Function
        await orderHandler.place_order(message)

    if message.content.startswith('!HELP'):
        """This will call the help function from 'user_functions' and display commands."""
        await user_functions.get_help(message)

    if message.content.startswith('!ORDERS'):
        """This function displays the users order history by order Id with product_id, 
           quantity, price and status. 
        """
        await orderHandler.orders(message)

    if message.content.startswith('!RECOMMENDED'):
        """This function currently returns a list of five random items by their product Id.
        """
        await recommend.recommend(message)

    if message.content.startswith('!BELOW'):
        """This function should now be able to handle more than just $20.
           This function searches the product dB and displays the first
           ten values under the price input by the user.
        """
        await recommend.below(message)
