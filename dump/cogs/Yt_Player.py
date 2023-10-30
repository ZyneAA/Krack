import os, asyncio, discord, json, requests, sqlite3, csv, re, ffmpy
from discord import opus
from discord.ext import commands, tasks
from discord.utils import get
import yt_dlp as youtube_dl
from cogs import BRIDGE

from cogs.music.queue import Play_List 
from cogs.music import music_embed, audio

class Yt_Player(commands.Cog):        
    
    def __inint__(self, client):
        self.client = client
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Initialized -----'YouTube Player'-----")
        
    def connfig(self, id):
        OPTIONS = {'format': 'bestaudio/best', 
                            'postprocessors': [{
                                    'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3',
                                    'preferredquality': '192',
                                }],
                            'outtmpl': f"./play_now/" + f'{id}',
                    } 
        return OPTIONS

    @commands.command()
    async def play(self, ctx):
        voice = ctx.voice_client
        server_id = ctx.guild
        BRIDGE.QUEUES[server_id].voice = voice
        lol = await BRIDGE.QUEUES[server_id].play()

    @commands.command()
    async def play_now(self, ctx, *, url = 'https://www.youtube.com/watch?v=zSwcTiurwwk'):  
        if not(ctx.voice_client):
            await ctx.send("🐙Not in a voice channel🐙") 
            exit
        voice = ctx.voice_client
        YDL_OPTIONS = self.connfig(ctx.guild.id)  
        if "list" in url:
            await ctx.send("🐙This command can't play a playlist.🐙")  
            exit 
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url = info['url']
            await ctx.send(f"🐙Now loading. Please wait a moment🐙")
            source = discord.FFmpegPCMAudio(url)
            voice.play(source) 
    
    @commands.command()
    async def queue(self, ctx, *, url):   
        server_id = ctx.guild 
        print(BRIDGE.QUEUES[server_id])
        # await ctx.channel.purge(limit = 1) # No need for this line
        if  BRIDGE.QUEUES[server_id].queue == None :
            play_list = Play_List() 
            play_list.add(url)
            BRIDGE.QUEUES[server_id].queue = play_list
        else:
            BRIDGE.QUEUES[server_id].queue.add(url)
        await ctx.send("Added to the queue!")   
    
    @commands.command()
    async def clear_queue(self, ctx):   
        server_id = ctx.guild.id  
        if not server_id in BRIDGE.QUEUES:
            await ctx.send("There is no song in the queue!")
            return
        del BRIDGE.QUEUES[server_id]
        await ctx.send("Queue cleared!")  
    

    @commands.command()
    async def show_queue(self, ctx):  
        server_id = ctx.guild  
        for i in BRIDGE.QUEUES[server_id].queue.play_list:
            await ctx.send(embed = i.song_info)
                 
    @commands.command()
    async def join(self, ctx, *, name):    
        voice_channel = discord.utils.get(ctx.guild.channels, name = name)
        voice = await voice_channel.connect() 
        await ctx.send(f"🐙The bot has joined to {voice_channel} : {voice_channel.id}🐙")
        
    @commands.command()
    async def leave(self, ctx):  
        voice = ctx.voice_client
        await voice.disconnect()
        await ctx.send(f"🐙The bot has disconnected🐙")
        
    @commands.command()
    async def stop(self, ctx):
        voice = ctx.voice_client
        if not voice.is_playing():
            await ctx.send("🐙No song is playing🐙")
        voice.stop()
        
    @commands.command()
    async def pause(self, ctx):
        voice = ctx.voice_client
        if not voice.is_playing():
            await ctx.send("🐙Not song is playing.🐙")
        voice.pause()

async def setup(client):
    await client.add_cog(Yt_Player(client))
    