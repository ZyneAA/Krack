import discord, os, asyncio
from pathlib import Path
from discord.ext import commands
from discord.message import Message

class Krack(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix = ">", case_insensitive = True, intents = discord.Intents.all())

    def setup(self):
        cogs = [p.stem for p in Path(".").glob("./cogs/*.py")]
        print(cogs)
        for cog in cogs:
            self.load_extension(f"bot.cogs.{cog}")
            print(f" Loaded `{cog}` cog.")
        print("Krack is awaking.......")

    def run(self):
        self.setup()
        with open("TOKEN", "r") as token:
            super().run("MTE2MTk0MDY0MjEwOTMzNzY0MQ.GGd3zz.th3ySOCFKVDRpT_DhfPCHj6DsbFGFwGtS5iUTI", reconnect = True)

    async def on_ready(self):
        self.client_id = (await self.application_info()).id
        print("Krack is ready.")

    async def process_commands(self, msg: Message):
        ctx = await self.get_context(msg, cls = commands.Context)

        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_message(self, msg):
        if not msg.author.bot:
            await self.process_commands(msg)   
    
def main():
    bot = Krack() 
    bot.setup()  
    bot.run()

if __name__ == "__main__":
    main()