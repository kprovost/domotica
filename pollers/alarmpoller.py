import domotica.alarm as alarm
import logging
from pollers.poller import Poller
from notifier import sms
from domotica import settings
import s7

class AlarmPoller(Poller):
    def __init__(self):
        self._wasArmed = None
        self._wasTriggered = None

    def onStateChange(self, s7conn, isArmed):
        if isArmed:
            logging.info("Alarm activated")
        else:
            logging.info("Alarm deactivated")

    def onTriggered(self, s7conn):
        msg = "Alarm!"
        logging.warn(msg)
        for dest in settings.SMS_DESTINATIONS:
            if not sms.send(msg, dest):
                logging.error("Failed to send SMS \"%s\" to %s" % (msg, dest))

    def poll(self, s7conn):
        a = alarm.Alarm(s7conn)

        isArmed = a.isArmed()
        logging.debug("Alarm armed status: %s" % isArmed)

        if self._wasArmed is not None and self._wasArmed != isArmed:
            self.onStateChange(s7conn, isArmed)
        self._wasArmed = isArmed

        if not isArmed:
            self._wasTriggered = False
            return

        isTriggered = a.isAlarmTriggered()
        logging.debug("Alarm trigger status: %s" % isTriggered)

        if self._wasTriggered is not None and isTriggered \
                and self._wasTriggered != isTriggered:
            self.onTriggered(s7conn)
        self._wasTriggered = isTriggered
