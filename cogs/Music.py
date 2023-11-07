import discord, wavelink, asyncio
from discord.ext import commands
from discord import app_commands

# from cogs.music.queue import Play_List
from cogs._CONTROLLER_ import CONTROLLERS
from cogs.music import music_embed
from cogs.music import util


class Music(commands.Cog):

    def __init__(self, bot):

        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):

        print("Musci cog is ready")


    @commands.Cog.listener()
    async def on_wavelink_node_ready(node: wavelink.Node) -> None:

        print(f"Node {node.id} is ready!")


    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackEventPayload):

        print("Something is playing")


    @commands.Cog.listener()
    async def on_wavelink_track_end(self, payload: wavelink.TrackEventPayload):

        time = 0

        if str(payload.event) == "END" or CONTROLLERS[payload.player.guild].playing == True:

            if len(CONTROLLERS[payload.player.guild].queue) == 1:
                del CONTROLLERS[payload.player.guild].queue[0]
                CONTROLLERS[payload.player.guild].queue_no = 0
                CONTROLLERS[payload.player.guild].playing = False

                # Timeout for the bot
                while True:

                    if CONTROLLERS[payload.player.guild].playing == False:
                        await asyncio.sleep(1)
                        time += 1
                    if time == CONTROLLERS[payload.player.guild].timeout:
                        await payload.player.disconnect()
                    if CONTROLLERS[payload.player.guild].playing == True:
                        break
                    
                return

            if CONTROLLERS[payload.player.guild].queue != None:
                del CONTROLLERS[payload.player.guild].queue[0]
                CONTROLLERS[payload.player.guild].queue_no -= 1
                next_one: wavelink.YouTubeMusicTrack = CONTROLLERS[payload.player.guild].queue[0]
                await payload.player.play(next_one)
            else:
                pass

        print("Something has stopped playing")


    @commands.command()
    async def play(self, ctx: commands.Context, *, search: str = '') -> None:

        guild = ctx.guild

        if len(CONTROLLERS[guild].queue) == 0 and search == "":
            pass
        else:
            if not ctx.voice_client:
                vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            else:
                vc: wavelink.Player = ctx.voice_client
        
        if search == '':

            if CONTROLLERS[guild].playing == True:
                sender = discord.Embed(color = discord.Color.red(), title = "Opps", description = "Already playing a song") 
                await ctx.send(embed = sender)
                return

            if len(CONTROLLERS[guild].queue) == 0:
                sender = discord.Embed(color = discord.Color.red(), title = "Opps", description = "No song in the queue") 
                await ctx.send(embed = sender)    #ADD EMBED HERE
                return
            else:
                track: wavelink.YouTubeTrack = CONTROLLERS[guild].queue[0]
                CONTROLLERS[guild].playing = True

                duration = util.make_duraion(track.length)
                image = await track.fetch_thumbnail()
                embed = music_embed.Button(track.uri ,duration, track.title, track.author, image, CONTROLLERS[guild].queue_no)
                await ctx.send(embed = embed.jalan())

                await vc.play(track)

            return

        tracks: list[wavelink.YouTubeTrack] = await wavelink.YouTubeTrack.search(search)
        if not tracks:
            sender = discord.Embed(color = discord.Color.red(), title = "Opps", description = f'Sorry I could not find any songs with search: `{search}`') 
            await ctx.send(embed = sender)
            return

        track: wavelink.YouTubeTrack = tracks[0]
        CONTROLLERS[guild].queue_no += 1
        CONTROLLERS[guild].queue.put(track)

        duration = util.make_duraion(track.length)
        image = await track.fetch_thumbnail()
        embed = music_embed.Button(track.uri ,duration, track.title, track.author, image, CONTROLLERS[guild].queue_no)
        
        if CONTROLLERS[guild].playing == False:
            await ctx.send(embed = embed.jalan())
            await vc.play(CONTROLLERS[guild].queue[0])
            CONTROLLERS[guild].playing = True
            return
        else:
            await ctx.send(embed = embed.jalone())
            return


    @commands.command()
    async def queue(self, ctx: commands.Context, *, search: str):

        guild = ctx.guild
        tracks: list[wavelink.YouTubeTrack] = await wavelink.YouTubeTrack.search(search)

        if CONTROLLERS[guild].queue == None :
            play_list = wavelink.Queue()
            play_list.put(tracks[0])
            CONTROLLERS[guild].queue = play_list
        else:
            CONTROLLERS[guild].queue.put(tracks[0])

        CONTROLLERS[guild].queue_no += 1
        await ctx.send(CONTROLLERS[guild].queue)

        da_track =  CONTROLLERS[guild].queue[-1]
        duration = util.make_duraion(da_track.length)
        image = await da_track.fetch_thumbnail()
        embed = music_embed.Button(da_track.uri ,duration, da_track.title, da_track.author, image, CONTROLLERS[guild].queue_no)
        
        await ctx.send(f"{tracks[0]} was added to the queue.", embed = embed.jalone())


    @commands.command()
    async def pause(self, ctx: commands.Context) -> None:

        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)
        await player.pause()


    @commands.command()
    async def stop(self, ctx: commands.Context) -> None:

        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)
        await player.stop()


    @commands.command()
    async def resume(self, ctx: commands.Context) -> None:

        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)
        await player.resume()


    @commands.command()
    async def skip(self, ctx: commands.Context) -> None:

        guild = ctx.guild

        if len(CONTROLLERS[guild].queue) == 0:
            sender = discord.Embed(color = discord.Color.red(), title = "Opps", description = "No song in the queue") 
            await ctx.send(embed = sender)

        node = wavelink.NodePool.get_node()
        player = node.get_player(guild.id)

        if CONTROLLERS[guild].playing == False:
            pass
        else:
            await player.stop()

        if len(CONTROLLERS[guild].queue) > 0:
            del CONTROLLERS[guild].queue[0]
            song: wavelink.YouTubeMusicTrack = CONTROLLERS[guild].queue[0]
            await player.play(song)
            return
        
        return    

    
    @commands.command()
    async def shuffle(self, ctx: commands.Context) -> None:

        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)
        await player.stop()
        await CONTROLLERS[ctx.guild].queue.shuffle()
        
    
    @commands.command()
    async def clear_queue(self, ctx: commands.Context) -> None:
        
        guild = ctx.guild
        
        if len(CONTROLLERS[guild].queue) == 0:
            await ctx.send("No song in the queue to clear.")
            return
        
        CONTROLLERS[guild].queue.clear()
        await ctx.send("All songs in the queue are cleared.")
        
    
    @commands.command()
    async def show_queue(self, ctx: commands.Context) -> None:

        guild = ctx.guild

        count = 1
        sar = ""
        embed = discord.Embed(title = "Songs that are currently in the queue :", color = discord.Color.random())

        for i in CONTROLLERS[guild].queue:
            sar += f"{count} : {i}\n"
            embed.add_field(name = f"{sar}", value = "", inline = False)
            sar = ""
            count +=1
    
        print(CONTROLLERS[guild].queue)
        await ctx.send(embed = embed)


    @commands.command(name = "Disconnect", aliases = ["leave"])
    async def leave(self, ctx: commands.Context) -> None:

        if not ctx.voice_client:
            await ctx.send("Not in  a voice channel")

        vc: wavelink.Player = ctx.voice_client
        await vc.disconnect()
        

    @commands.command()
    async def vol(self, ctx: commands.Context, *, vol) -> None:

        node = wavelink.NodePool.get_node()
        player = node.get_player(ctx.guild.id)
        await player.set_volume(int(vol))


    @commands.command()
    async def join(self, ctx: commands.Context, *, channel: discord.VoiceChannel | None = None):

        try:
            channel = channel or ctx.author.voice.channel
        except AttributeError:
            return await ctx.send('No voice channel to connect to. Please either provide one or join one.')
        
        vc: wavelink.Player = await channel.connect(cls=wavelink.Player)
        return vc
    

    @app_commands.command(name = "changed", description = "Add a song to a playlist")
    async def func(self, interaction: discord.Interaction, song_name: str, playlist: str):

        await interaction.response.send_message("ff")

async def setup(client):

    await client.add_cog(Music(client))
