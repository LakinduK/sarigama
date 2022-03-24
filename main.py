import discord
import os
from keep_alive import keep_alive
from music import prefix
from discord.ext import commands
import music

cogs = [music]
activity = discord.Game(name=prefix+"help")
# bot prefix setup (Prefix defined in music.py)
client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all(),activity=activity)
client.remove_command("help")


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(
            "**Invalid command. Try using** `help` **to figure out commands!**"
        )
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('**Please pass in all requirements.**')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "**You dont have all the requirements or permissions for using this command :angry:**"
        )


for i in range(len(cogs)):
    cogs[i].setup(client)



# Run bot
# copy the discord client secret key, add as an environment variable, use it as per below
keep_alive()
client.run(os.environ['TOKEN'])
