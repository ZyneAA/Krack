import discord
from datetime import datetime

from discord.ui import Button
import yt_dlp as youtube_dl

class Button(discord.ui.View):
    def __init__(self, url, duration, title, uploader, upload_date, thumbnail):
        super().__init__()
        self.url = url
        self.thumbnail = thumbnail
        self.duration = duration
        self.uploader = uploader
        self.upload_date = upload_date
        self.title = title

    def jalan(self):
        embed = discord.Embed(title = self.title, description = "", colour = discord.Colour.random())
        embed.set_thumbnail(url = self.thumbnail)
        embed.add_field(name = self.uploader, value = " ", inline = False)
        embed.add_field(name = f'Upload Date : {datetime.strptime(self.upload_date, "%Y%m%d").strftime("%B-%d-%Y")}', value = " ",  inline = False)
        return embed
