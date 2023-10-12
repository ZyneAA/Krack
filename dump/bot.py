import discord, asyncio
from discord.ext import commands
import os

#import all of the cogs
from music_cog import music_cog

bot = commands.Bot(command_prefix='$', intents = discord.Intents.all())

#remove the default help command so that we can write out own
bot.remove_command('help')

#register the class with the bot
#await bot.add_cog(music_cog(bot))

async def load():
    await bot.add_cog(music_cog(bot))

asyncio.run(load())

#start the bot with our token
bot.run("MTA3NDMzNzUxMjMyOTMxNDM5NA.GxPluR.9lRMchX9Frvu-4B6fWJfJ1NTtTh6jKYtG0Xo4g")