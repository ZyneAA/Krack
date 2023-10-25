import discord

from discord.ui import Button
import yt_dlp as youtube_dl

class Button(discord.ui.View):
    def __init__(self, url):
        super().__init__()
        self.url = url

    def jalan(self):
        YDL_OPTIONS = {'format': 'bestaudio/best'}
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(self.url, download = False)
            embed = discord.Embed(title = info.get('title'), description = info.get('uploader'), colour = discord.Colour.random())
            # embed.set_image(url = info.get('thumbnail')) # Thumbnail 
        return embed
