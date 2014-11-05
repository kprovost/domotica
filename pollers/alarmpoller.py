import domotica.alarm
import domotica.alarm as alarm
import logging
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
        logging.debug("Alarm armed status: %s" % isArmed)

        if self._wasArmed != isArmed:
            if isArmed:
                logging.info("Alarm activated")
            else:
                logging.info("Alarm deactivated")

        if not isArmed:
            return

        isTriggered = a.isAlarmTriggered()
        if self._wasTriggered is None:
            self._wasTriggered = isTriggered
        logging.debug("Alarm trigger status: %s" % isTriggered)

        if isTriggered and self._wasTriggered != isTriggered:
            logging.warn("Alarm triggered")
            # Notify
            pass
