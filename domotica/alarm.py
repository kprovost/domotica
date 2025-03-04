import s7
from django.conf import settings

detectors = [
        #( "Inrit", 32 ),
        #( "Keuken", 4 ),
        #( "Bijkeuken", 2 ),
        #( "Zithoek", 22 ),
        #( "Eethoek", 6 ),
        #( "Inkomhal", 14 )
        ]

class Detector:
    DETECTOR_DB = 12

    ENABLE_BIT = 9
    STATUS_BIT = 10

    def __init__(self, name, id, s7conn):
        self._name = name
        self._id = id
        self._s7conn = s7conn

    def getName(self):
        return self._name

    def getID(self):
        return self._id

    def isEnabled(self):
        return self._s7conn.readBit(self.DETECTOR_DB, self._id, self.ENABLE_BIT)

    def isTriggered(self):
        return self._s7conn.readBit(self.DETECTOR_DB, self._id, self.STATUS_BIT)

    def toggle(self):
        if self.isEnabled():
            bit = 0
        else:
            bit = 1
        self._s7conn.writeBit(self.DETECTOR_DB, self._id, self.ENABLE_BIT, bit)
        return True

class Alarm:
    def __init__(self, s7conn):
        self._s7conn = s7conn

    def arm(self):
        # Toggle bit
        self._s7conn.writeFlagBit(0, settings.ALARM_ON, 1)
        self._s7conn.writeFlagBit(0, settings.ALARM_ON, 0)

    def disarm(self):
        # Toggle bit
        self._s7conn.writeFlagBit(0, settings.ALARM_OFF, 1)
        self._s7conn.writeFlagBit(0, settings.ALARM_OFF, 0)

    def isArmed(self):
        return self._s7conn.readFlagBit(0, settings.ALARM_IS_SET)

    def isWarning(self):
        # Alarm is two state when triggered, the first 'warning' flashes the lights
        # The second stage will trigger the siren and SMS warning.
        return False
   
    def isAlarmTriggered(self):
        return self._s7conn.readFlagBit(0, settings.ALARM_TRIGGERED)

def getDetectors(s7conn):
    l = [ ]
    for name, id in detectors:
        d = Detector(name, id, s7conn)
        l.append(d)
    return l

def getDetectorByID(s7conn, id):
    l = getDetectors(s7conn)
    for d in l:
        if d.getID() == id:
            return d
    return None

