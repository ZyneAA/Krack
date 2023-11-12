import discord, wavelink
from datetime import datetime

from discord.ui import Button
import yt_dlp as youtube_dl

class Button(discord.ui.View):

    def __init__(self, url = None, duration = None, title = None, uploader = None, image = None, queue_no = None):
        super().__init__()

        self.url = url
        self.duration = duration
        self.uploader = uploader
        self.title = title
        self.image = image
        self.queue_no = queue_no


    def jalan(self):

        embed = discord.Embed(title = f"🎶{self.title}🎶", description = f"💿 Now Playing | Queue : {self.queue_no} 💿", type='rich', url = self.url, colour = discord.Colour.random())
        embed.add_field(name = f"☁️ Uploader : {self.uploader} ☁️", value = " ", inline = False)
        embed.add_field(name = f"🕘 Duration : {self.duration} 🕘", value = " ", inline = False)
        embed.set_thumbnail(url = self.image)

        return embed
    
    
    def jalone(self):

        embed = discord.Embed(title = f"🎶{self.title}🎶", description = f" 📥 Added To The Queue | Queue : {self.queue_no} 📥", type='rich', url = self.url, colour = discord.Colour.random())
        embed.add_field(name = f"☁️ Uploader : {self.uploader} ☁️", value = " ", inline = False)
        embed.add_field(name = f"🕘 Duration : {self.duration} 🕘", value = " ", inline = False)
        embed.set_thumbnail(url = self.image)

        return embed
    
    def jalwan(self):

        embed = discord.Embed(title = f"🎶{self.title}🎶", description = f" Select a Playlist", type='rich', url = self.url, colour = discord.Colour.random())
        embed.add_field(name = f"☁️ Uploader : {self.uploader} ☁️", value = " ", inline = False)
        embed.add_field(name = f"🕘 Duration : {self.duration} 🕘", value = " ", inline = False)
        embed.set_thumbnail(url = self.image)

        return embed
