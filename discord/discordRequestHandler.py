
async def handle(message):
    if message.content.startswith('!Cancel'):
         #Cancel function
         pass
    if message.content.startswith("!Status"):
        #Status function
        await message.channel.send("The status of this order is...")

    if message.content.startswith("!New"):
        #New Order Function

        await message.channel.send("The status of this order is...")