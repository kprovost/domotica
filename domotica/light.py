import lightconf
import s7

class Light:
    def __init__(self, name, id, s7conn):
        self._name = name
        self._id = id
        self._s7conn = s7conn

        self.STATUS_DB = 12
        self.TIMEOUT_DB = 15

        self.TOGGLE_BIT = 5          # write only
        self.STATUS_BIT = 6          # read only
        self.MOTION_TRIGGER_BIT = 7  # read/write
        self.BLINK_ON_MOTION_BIT = 8 # read/write

    def getName(self):
        return self._name

    def getID(self):
        return self._id

    def isOn(self):
        return self._s7conn.readBit(self.STATUS_DB, self._id, self.STATUS_BIT)

    def getTimeout(self):
        return 10

    def toggle(self):
        return False

def loadAll(s7conn):
    lights = [ ]
    for name, id in lightconf.lights:
        l = Light(name, id, s7conn)
        lights.append(l)
    return lights

