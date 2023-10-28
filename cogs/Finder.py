import os, asyncio, discord, json, requests, sqlite3, csv, re
from discord.ext import commands, tasks

from cogs.steam import steam_embed

class Finder(commands.Cog):
    
    def __inint__(self, client):

        self.client = client

          
    @commands.Cog.listener()
    async def on_ready(self):

        print("Initialized -----'Finder'-----")

        
    @commands.command()
    async def yt(self, ctx, mode, *, querry):

        if mode == "-s":
            result = "https://www.youtube.com/results?search_query="
            if " " in querry:
                querry = querry.replace(" ","+") 
            await ctx.send(result + querry)

        elif mode == "-f":
            await ctx.send(querry)
        await ctx.send("Must provid a valid commend!")


    @commands.command()
    async def phub(self, ctx, *, querry):

        result = "https://www.pornhub.com/video/search?search="
        await ctx.send("Search contains NSFW contents!\n" + result + querry)


    @commands.command()
    async def twt(self, ctx, *, querry):

        result = "https://www.twitch.tv/search?term="

        if " " in querry:
            querry = querry.replace(" ","+")

        await ctx.send(result + querry)


    @commands.command()
    async def lee(self, ctx, *, querry : None):

        await ctx.send(f"HNZ is HML' son")


    @commands.command()
    async def web(self, ctx, *, querry):

        result = "https://www.google.com/search?q="

        if " " in querry:
            querry = querry.replace(" ","+")

        await ctx.send(result + querry)

   
    @commands.command()
    async def t(self, ctx, *, querry):

        a = ["q", "w", "e", "r"]
        for  i in a:
            if querry == i:
                await ctx.send("T")


    @commands.command()
    async def steam(self, ctx, *, name = ''):
        if name == "":
            await ctx.send("Please Write '/stream game_name'")
            return       
        sar = str(name).upper()
        matching_games = []
        except_terms = ['bundle', 'extension', 'non-game-term']
        matching_id = []
        print(sar)
        with open("./cogs/steam/file.csv", "r", encoding = 'utf-8') as f:
            csvreader = csv.reader(f)
            for row in csvreader:
                list = row[0].strip()
                serial = row[1]
                is_game = re.match(r'^[A-Za-z0-9\s-]+$', list) and not any(term in list.lower() for term in except_terms)
                # Search and match the names from database 
                if is_game and  list.startswith(sar):
                        matching_games.append(list)
                        matching_id.append(serial)

        if matching_games:
                await ctx.send("--Found Games--")
                for game in matching_games:       
                    view = steam_embed.Button(game,row[1],"US")
                    embed = discord.Embed(title = game, description = "Click the button below to get the detail!")  
                    await ctx.send( embed = embed , view = view)
                await ctx.send()
                await ctx.send("-- That Is All --")
        else: 
                await ctx.send("-- Not Found --")  
               

async def setup(client):
    await client.add_cog(Finder(client))