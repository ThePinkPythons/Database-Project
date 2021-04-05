from random import randint

from orders.handler import Order
from products.handler import GetProduct
from user.handler import GetUsers

MIN = 1
MAX = 999999


async def check_if_user_has_account(user_name):
    """Check if the user has an account if not return false."""
    user = GetUsers()
    user.by_email(user_name)
    user = user.query()
    if len(user) > 0:
        return True
    else:
        return False


async def create_order_line_items(user_name, message):
    """Append new list to the orders table"""
    user = GetUsers()
    user.by_email(user_name)
    user = user.query()
    try:
        user = list(user[0].keys())
        print(message)
        new_order = Order(user[0], user[1], user[2], user[3], user[4], message[1], message[2], message[4],
                          message[3]).save()
    except Exception as e:
        print(e)


async def order(message):
    products = GetProduct()
    # Create for loop for getting all products
    # product.by


async def cancel(message):
    user = GetUsers()
    user.by_email(message.author.name)
    user = user.query()
    await message.channel.send("There are no orders to cancel for user | " + message.author.name)


async def create_new_order(message):
    """Create new order and convert to list"""
    order_details = message.content.split(",")
    order_details.append(randint(MIN, MAX))
    await create_order_line_items(message.author.name, order_details)
