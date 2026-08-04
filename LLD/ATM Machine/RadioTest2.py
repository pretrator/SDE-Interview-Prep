from enum import Enum

class RadioState(Enum):
    PLAYING = "PLAYING"
    STOPPED = "STOPPED"
    PAUSED = "PAUSED"

class Radio():
    def __init__(self):
        self.state = RadioState.STOPPED

    def play(self):
        pass

    def pause(self):
        pass

    def stop(self):
        pass

