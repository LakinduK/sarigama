import discord
from discord.ext import commands
import youtube_dl
from requests import get


# Music commands class init
class music(commands.Cog):
    def __init__(self, client):
        self.client = client

# join bot to channel

    @commands.command()
    async def join(self, ctx):
      await fjoin(self, ctx)

# bot exit command

    @commands.command()
    async def exit(self, ctx):
        await ctx.voice_client.disconnect()

# music play command

    @commands.command()
    async def url(self, ctx, url):
        ctx.voice_client.stop()

        FFMPEG_OPTIONS = {
            'before_options':
            '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        YDL_OPTIONS = {'format': "bestaudio"}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']

            # create stream to play audio
            source = await discord.FFmpegOpusAudio.from_probe(
                url2, **FFMPEG_OPTIONS)
            vc.play(source)

    @commands.command()
    async def play(self, ctx, *, url):
        await fjoin(self, ctx)
        ctx.voice_client.stop()
        

        FFMPEG_OPTIONS = {
            'before_options':
            '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        vc = ctx.voice_client

        # info = ydl.extract_info(url, download=False)
        info = search(url)
        await ctx.send("Playing ▶️ " + info['webpage_url'])
        url2 = info['formats'][0]['url']

        # create stream to play audio
        source = await discord.FFmpegOpusAudio.from_probe(
            url2, **FFMPEG_OPTIONS)
        vc.play(source)

    # music pause

    @commands.command()
    async def ps(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("Music Paused ⏸")


# music resume

    @commands.command()
    async def re(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("Music resumed ⏯️")

YDL_OPT = {'format': 'bestaudio', 'noplaylist': 'True'}


# Search func
def search(arg):
    with youtube_dl.YoutubeDL(YDL_OPT) as ydl:
        try:
            get(arg)
        except:
            video = ydl.extract_info(f"ytsearch:{arg}",
                                     download=False)['entries'][0]
        else:
            video = ydl.extract_info(arg, download=False)

    return video


async def fjoin(self, ctx):
    # check if user is in a voice channel
    if ctx.author.voice is None:
        await ctx.send("You are not in a voice channel!")
    # check if bot is in a voice channel
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)


def setup(client):
    client.add_cog(music(client))
