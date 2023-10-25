from cogs.music.music_embed import Button

class Song:
    def __init__(self, url):
        self.url = url
        self.song_info = Button(self.url).jalan()

    def get_info(self):
        pass
