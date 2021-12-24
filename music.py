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
  async def p(self,ctx,url):
    ctx.voice_client.stop()

    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format':"bestaudio"}
    vc = ctx.voice_client

    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(url, download=False)
      url2 = info['formats'] [0]['url']

      # create stream to play audio
      source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
      vc.play(source)

# music pause
  @commands.command()
  async def ps(self,ctx):
    await ctx.voice_client.pause()
    await ctx.send("Music Paused ⏸️")

# music pause
  @commands.command()
  async def re(self,ctx):
    await ctx.voice_client.resume()
    await ctx.send("Music resumed ⏯️")



def setup(client):
  client.add_cog(music(client))