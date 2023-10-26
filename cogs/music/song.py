import yt_dlp as youtube_dl

from cogs.music.music_embed import Button

class Song:
    def __init__(self, url):
        self.url = url
        self.duration = None
        self.title = None
        self.uploader = None
        self.upload_date = None
        self.thumbnail = None
        self.get_info()
        self.song_info = Button(self.url, self.duration, self.title, self.uploader, self.upload_date, self.thumbnail).jalan()

    def get_info(self):
        YDL_OPTIONS ={'format': 'bestaudio/best', 
                            'postprocessors': [{
                                   'key': 'FFmpegExtractAudio',
                                    'preferredcodec': 'mp3',
                                    'preferredquality': '192',
                                }]
                        }
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(self.url, download = False)
            self.duration = info.get('duration')
            self.title = info.get('title')
            self.uploader = info.get('uploader')
            self.upload_date = info.get('upload_date')
            self.thumbnail = info.get('thumbnail')
            self.url = info['url']
