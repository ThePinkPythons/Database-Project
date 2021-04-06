from random import randint

from orders.handler import Order
from products.handler import GetProduct
from user.handler import GetUsers

MIN = 1
MAX = 999999


async def check_if_user_has_account(user_name):
    """Check if the user has an account if not return false."""
    user = GetUsers()
    user.by_author_id(user_name)
    user = user.query()
    if len(user) > 0:
        return True
    else:
        return False


async def create_order_line_items(user_name, message):
    """Append new list to the orders table"""
    user = GetUsers()
    user.by_author_id(user_name)
    user = user.query()
    try:
        user = list(user[0].keys())
        print(message)
        new_order = Order(user[0], user[1], user[2], user[3], user[4], message[1], message[2], message[4],
                          message[3]).save()
    except Exception as e:
        print(e)


async def orders(message):
    user_orders = []
    products = GetProduct()
    # Create for loop for getting all products

    products.by_author_id(message.author)
    await message.author.send("Your past orders were: {}".format(str(user_orders)))


async def cancel(message):
    user = GetUsers()
    user.by_author_id(message.author.name)
    user = user.query()
    await message.author.send("There are no orders to cancel for user | " + message.author.name)


async def create_new_order(message):
    """Create new order and convert to list"""
    order_details = message.content.split(",")
    order_details.append(randint(MIN, MAX))
    await create_order_line_items(message.author.name, order_details)


async def place_order(message):
    if await check_if_user_has_account(message.author.name):
        # await message.channel.send('Please enter the product_id and quantity you would like, separated by spaces')
        await create_new_order(message)
    if await check_if_user_has_account(message.author):
        await message.author.send('Please enter the product_id and quantity you would like, separated by spaces')
        # wait for the user's next message
        NEWORDER = True
        await create_new_order(message)
    else:
        await message.author.send(
            'You must have a user to create an order.'
            '\n To do this enter your address, city, state, and zip separated by spaces')
        # wait for the user's next message
        CURRENTUSERACTION = True
