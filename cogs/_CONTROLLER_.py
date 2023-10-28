import wavelink

class Controller:

    def __init__(self, bot):
        
        self.bot = bot
        self.queue = wavelink.Queue()
