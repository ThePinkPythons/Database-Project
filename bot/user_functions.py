from user.handler import User


async def get_help(message):
    await message.author.send(
        'To create an account type: add'
        '\nFor past orders type: orders'
        '\nFor recommended products type: recommended'
        '\nFor products that cost less than $20 type: below20'
        '\nTo create a new order type: new'
        '\nTo cancel an order type: cancel'
        '\nTo get the status of an order type: status')


async def add_user(message):
    new_account = message.content.replace("!ADD", "").split(",")
    new_account.pop(0)
    new_account.insert(0, message.author.name)
    try:
        User(new_account[0], new_account[1], new_account[2], new_account[3], new_account[4]).save()
        await message.author.send("The account has been created!")
    except Exception as e:
        print(e)
        await message.author.send(
            'The account could not be created make sure all details is provided.'
            '\n !ADD,address,city,state,zip')


async def remove_user():
    pass
