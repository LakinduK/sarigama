import discord
import os
from keep_alive import keep_alive
from discord.ext import commands
import music

cogs = [music]

# bot prefix setup
client = commands.Bot(command_prefix='!', intents = discord.Intents.all())

for i in range(len(cogs)):
  cogs[i].setup(client)



# Run bot
# copy the discord client secret key, add as an environment variable, use it as per below 
keep_alive()
client.run(os.environ['TOKEN'])
