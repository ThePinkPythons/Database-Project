"""File used to handle creating order feature."""

async def create_new_order(message):
    new_order = message.content.split()
    #TODO: 
    #Splits message.content into an array this is then used to access the db
    print(new_order)
    await message.channel.send("Order placed! Thank you.")
