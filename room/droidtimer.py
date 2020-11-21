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


droidtime = str(datetime.utcnow()).split()[1].split('.')[0]

def hello():
   delete = rm.get(find.timer == droidtime)
   numba1 = delete.split(':')[1]
   numba2 = droidtime.split(':')[1]
   if int(numba1) >= int(numba2):
      print('delete')
   else:
    print('')
       

      
rt = RepeatedTimer(0.1, hello)


