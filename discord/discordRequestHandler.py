async def handle(message):
    if message.content.startswith('!CANCEL'):
        # Cancel function
        pass

    if message.content.startswith('!STATUS'):
        # Status function
        await message.channel.send('The status of this order is...')

    if message.content.startswith('!HELP'):
        await message.channel.send(
            'For past orders type: orders'
            '\n For recommended products type: recommended'
            '\n For products that cost less than $20 type: below20')
    if message.content.startswith('ORDERS'):
        pass
    if message.content.startswith('RECOMMENDED'):
        pass
    if message.content.startswith('BELOW20'):
        pass
