import discord
from discord.ext import commands
import youtube_dl
import asyncio
from requests import get
# from asyncio importasyncio, run

queues = []

prefix = '!'


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

    # bot list clear

    @commands.command()
    async def clear(self, ctx):
        queues.clear()
        await ctx.reply("PlayList Cleared")

    @commands.command()
    async def help(self, ctx):

        txt = """ 
```
!play  <Song name Or song url>
!ps    = PAUSE
!re    = RESUME
!next  = Next song
!list  = Pending song list
!clear = Clear Playlist
!exit  = Disconnect bot from channel
      ```
         """

        msg = txt.replace("!", prefix)
        await ctx.send(msg)

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

    # music list

    @commands.command()
    async def list(self, ctx):
        if len(queues) > 0:
            msg = []

            i = 0
            while i < len(queues):
                msg.append((f'({i+1})  {queues[i]}'))
                i += 1

            await ctx.send('\n'.join(msg))
        else:
            await ctx.send("List is Empty")

    # music pause

    @commands.command(name='ps', aliases=['pause'])
    async def ps(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("Music Paused ⏸")

    # music resume

    @commands.command(name='re', aliases=['resume'])
    async def re(self, ctx):
        ctx.voice_client.resume()
        await ctx.send("Music resumed ⏯️")

    # music next

    @commands.command(name='next', aliases=['skip'])
    async def next(self, ctx):
        await ctx.reply("Skiped ⏯️")
        ctx.voice_client.stop()
        await play_next(ctx)

    @commands.command()
    async def play(self, ctx, *, url):
        await fjoin(self, ctx)
        # ctx.voice_client.stop()
        if "?list=" in url or "&list=" in url:
            add_url(url)
            await ctx.reply("PlayList Added)")
            if not ctx.voice_client.is_playing():
                await play_next(ctx)
            return

        if ctx.voice_client.is_playing():
            info = search(url)
            add_url(url)
            await ctx.reply("Song Queued " + info['webpage_url'])
            return

        FFMPEG_OPTIONS = {
            'before_options':
            '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        vc = ctx.voice_client

        # info = ydl.extract_info(url, download=False)
        info = search(url)
        await ctx.send("Playing ▶️ " + info['webpage_url'])
        print(len(info['formats'][0]['url']))
        url2 = info['formats'][0]['url']

        # create stream to play audio
        source = await discord.FFmpegOpusAudio.from_probe(
            url2, **FFMPEG_OPTIONS)
        vc.play(source, after=lambda e: asyncio.run(play_next(ctx)))


async def play_next(ctx):
    print("Enddedd____")
    if len(queues) > 0:
        print(len(queues))
        url = queues[0]

        FFMPEG_OPTIONS = {
            'before_options':
            '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        vc = ctx.voice_client

        # info = ydl.extract_info(url, download=False)
        info = search(url)
        # await ctx.send("Playing ▶️ " + info['webpage_url'])
        url2 = info['formats'][0]['url']
        # create stream to play audio
        source = await discord.FFmpegOpusAudio.from_probe(
            url2, **FFMPEG_OPTIONS)

        if url in queues: queues.remove(url)

        vc.play(source, after=lambda e: asyncio.run(play_next(ctx)))
    else:
        print("Queue is Emplty")
        # time.sleep(5)
        await asyncio.sleep(5)
        await ctx.send("Queue is Emplty")
        # if not ctx.voice_client.is_playing():
        #  return  ctx.voice_client.disconnect()


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


def add_url(url):
    if "?list=" in url or "&list=" in url:

        res = [
            i.split("=")[-1] for i in url.split("?", 1)[-1].split("&")
            if i.startswith('list' + "=")
        ][0]
        url = 'https://www.youtube.com/playlist?list=' + res
        ydl = youtube_dl.YoutubeDL({
            'outtmpl': '%(id)s%(ext)s',
            'quiet': True,
        })
        video = ""
        print("list" + url)
        with ydl:
            result = ydl.extract_info \
            (url,
            download=False) #We just want to extract the info

            if 'entries' in result:
                # Can be a playlist or a list of videos
                video = result['entries']

                #loops entries to grab each video_url
                for i, item in enumerate(video):
                    video = result['entries'][i]
                    print(video['title'])
                    queues.append(video['title'])

    else:
        queues.append(url)


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
