import domotica.alarm
import domotica.alarm as alarm
from poller import Poller
import s7

class AlarmPoller(Poller):
    def __init__(self):
        self._detection = False

    def poll(self, s7conn):
        a = alarm.Alarm(s7conn)

        if a.isArmed():
            print "Alarm armed!"
        else:
            print "Alarm not armed"
            return

        if a.isAlarmTriggered():
            print "Alarm triggered too!"
