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

    async def next_song(self, error):
        self.queue.next()
        next_song = self.queue.play_list[0]
        self.current_song = None
        if next_song is None:
            return
        coro = await self.play()
        await self.client.loop.create_task(coro)
    #self.voice.play(source,  after = lambda e: self.next_song(e))

    async def play(self):  
        if self.queue.play_list == None:
            return
        self.current_song = self.queue.play_list[0]
        print(self.current_song.url)
        source = discord.FFmpegPCMAudio(self.current_song.url)
        self.voice.play(source, after=lambda e : self.next_song(e))



            # while self.voice.is_playing():
            #     await asyncio.sleep(1)
            #     if not self.voice.is_playing():
            #         print("next one")
            #         self.queue.next()
            # if not self.voice.is_playing():
            #     self.queue.next()
