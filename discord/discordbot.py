import discord
import discordRequestHandler
import add
client = discord.Client()

@client.event
async def on_ready():
    print("Connecting as", client.user.name)


@client.event
async def on_message(message):
    # Check if the user who sent the message is this bot.
    if message.author == client.user:
        return
    #Check if message starts with !
    if message.content.startswith("!"):
    #Next check if the user already has an account
        await discordRequestHandler.handle(message)

# I dont want to store a secret api key on discord
# Dont upload the code.txt file!!!
def get_code():
    with open('code.txt') as f:
        return f.readline()


# Token
client.run(get_code())
