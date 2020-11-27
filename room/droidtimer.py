from tinydb import TinyDB, Query
from datetime import datetime
from threading import Timer
from time import sleep

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

rm = TinyDB('room.json')
find = Query()
data = rm.all()


start_timep = str(datetime.utcnow()).split()[1].split('.')[0].split(':')[1]
start_time = 49
if int(start_time) + 11 >= 60:
    end_time = int(start_time) + 11 - 60
else:
    end_time = int(start_time) + 11
print(end_time)
   
       

      
# rt = RepeatedTimer(1, hello)


