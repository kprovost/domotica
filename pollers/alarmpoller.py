import domotica.alarm
import domotica.alarm as alarm
from poller import Poller
import s7

class AlarmPoller(Poller):
    def __init__(self):
        self._wasArmed = None
        self._wasTriggered = None

    def poll(self, s7conn):
        a = alarm.Alarm(s7conn)

        isArmed = a.isArmed()
        if self._wasArmed is None:
            self._wasArmed = isArmed

        if self._wasArmed != isArmed:
            # Log state change
            pass

        if not isArmed:
            return

        isTriggered = a.isAlarmTriggered()
        if self._wasTriggered is None:
            self._wasTriggered = isTriggered

        if isTriggered and self._wasTriggered != isTriggered:
            print "Alarm went off!"
            # Notify
            pass
