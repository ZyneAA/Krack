from collections import deque
import random

from cogs import config
from cogs.music.song import Song

class Play_List:
    def __init__(self):
        self.play_list = deque()
        self.bin = None
        self.loop = False

    def add(self, url):
        if len(self.play_list) >= config.MAXIMUM_QUEUE_SIZE:
            return config.MAXIMU_QUEUE_SIZE_REACHED
        self.play_list.append(Song(url))

    def remove(self):
        if len(self.play_list) < 1:
            return config.MINIMUM_QUEUE_SIZE_REACHED
        self.bin = self.play_list[-1]
        self.play_list.pop()

    def next(self):
        if self.play_list == None:
            return
        print("inside next function")
        self.play_list.popleft()

    def recover(self):
        return self.bin

    def shatfel(self):
        random.shuffle(self.play_list)