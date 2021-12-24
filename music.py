import discord
from discord.ext import commands
import youtube_dl

# Music commands class init
class music(commands.Cog):
  def __init__(self, client):
    self.client = client

def setup(client):
  client.add_cog(music(client))