from sys import executable
import discord
from discord.ext import commands
import youtube_dl
from youtube import *
import asyncio

# bot is configured as a class object, so the methods will be commands


class youtube_player(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.link = ''
        self.queue = []

# Join makes bot join the voice channel of whoever says the command

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Join VC, nerd!")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    # Makes bot disconnect

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()

    #Play is pretty intensive, this actually holds the code that streams youtube to the discord bot's voice -- typically going to be used by other methods, as it only takes a youtube link as params

    @commands.command()
    async def play(self, ctx, url):
        FFMPEG_OPTIONS = {
            'before_options':
            '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        YDL_OPTIONS = {'format': 'bestaudio'}
        vc = ctx.voice_client
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:

            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(
                url2, **FFMPEG_OPTIONS)
            vc.play(source)
            await ctx.send('NOW PLAYING; ' + str(info['title']))

    #Loops through the list of youtube links

    @commands.command()
    async def playqueue(self, ctx):
        while len(self.queue) >= 1:
            ctx.voice_client.stop()
            info = youtube_dl.YoutubeDL().extract_info(self.queue[0],
                                                       download=False)
            await self.play(ctx, self.queue[0])
            clock = int(info['duration'])
            await asyncio.sleep(clock)
            self.queue.remove(self.queue[0])
        await ctx.send('Queue Ended')

    #Clears the list of youtube links

    @commands.command()
    async def clearqueue(self, ctx):
        self.queue = []
        await ctx.send('Queue Cleared, add new songs')

    @commands.command()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send('Paused')

    @commands.command()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send('Resumed')

    # Search using a different youtube api module, than the one used for Play's streaming code. This returns 'valid' youtube links.
    #Addto will add those links to a list

    @commands.command()
    async def search(self, ctx, qry):
        srch = Search(qry)
        lnk = srch[0]['vid']
        self.link = f'https://www.youtube.com/watch?v={lnk}'
        await ctx.send("Here's what I found;")
        await ctx.send(self.link)

    @commands.command()
    async def addto(self, ctx):
        self.queue.append(self.link)
        await ctx.send('Song added')

    @commands.command()
    async def playnext(self, ctx):
      self.queue.insert(1, self.link)
      info = youtube_dl.YoutubeDL().extract_info(
        self.link,
        download=False
      ) 
      await ctx.send('UP NEXT; ' + str(info['title']))

    #lists all commands that are implemented, with small decriptions
    
    @commands.command()
    async def plzhelp(self, ctx):
      commands = {
        'join': 'makes me join a voice chat',
        'disconnect': 'kicks me :(',
        'play': "I'll play a song directly from a YouTube link",
        'search': 'Fetches a youtube link',
        'addto': "adds a song to my internal playlist",
        'playqueue': "I'll play the songs in my internal playlist",
        'playnext': "I will play you're most recent search, next in the queue",
        'pause': "I'm not a big fan of this one, but it is a feature",
        'resume': 'Significantly better than pause',
        'clearqueue': 'If you wanna wipe my internal playlist',
        

      }
      for k in commands.keys():

        await ctx.send(k + ': ' + commands[f'{k}'])

    #just a little something for me ;)

    @commands.command()
    async def PhantomsSecretPlaylist(self, ctx):
      self.queue = []
      self.playqueue()
      await ctx.send("Currently playing Master's top secret playlist, enjoy my liege..")
      


def setup(client):
    client.add_cog(youtube_player(client))
