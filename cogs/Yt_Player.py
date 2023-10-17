import os, asyncio, discord, json, requests, sqlite3, csv, re, ffmpy
from discord import opus
from discord.ext import commands, tasks
from discord.utils import get
import yt_dlp as youtube_dl

class Yt_Player(commands.Cog):   
    
    queues = {}                
    
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
    
    def play_next(self, ctx):
        print("now inside play_next function")
        voice = ctx.voice_client
        server_id = ctx.guild.id
        if len(self.queues[server_id]) > 0:
            song = self.queues[server_id][0]
            YDL_OPTIONS = {'format': 'bestaudio/best', 
                            'postprocessors': [{
                                    'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3',
                                    'preferredquality': '192',
                                }],
                            'outtmpl': f"./queue/{server_id}/" + 'song',
                    }
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                ydl.download([f"https://www.youtube.com/watch?v={song[0]}"])
                source = discord.FFmpegOpusAudio(f"./queue/{server_id}/song.mp3")
                self.queues[server_id].pop(0)
                voice.play(source, after = lambda e: self.play_next())
                #self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            return
    
    @commands.command()
    async def play(self, ctx):
        voice = ctx.voice_client
        server_id = ctx.guild.id
        if voice.is_playing():
            await ctx.send("Song's already playing stop the song first.")
        if server_id not in self.queues:
            await ctx.send("There's no song in the queue") 
        song = self.queues[server_id][0]
        YDL_OPTIONS = {'format': 'bestaudio/best', 
                            'postprocessors': [{
                                    'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3',
                                    'preferredquality': '192',
                                }],
                            'outtmpl': f"./queue/{server_id}/" + 'song',
                    } 
        await ctx.send("Now playing: "+ song[1])
        if len(self.queues[server_id]) > 0:
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                ydl.download([f"https://www.youtube.com/watch?v={song[0]}"])
                source = discord.FFmpegOpusAudio(f"./queue/{server_id}/song.mp3")
                self.queues[server_id].pop(0)
                voice.play(source, after = lambda e: self.play_next())
    
    @commands.command()
    async def play_now(self, ctx, *, url):  
        if not(ctx.voice_client):
            await ctx.send("🐙Not in a voice channel🐙") 
            exit
        voice = ctx.voice_client
        YDL_OPTIONS = self.connfig(ctx.guild.id)  
        if "list" in url:
            await ctx.send("🐙This command can't play a playlist.🐙")  
            exit 
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)["title"]
            await ctx.send(f"🐙Now loading '{info}'. Please wait a moment🐙")
            ydl.download([url])
            source = discord.FFmpegOpusAudio(f"./play_now/{ctx.guild.id}.mp3")
            voice.play(source)
    
    @commands.command()
    async def queue(self, ctx, *, url):   
        YDL_OPTIONS = {'format': 'bestaudio/best'} 
        if "list" in url:
            await ctx.send("This command is for queuing songs, not for a playlist.")     
        if "https://www.youtube.com/watch?v=" not in url:
            await ctx.send("🐙Must be a valid link from YouTube🐙")     
        server_id = ctx.guild.id  
        if not server_id in self.queues:
            self.queues[server_id] = []
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download = False)
            self.queues[server_id].append([info.get("id", None), info.get("title", None)])
            await ctx.send(self.queues[server_id])   
                 
    @commands.command()
    async def join(self, ctx, *, name):    
        voice_channel = discord.utils.get(ctx.guild.channels, name = name)
        voice = await voice_channel.connect() 
        print(voice_channel.id)  
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
    
    
# info = ydl.extract_info(url, download = False)
            # url = info["formats"][0]['url']
            # with open("lol.json", "w") as f:
            #     json.dump(info, f, indent = 4)