import discord
from discord.ext import commands
import youtube_dl

# Music commands class init
class music(commands.Cog):
  def __init__(self, client):
    self.client = client


# join bot to channel
  @commands.command()
  async def join(self,ctx):
    
  # check if user is in a voice channel
    if ctx.author.voice is None:
      await ctx.send("You are not in a voice channel!")
    voice_channel = ctx.author.voice.channel
    # check if bot is in a voice channel
    if ctx.voice_client is None:
      await voice_channel.connect()
    else:
      await ctx.voice_client.move_to(voice_channel)
  
  @commands.command()
  async def disconnect(self,ctx):
    await ctx.voice_client.disconnect()


# music play command
  @commands.command()
  async def play(self,ctx,url):
    ctx.voice_client.stop()



def setup(client):
  client.add_cog(music(client))