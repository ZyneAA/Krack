import wavelink

class Controller:

    def __init__(self, bot):
        
        self.bot = bot
        self.queue = wavelink.Queue()
        self.queue_no = 0
        self.playing = False
        self.timeout = 30