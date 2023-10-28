import discord
import wavelink
from discord.ext import commands

from cogs.steam import steam
from cogs.music import utility
from cogs._CONTROLLER_ import Controller

class Krack(commands.Bot):

    def __init__(self) -> None:

        intents = discord.Intents.all()
        intents.message_content = True

        super().__init__(intents = intents, command_prefix = '/')

    async def on_ready(self) -> None:

        await self.change_presence(status = discord.Status.online, activity = discord.Game("🤡"))

        # Load all cogs
        await self.load_extension("cogs.Finder")
        await self.load_extension("cogs.Music")
        await self.load_extension("cogs.Utility")
        await self.load_extension("cogs.Steam")

        # Registering all the guilds that the bot had joined
        for guild in self.guilds:
            utility.QUEUES[guild] = Controller(guild)


    async def setup_hook(self) -> None:

        node: wavelink.Node = wavelink.Node(uri='http://localhost:2333', password='youshallnotpass')
        await wavelink.NodePool.connect(client=self, nodes=[node])
 
bot = Krack()
def main():
    with open("TOKEN", "r") as token:
        bot.run(token.read())

@bot.command()
async def reload_cog(ctx):

    await bot.reload_extension("cogs.Finder")
    await bot.reload_extension("cogs.Music")
    await bot.reload_extension("cogs.Utility")
    await bot.reload_extension("cogs.Steam")

if __name__ == "__main__":
    main()