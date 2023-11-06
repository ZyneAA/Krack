import discord, wavelink, sqlite3, asyncio
from discord.ext import commands

from cogs.steam import steam
from cogs._CONTROLLER_ import Controller, CONTROLLERS

class Krack(commands.Bot):

    def __init__(self) -> None:

        intents = discord.Intents.all()
        intents.message_content = True

        super().__init__(intents = intents, command_prefix = '>')

    async def on_ready(self) -> None:

        await self.change_presence(status = discord.Status.online, activity = discord.Game("🤡"))

        # Load all cogs
        await self.load_extension("cogs.Finder")
        await self.load_extension("cogs.Music")
        await self.load_extension("cogs.Utility")
        await self.load_extension("cogs.Steam")

        # Registering all the guilds that the bot had joined and get the data from the database
        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        
        for guild in self.guilds:
            
            CONTROLLERS[guild] = Controller(guild)
            
            insert_data = ("INSERT INTO guilds (guild, playlist) "
              "VALUES (?, ?)")
            data = (guild.name, None)
            cursor.execute(insert_data, data)
        con.commit()
        cursor.close()
        con.close()


    async def setup_hook(self) -> None:

        node: wavelink.Node = wavelink.Node(uri='http://localhost:2333', password='youshallnotpass')
        await wavelink.NodePool.connect(client=self, nodes=[node])
 

bot = Krack()

def main():

    with open("TOKEN", "r") as token:
        bot.run(token.read())
        
        
@bot.event
async def on_guild_join(guild):
    
    con = sqlite3.connect('data.db')
    cursor = con.cursor()
    
    CONTROLLERS[guild] = Controller(guild)  
    
    insert_data = ("INSERT INTO guilds (guild, playlist) "
              "VALUES (?, ?)")
    data = (guild.name, None)
    cursor.execute(insert_data, data)
    
    await asyncio.sleep(1)
    
    con.commit()   
    cursor.close() 
    con.close()


@bot.command()
async def reload_cog(ctx):

    await bot.reload_extension("cogs.Finder")
    await bot.reload_extension("cogs.Music")
    await bot.reload_extension("cogs.Utility")
    await bot.reload_extension("cogs.Steam")

    await ctx.send("COGS RELOADED!")

if __name__ == "__main__":
    main()