import discord
from discord.ext import commands
import youtube_player




cogs = [youtube_player]

client = commands.Bot(command_prefix='>>', intents=discord.Intents.all())



for index in range(len(cogs)):
    cogs[index].setup(client)

#please dont steal our token :(

client.run('ODk4MzE3NTQ2Njk1MDU3NDA5.YWidaQ.M-60udqjwbdfscRn55cM_CUq17s')