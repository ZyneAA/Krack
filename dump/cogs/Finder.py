import os, asyncio, discord, json, requests, sqlite3, csv, re
from discord.ext import commands, tasks

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
    async def lee(self, ctx, *, querry):
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

    #Loading data from the database
    # async def add(self):
    #     for i in self.data:
    #         await asyncio.sleep(1)
    #         yield i[0]   
    # async def send_task(self):
    #     async for i in self.add():
    #         await asyncio.sleep(1)
    #         print(i)
        
    # @commands.command()
    # async def s(self, ctx, *, querry):
    #     a = []
    #     pattern = re.compile(querry, re.IGNORECASE)
    #     with open("./file.csv", "r") as f:
    #         reader = csv.reader(f)    
    #         for i in reader:  
    #             a.append(i)
    #     await ctx.send(a[0])
                  
async def setup(client):
    await client.add_cog(Finder(client))