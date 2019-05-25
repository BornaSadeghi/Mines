import time

class Timer:
    def __init__(self):
        self.seconds = 0
        self.startTime = time.time()
        self.paused = True
    def getTime(self):
        return self.seconds
    def update(self): # gets time since timer was started
        if not self.paused:
            self.seconds = time.time() - self.startTime
        else:
            self.startTime = time.time() - self.seconds
    def togglePause(self):
        self.paused = not self.paused 
    def pause(self):
        self.paused = True
    def unpause(self):
        self.paused = False
    def stop(self):
        self.paused = True
        self.startTime = time.time()
        self.seconds = 0