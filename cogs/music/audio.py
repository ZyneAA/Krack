import yt_dlp as youtube_dl
import os, asyncio, discord, json, requests, sqlite3, csv, re, ffmpy
from discord import opus
import concurrent.futures

from cogs.music import utility

class Audio:
    def __init__(self, client, queue = None, id = None, voice = None):
        self.client = client
        self.queue = queue
        self.current_song = None
        self.id = id
        self.voice  = voice

    async def next_song(self):
        next_song = self.queue.play_list[0]
        self.current_song = None
        if next_song is None:
            return
        coro = await self.play_song(next_song)

    async def play(self):
        YDL_OPTIONS ={'format': 'bestaudio/best', 
                            'postprocessors': [{
                                   'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3',
                                    'preferredquality': '192',
                                }],
                            'outtmpl': f"./queue/{self.id}/" + 'song',
                        }
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            self.current_song = self.queue.play_list[0]
            ydl.download(self.queue.play_list[0].url)
            self.queue.next()
            source = discord.FFmpegOpusAudio(f"./queue/{self.id}/song.mp3")
            self.voice.play(source,  after = lambda e: self.next_song(e))

    async def plaow(self):
        YDL_OPTIONS ={'format': 'bestaudio/best', 
                            'postprocessors': [{
                                   'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3',
                                    'preferredquality': '192',
                                }],
                            'outtmpl': f"./queue/{self.id}/" + 'song',
                        }
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            for i in self.queue.play_list:
                info = ydl.extract_info(i.url, download = False)
                duration = info.get('duration')
                url = info['url']
                self.current_song = i

                # ydl.download(i.url)
                # source = discord.FFmpegOpusAudio(f"./queue/{self.id}/song.mp3")
                
                source = discord.FFmpegPCMAudio(url)
                self.voice.play(source)
                await asyncio.sleep(float(duration))



# YDL_OPTIONS ={'format': 'bestaudio/best', 
#                             'postprocessors': [{
#                                    'key': 'FFmpegExtractAudio',
#                                     'preferredcodec': 'mp3',
#                                     'preferredquality': '192',
#                                 }],
#                             'outtmpl': f"./queue/{self.id}/" + 'song',
#                         }