"""Function used to create account for a user."""

async def check_if_user_has_account(message):
    """Function used to check if the current user has an account."""
    return False

async def prompt_user_to_add_account(message):
    await message.channel.send("It looks like you have not placed an order before.")
    await message.channel.send("To Create an account type: !Account email, address, city, state, city")

async def add_user_to_the_system(message):
    """Used to write new user to the system."""
    newUser = message.content.split()
    #Array that stores the user's details such as order-id
    print(newUser)
    #order_id = newUser[0]
    #email = newUser[1]
    #Needs to include message.author as the username!
    mapping = {
        "order_id": "integer",
        "email": "varchar",
        "address": "varchar",
        "city": "varchar",
        "state": "varchar",
        "zip": "integer"
    }
    keys = mapping.keys()
    _db = Database.instance(":memory:", "orders", mapping)
    create = Create("orders", keys)

    # TODO -- looking for a list of dictionaries that map the column name to the value
    data = [{"a": 1}, {"a": 2}]
    create_records(keys, create, data)


#creates intermediary table on fly
#will this overwrite these files everytime
def create_order_line_items(order_id):

    # creates entirety of database
    # this has to run when application starts

    mapping = {
        "order_id": "integer",
        "product_id": "varchar",
        "quantity": "integer"

    }

    keys = mapping.keys()
    _db = Database.instance(":memory:", "order_line_items", mapping)
    create = Create("order_line_items", keys)

    # TODO -- looking for a list of dictionaries that map the column name to the value
    data = [{"a": 1}, {"a": 2}]
    create_records(keys, create, data)
