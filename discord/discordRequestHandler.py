import sqlite3
import add
import newOrder
#from db.crud.executor import create_table, create_records
#from db.sql.connection.singleton import Database
#from db.sql.query.builder import CreateTable, Create


async def handle(message):

    if message.content.startswith("!Account"):
        await add.add_user_to_the_system(message)

    if await add.check_if_user_has_account(message.author):
            if message.content.startswith('!Cancel'):
                 #Cancel function
                 pass
            if message.content.startswith("!Status"):
                #Status function
                await message.channel.send("The status of this order is...")

            if message.content.startswith("!New"):
                #New Order Function
                await newOrder.create_new_order(message)
    else:
        await add.prompt_user_to_add_account(message)
