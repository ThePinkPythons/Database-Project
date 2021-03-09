"""
Discord Message Handler
"""
from db.crud.executor import get_record
from db.sql.connection.singleton import Database
from db.sql.query.builder import Select


async def handle(message):

    if message.content.startswith('!CANCEL'):
        # Cancel function
        pass

    if message.content.startswith("!STATUS"):
        # Status function
        await message.channel.send("The status of this order is...")

    if message.content.startswith('!HELP'):
        await message.channel.send(
            'For past orders type: orders'
            '\n For recommended products type: recommended'
            '\n For products that cost less than $20 type: below20')

    if message.content.startswith('!ORDERS'):
        await message.channel('Your past orders were: ')


    if message.content.startswith('!RECOMMENDED'):
        await message.channel.send('This functionality currently does not exist. '
                                   'Please check during a later sprint. ')

    if message.content.startswith('!BELOW20'):
        _db = Database.instance(None)
        sel = Select("products", ["product_id"])
        sel.less_than_or_equal_to("sale_price", 20.0)
        products = []
        for product in get_record(sel):
            products.append(product[0])
        msg = "The products below $20 are: {}".format(str(products[:10]))
        await message.channel.send(msg)
