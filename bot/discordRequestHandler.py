"""
Discord Message Handler
"""

from bot import orderHandler, user_functions
from bot import recommend

# TODO: Split file into other files.


async def handle(message):
    """Handler user message"""
    if message.content.startswith('!ADD'):
        """This function creates a new user. """
        await user_functions.add_user(message)

    elif message.content.startswith('!CANCEL'):
        """This function will set the status of an order to cancelled."""
        await orderHandler.cancel(message)

    elif message.content.startswith("!STATUS"):
        """This function will get the status of an order based off of the order Id"""
        await orderHandler.order_status(message)


    elif message.content.startswith('!NEW'):
        """This functions creates a new order"""
        await orderHandler.place_order(message)

    elif message.content.startswith('!HELP'):
        """This will call the help function from 'user_functions' and display commands."""
        await user_functions.get_help(message)

    elif message.content.startswith('!ORDERS'):
        """This function displays the users order history by order Id with product_id,
           quantity, price and status.
        """
        await orderHandler.orders(message)

    elif message.content.startswith('!RECOMMENDED'):
        """This function currently returns a list of five random items by their product Id.
        """
        await recommend.recommend(message)

    elif message.content.startswith('!BELOW'):
        """This function should now be able to handle more than just $20.
           This function searches the product dB and displays the first
           ten values under the price input by the user.
        """
        await recommend.below(message)

    else:
        await message.author.send("I do ont understand this message. Use !Help for help.")
