import discord, wavelink, asyncio
from discord.ext import commands

# from cogs.music.queue import Play_List
from cogs.music import utility
from cogs.music import music_embed


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

        if str(payload.event) == "END" or utility.QUEUES[payload.player.guild].playing == True:

            if len(utility.QUEUES[payload.player.guild].queue) == 1:
                del utility.QUEUES[payload.player.guild].queue[0]
                utility.QUEUES[payload.player.guild].queue_no = 0
                utility.QUEUES[payload.player.guild].playing = False

                # Timeout for the bot
                while True:

                    if utility.QUEUES[payload.player.guild].playing == False:
                        await asyncio.sleep(1)
                        time += 1
                    if time == utility.QUEUES[payload.player.guild].timeout:
                        await payload.player.disconnect()
                    if utility.QUEUES[payload.player.guild].playing == True:
                        break
                    
                return

            if utility.QUEUES[payload.player.guild].queue != None:
                del utility.QUEUES[payload.player.guild].queue[0]
                utility.QUEUES[payload.player.guild].queue_no -= 1
                next_one: wavelink.YouTubeMusicTrack = utility.QUEUES[payload.player.guild].queue[0]
                await payload.player.play(next_one)
            else:
                pass

        print("Something has stopped playing")


    @commands.command()
    async def play(self, ctx: commands.Context, *, search: str = '') -> None:

        guild = ctx.guild

        if len(utility.QUEUES[guild].queue) == 0 and search == "":
            pass
        else:
            if not ctx.voice_client:
                vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            else:
                vc: wavelink.Player = ctx.voice_client
        
        if search == '':

            if utility.QUEUES[guild].playing == True:
                sender = discord.Embed(color = discord.Color.red(), title = "Opps", description = "Already playing a song") 
                await ctx.send(embed = sender)
                return

            if len(utility.QUEUES[guild].queue) == 0:
                sender = discord.Embed(color = discord.Color.red(), title = "Opps", description = "No song in the queue") 
                await ctx.send(embed = sender)    #ADD EMBED HERE
                return
            else:
                track: wavelink.YouTubeTrack = utility.QUEUES[guild].queue[0]
                utility.QUEUES[guild].playing = True

                duration = self.mak_duraion(track.length)
                image = await track.fetch_thumbnail()
                embed = music_embed.Button(track.uri ,duration, track.title, track.author, image, utility.QUEUES[guild].queue_no)
                await ctx.send(embed = embed.jalan())

                await vc.play(track)

            return

        tracks: list[wavelink.YouTubeTrack] = await wavelink.YouTubeTrack.search(search)
        if not tracks:
            sender = discord.Embed(color = discord.Color.red(), title = "Opps", description = f'Sorry I could not find any songs with search: `{search}`') 
            await ctx.send(embed = sender)
            return

        track: wavelink.YouTubeTrack = tracks[0]
        utility.QUEUES[guild].queue_no += 1
        utility.QUEUES[guild].queue.put(track)

        duration = self.mak_duraion(track.length)
        image = await track.fetch_thumbnail()
        embed = music_embed.Button(track.uri ,duration, track.title, track.author, image, utility.QUEUES[guild].queue_no)
        
        if utility.QUEUES[guild].playing == False:
            await ctx.send(embed = embed.jalan())
            await vc.play(utility.QUEUES[guild].queue[0])
            utility.QUEUES[guild].playing = True
            return
        else:
            await ctx.send(embed = embed.jalone())
            return


    def mak_duraion(self, length):
        seconds = length / 1000
        minutes = seconds // 60
        remaining_seconds = seconds % 60
        return f"{int(minutes)}:{int(remaining_seconds)}"


    @commands.command()
    async def queue(self, ctx: commands.Context, *, search: str):

        guild = ctx.guild
        tracks: list[wavelink.YouTubeTrack] = await wavelink.YouTubeTrack.search(search)

        if  utility.QUEUES[guild].queue == None :
            play_list = wavelink.Queue()
            play_list.put(tracks[0])
            utility.QUEUES[guild].queue = play_list
        else:
            utility.QUEUES[guild].queue.put(tracks[0])

        utility.QUEUES[guild].queue_no += 1
        await ctx.send(utility.QUEUES[guild].queue)

        da_track =  utility.QUEUES[guild].queue[-1]
        duration = self.mak_duraion(da_track.length)
        image = await da_track.fetch_thumbnail()
        embed = music_embed.Button(da_track.uri ,duration, da_track.title, da_track.author, image, utility.QUEUES[guild].queue_no)
        
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


async def setup(client):

    await client.add_cog(Music(client))
