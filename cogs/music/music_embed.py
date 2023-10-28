import discord, wavelink
from datetime import datetime

from discord.ui import Button
import yt_dlp as youtube_dl

class Button(discord.ui.View):

    def __init__(self, url, duration, title, uploader, image):
        super().__init__()

        self.url = url
        self.duration = duration
        self.uploader = uploader
        self.title = title
        self.image = image


    def jalan(self):

        embed = discord.Embed(title = f"🎶{self.title}🎶", description = "💿 Now Playing 💿", type='rich', url = self.url, colour = discord.Colour.random())
        embed.add_field(name = f"☁️ Uploader : {self.uploader} ☁️", value = " ", inline = False)
        embed.add_field(name = f"🕘 Duration : {self.duration} 🕘", value = " ", inline = False)
        embed.set_thumbnail(url = self.image)

        return embed
    
    
    def jalone(self):

        embed = discord.Embed(title = f"🎶{self.title}🎶", description = " 📥 Added To The Queue 📥", type='rich', url = self.url, colour = discord.Colour.random())
        embed.add_field(name = f"☁️ Uploader : {self.uploader} ☁️", value = " ", inline = False)
        embed.add_field(name = f"🕘 Duration : {self.duration} 🕘", value = " ", inline = False)
        embed.set_thumbnail(url = self.image)

        return embed
