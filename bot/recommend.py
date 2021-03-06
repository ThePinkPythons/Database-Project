from db.crud.executor import get_record
from db.sql.connection.singleton import Database
from db.sql.query.builder import Select
import random
import csv


async def below(message):
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

        rand_products = []
        while rand_products != 10:
            rand_product_id = random.randint(0, len(products)-1)
            chosen_random_prod = products[rand_product_id][0]
            rand_products.append(chosen_random_prod)
        msg = "The products below ", below, " are: {}".format(str(rand_products))
        await message.channel.send(msg)
    else:
        # Simple help response if the user inputs something other than a digit.
        await message.channel.send(
            'Please type a integer after !BELOW'
            '\n Example !BELOW20'
            '\n this will return the first ten items below $20')


async def recommend(message):
    rand_prods = []
    products = []
    with open("product_data.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            rand_prods.append(row)

    db_length = len(rand_prods)
    while len(products) != 5:
        rand_prodid = random.randint(0, db_length - 1)
    
        chosen_prodid = rand_prods[rand_prodid][0]
        products.append(chosen_prodid)
        print(chosen_prodid)

    # _db = Database.instance(None)
    # Select from products dB using params Group,Order,Limit
    # sel = Select("products", ["product_id"], None, None, 5)
    # products = []
    # TODO:
    """
        If statement checks if the user has ordered anything before the recommend
        five items. If not recommend five random items from product list. 
    """
    # for product in get_record(sel):
    #    products.append(product[0])

    if products:
        msg = "I would like to recommend {}".format(str(products))
        await message.author.send(msg)
    else:
        await message.author.send("Server side error. Try again later.")