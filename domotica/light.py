from django.conf import settings
import s7

class Light:
    def __init__(self, name, merker, do, s7conn):
        self._name = name
        self._merker = merker
        self._do = do
        self._s7conn = s7conn
        self._currentTimeout = None

    def getName(self):
        return self._name

    def getID(self):
        return self._merker

    def isOn(self):
        return self._s7conn.readOutput(0, self._do)

    def toggleLight(self):
        self._s7conn.writeFlagBit(0, self._merker, 1)
        self._s7conn.writeFlagBit(0, self._merker, 0)
        return True

def AllOn(s7conn):
    s7conn.writeFlagBit(0, settings.LIGHTS_ALL_ON, 1)
    s7conn.writeFlagBit(0, settings.LIGHTS_ALL_ON, 0)
    return True

def AllOff(s7conn):
    s7conn.writeFlagBit(0, settings.LIGHTS_ALL_OFF, 1)
    s7conn.writeFlagBit(0, settings.LIGHTS_ALL_OFF, 0)
    return True
