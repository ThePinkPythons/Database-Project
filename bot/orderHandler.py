from random import randint

<<<<<<< HEAD
from orders.handler import Order
from products.handler import GetProduct,Product
=======
from orders.handler import Order, GetOrders
from products.handler import GetProduct
>>>>>>> 7a56de70931410a48ff426746011ad335c7fc5dd
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

<<<<<<< HEAD
=======

# TODO:
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
>>>>>>> 7a56de70931410a48ff426746011ad335c7fc5dd


async def orders(message):
    """Used to view past orders."""
    user_orders = []
    products = GetOrders()
    # Create for loop for getting all products
    for orders in products.by_author_id(message.author):
        user_orders.append(orders)
    print(user_orders)
    await message.author.send("Your past orders were: {}".format(str(user_orders)))


async def cancel(message):
    """Cancel a recently placed order."""
    user = GetUsers()
    user.by_author_id(message.author.name)
    user = user.query()
    await message.author.send("There are no orders to cancel for user | " + message.author.name)

<<<<<<< HEAD
#TODO:
=======

# TODO:
async def create_new_order(message):
    """Create new order and convert to list"""
    order_details = message.content.split(",")
    order_details.append(randint(MIN, MAX))
    await create_order_line_items(message.author.name, order_details)


# TODO:
>>>>>>> 7a56de70931410a48ff426746011ad335c7fc5dd
async def place_order(message):
    """Create a new order.
    First check if the user has an account.
    Requires:
        product_id and quantity.
    """
    if await check_if_user_has_account(message.author.name):
        order_details = message.content.split(",")
        # Remove !NEW from list
        order_details.pop(0)
<<<<<<< HEAD
        #Insert order_Id as order_details[2]
        order_details.insert(0,randint(MIN,MAX))
        order_details.insert(0,message.author.name)
=======
        # Insert order_Id as order_details[2]
        order_details.insert(0, randint(MIN, MAX))
        order_details.insert(0, message.author.name)
        try:
            get_Total_Price = GetProduct()
            get_Total_Price.by_product_id(order_details[2])
            order_details.append(get_Total_Price.query())
        except:
            print("Product_ID does not exist.")
>>>>>>> 7a56de70931410a48ff426746011ad335c7fc5dd
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
