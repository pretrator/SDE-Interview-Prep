from enum import Enum

class RadioState(Enum):
    PLAYING = "PLAYING"
    STOPPED = "STOPPED"
    PAUSED = "PAUSED"

class Radio():
    def __init__(self):
        self.state = RadioState.STOPPED

    def play(self):
        if self.state == RadioState.PLAYING:
            print('already playing')
        if self.state == RadioState.STOPPED:
            self.state = RadioState.PLAYING
            print(' stopped  to Playing')
        if self.state == RadioState.STOPPED:
            self.state = RadioState.PLAYING
            print(' stopped  to Playing')
        

    def pause(self):
        self.state = RadioState.PLAYING

    def stop(self):
        pass

