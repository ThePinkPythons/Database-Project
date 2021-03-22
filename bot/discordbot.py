import os

import discord
from . import discordRequestHandler

client = discord.Client()


@client.event
async def on_ready():
    print("Hi, I am Bytes the Pink Pythons team bot. For a list of commands type '!help'.")
    print("Connecting as", client.user.name)


@client.event
async def on_message(message):
    # Check if the user who sent the message is this bot.
    if message.author == client.user:
        return
    else:
        await discordRequestHandler.handle(message)


# I dont want to store a secret api key on bot
# Dont upload the code.txt file!!!
def get_code():
    with open('code.txt') as f:
        return f.readline()


# I dont want to store a secret api key on bot
# Dont upload the code.txt file!!!
def get_code():
    fpath = os.getcwd()
    fpath = os.path.sep.join([fpath, "bot", "productdata", "code.txt"])
    with open(fpath, 'r') as f:
        return f.readline()


def start():
    """
    Start the discord bot
    """
    client.run(get_code())
