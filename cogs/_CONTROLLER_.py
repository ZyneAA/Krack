import wavelink


CONTROLLERS = {}

class Controller:

    def __init__(self, bot):
        
        # General
        self.bot = bot
        self.timeout = 30

        # Queue related
        self.queue = wavelink.Queue()
        self.queue_no = 0
        self.playing = False
        
        # Playlist related
        self.playing_p = False
        self.current_song_in_p = None
        self.loop = False
        self.playlists = {}
        
        # Steam 