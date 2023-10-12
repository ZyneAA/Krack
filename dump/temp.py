    
@client.command()
async def queue(ctx, *, url):   
    global queues
    YDL_OPTIONS = {'format': 'bestaudio/best'} 
    if "list" in url:
        await ctx.send("This command is for queuing songs, not for a playlist.")     
    if "https://www.youtube.com/watch?v=" not in url:
        await ctx.send("Must be a valid link from YouTube")     
    server_id = ctx.guild.id  
    if not server_id in queues:
        queues[server_id] = []
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download = False)
        queues[server_id].append([info.get("id", None), info.get("title", None)])
        print(queues)
        
def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the first url
            m_url = self.music_queue[0][0]['source']

            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False

@client.command()
async def play(ctx):
    voice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    server_id = ctx.guild.id
    if voice.is_playing():
        await ctx.send("Song's already playing stop the song first.")
    if server_id not in queues:
        await ctx.send("There's no song in the queue ") 
    for i in queues[server_id]:
        YDL_OPTIONS = {'format': 'bestaudio/best', 
                            'postprocessors': [{
                                    'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3',
                                    'preferredquality': '192',
                                }],
                            'outtmpl': f"./queue/{server_id}/" + 'song',
                    } 
    await ctx.send("Now playing: "+ i[1])
    if len(queues[server_id]) > 0:
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            ydl.download([f"https://www.youtube.com/watch?v={i[0]}"])
            source = discord.FFmpegOpusAudio(f"./queue/{server_id}/song.mp3")
            queues[server_id].pop(0)
            ctx.voice_client.play((source), after = lambda e: play(ctx))
    else:
        del queues[server_id]
        await ctx.send("No song left in the queue")
            