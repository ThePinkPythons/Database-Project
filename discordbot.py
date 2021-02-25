import discord
import discordRequestHandler

client = discord.Client()


@client.event
async def on_ready():
    await client.channel.send("Hi, I am Bytes the Pink Pythons team bot. For a list of commands type '!help'.")
    print("Connecting as", client.user.name)


@client.event
async def on_message(message):
    # Check if the user who sent the message is this bot.
    if message.author == client.user:
        return
    await discordRequestHandler.handle(message.upper())


# I dont want to store a secret api key on discord
# Dont upload the code.txt file!!!
def get_code():
    with open('code.txt') as f:
        return f.readline()


# Token
client.run(get_code())