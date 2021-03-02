async def handle(message):
    if message.content.startswith('!CANCEL'):
        # Cancel function
        pass

    if message.content.startswith("!STATUS"):
        # Status function
        await message.channel.send("The status of this order is..."):

    if message.content.startswith('!HELP'):
        await message.channel.send(
            'For past orders type: orders'
            '\n For recommended products type: recommended'
            '\n For products that cost less than $20 type: below20')

    if message.content.startswith('ORDERS'):
        await message.channel('Your past orders were: ')


    if message.content.startswith('RECOMMENDED'):
        await message.channel.send('This functionality currently does not exist. '
                                   'Please check during a later sprint. ')

    if message.content.startswith('BELOW20'):
        await message.channel.send('The products below $20 are: ')

