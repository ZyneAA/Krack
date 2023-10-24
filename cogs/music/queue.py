from collections import deque
import random

from cogs import config

class Play_List:
    def __init__(self):
        self.play_list = deque()
        self.bin = None
        self.loop = False

    def add(self, val):
        if len(self.play_list) >= config.MAXIMUM_QUEUE_SIZE:
            return config.MAXIMU_QUEUE_SIZE_REACHED
        self.play_list.append(val)

    def remove(self):
        if len(self.play_list) < 1:
            return config.MINIMUM_QUEUE_SIZE_REACHED
        self.bin = self.play_list
        self.play_list.pop()

    def recover(self):
        return self.bin

    def shatfel(self):
        random.shuffle(self.play_list)