import discord
from discord.ext import commands
from discord import FFmpegOpusAudio
from dotenv import load_dotenv, find_dotenv
from time import *
import os
import youtube_dl
import requests

spotify = commands.Bot(command_prefix="spotify.", intents=discord.Intents.all())

load_dotenv(find_dotenv())
MARONG_SPOTIFY_TOKEN = os.getenv('MARONG_SPOTIFY_TOKEN')

@spotify.event
async def on_ready():
    await spotify.change_presence(activity=discord.Game(name="marong.spotify"))
    print(f"{spotify.user} is ready!\n*-----* Online *-----*")

@spotify.event
async def on_message(ctx):
    if ctx.author is spotify.user:
        return
    await spotify.process_commands(ctx)

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn',}
YTDL_OPTIONS = {'format': 'bestaudio/best','extractaudio': True,'audioformat': 'mp3','outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s','restrictfilenames': True,'noplaylist': True,'nocheckcertificate': True,'ignoreerrors': False,'logtostderr': False,'quiet': True,'no_warnings': True,'default_search': 'auto','source_address': '0.0.0.0',}
@spotify.command()
async def marong(ctx,*,item):
    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()
    else:
        ctx.voice_client.stop()
    if ctx.author.bot:
        return
    if not ctx.author.voice:
        return await ctx.send(embed = discord.Embed(title = "**Please Join a voice channel to play a song.**",colour = discord.Colour.from_rgb(255,0,0)), delete_after = 4)
    if item == None:
        return await ctx.send(embed = discord.Embed(title = "**Please enter a url or song name.**",colour = discord.Colour.from_rgb(255,0,0)), delete_after = 4)
    with youtube_dl.YoutubeDL(YTDL_OPTIONS) as ydl:
        try:
            requests.get(item) 
        except:
            video = ydl.extract_info(f"ytsearch:{item}", download=False)['entries'][0]
        else:
            video = ydl.extract_info(item, download=False)
    audio = await FFmpegOpusAudio.from_probe(video['formats'][0]['url'],**FFMPEG_OPTIONS)
    ctx.voice_client.play(source = audio)
    
    

spotify.run(MARONG_SPOTIFY_TOKEN)