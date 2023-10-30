import wavelink

class Controller:

    def __init__(self, bot):
        
        # General
        self.bot = bot
        self.timeout = 30

        # Queue reloated
        self.queue = wavelink.Queue()
        self.queue_no = 0
        self.playing = False
        