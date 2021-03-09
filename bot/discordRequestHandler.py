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
        pass


    if message.content.startswith('!RECOMMENDED'):
        await message.channel.send('This functionality currently does not exist. '
                                   'Please check during a later sprint. ')

    if message.content.startswith('!BELOW'):
        """This function should now be able to handle more than just $20.
            This function searches the product dB and displays the first
            ten values under the price inputtued by the user.
        """
        #Substring the user's input to get the integer value.
        below = message.content[6:]
        #Check if the Substring contains a digit.
        if(below.isdigit()):
            _db = Database.instance(None)
            sel = Select("products", ["product_id"])
            sel.less_than_or_equal_to("sale_price", below)
            products = []
            for product in get_record(sel):
                products.append(product[0])
            msg = "The products below ", below , " are: {}".format(str(products[:10]))
            await message.channel.send(msg)
        else:
            #Simple help response if the user inputs something other than a digit.
            await message.channel.send(
            'Please type a integer after !BELOW'
            '\n Example !BELOW20'
            '\n this will return the first ten items below $20')
