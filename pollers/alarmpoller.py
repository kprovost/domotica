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
        logging.debug("Alarm armed status: %s" % isArmed)

        if self._wasArmed is not None and self._wasArmed != isArmed:
            if isArmed:
                logging.info("Alarm activated")
            else:
                logging.info("Alarm deactivated")
        self._wasArmed = isArmed

        if not isArmed:
            self._wasTriggered = False
            return

        isTriggered = a.isAlarmTriggered()
        logging.debug("Alarm trigger status: %s" % isTriggered)

        if self._wasTriggered is not None and isTriggered \
                and self._wasTriggered != isTriggered:
            logging.warn("Alarm triggered")
            # Notify
        self._wasTriggered = isTriggered
