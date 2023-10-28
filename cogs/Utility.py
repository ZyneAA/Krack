import os, asyncio, discord, json, requests, sqlite3, csv, re
from discord.ext import commands, tasks
from discord.utils import get

class Utility(commands.Cog):
    
    def __inint__(self, bot):
        self.bot = bot
    

    @commands.Cog.listener()
    async def on_ready(self):
        
        print("Initialized -----'Utility'-----")


    @commands.command()
    async def clear(self, ctx, amount = 1):

        await ctx.channel.purge(limit = amount + 1)
        

    @commands.command()
    async def to(self, ctx, *, mode):

        if mode == "me":
            await ctx.author.send("Hi!")
        elif mode == "":
            await ctx.send("Hi!")


    @commands.command()
    async def show_steam_region(self, ctx):

        embed = discord.Embed(title = "Here are some region codes\n\nUS: United States\nAR: Argentina\nGB: United Kingdom\nAU: Australia\nDE: Germany\nFR: France\nJP: Japan\nKR: South Korea\n\nIf you know more you can always use them to find games.")
        await ctx.send(embed = embed)


async def setup(bot):
    await bot.add_cog(Utility(bot))
