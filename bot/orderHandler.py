from random import randint

from orders.handler import Order
from products.handler import GetProduct,Product
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



async def orders(message):
    """Used to view past orders."""
    user_orders = []
    products = GetOrders()
    # Create for loop for getting all products
    for orders in products.by_author_id(message.author):
        user_orders.append(order)
    print(user_orders)
    await message.author.send("Your past orders were: {}".format(str(user_orders)))


async def cancel(message):
    """Cancel a recently placed order."""
    user = GetUsers()
    user.by_author_id(message.author.name)
    user = user.query()
    await message.author.send("There are no orders to cancel for user | " + message.author.name)

#TODO:
async def place_order(message):
    """Create a new order.
    First check if the user has an account.
    Requires:
        product_id and quantity.
    """
    if await check_if_user_has_account(message.author.name):
        order_details = message.content.split(",")
        #Remove !NEW from list
        order_details.pop(0)
        #Insert order_Id as order_details[2]
        order_details.insert(0,randint(MIN,MAX))
        order_details.insert(0,message.author.name)
        print(order_details)
        product_id_details = GetProduct()
        product_id_details.by_product_id(order_details[2])
        product_id_details = product_id_details.query()
        product_id_details = product_id_details[0]
        print(product_id_details)
        #quantity, wholesale, sale , supplier product_id
        Product(order_details[2],product_id_details['wholesale_price'],product_id_details['sale_price'],product_id_details['supplier_id']).save()

    else:
        await message.author.send("Please create an account using the '!ADD' command. Use !help for help")
