import discord
from discord.ext import commands
import music

cogs = [music]

for i in range(len(cogs)):
  cogs[i].setup()

# bot prefix setup
client = commands.Bot(command_prefix='!!', intents = discord.Intents.all())


# Run bot
client.run()