import discord, wavelink
from discord.ext import commands, tasks

from cogs.music import utility


class InactivityTimeout:

    def __init__(self, player, timeout_minutes=5):

        self.player = player
        self.timeout_minutes = timeout_minutes
        self.check_inactivity.start()


    @tasks.loop(minutes=1)
    async def check_inactivity(self):

        for guild in utility.QUEUES.keys():

            if isinstance(self.player, wavelink.player) and not utility.QUEUES[self.player.guild].playing == True and self.player.is_connected():
                if player.inactivity_time >= self.timeout_minutes * 60:
                    await player.disconnect()
                    channel = self.bot.get_channel(player.channel_id)
                    if channel:
                        await channel.send("Disconnected due to inactivity")


    def start(self):
        self.check_inactivity.start()


    def stop(self):
        self.check_inactivity.stop()
