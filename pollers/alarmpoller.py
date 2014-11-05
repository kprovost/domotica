import domotica.alarm
import domotica.alarm as alarm
from poller import Poller
import s7

class AlarmPoller(Poller):
    def __init__(self):
        self._detection = False

    def poll(self, s7conn):
        print "Poll alarm"
