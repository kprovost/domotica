import lightconf
import s7

class Light:
    STATUS_DB = 12
    TIMEOUT_DB = 15

    TOGGLE_LIGHT_BIT = 5    # write only
    STATUS_BIT = 6          # read only
    MOTION_TRIGGER_BIT = 7  # read/write
    BLINK_ON_MOTION_BIT = 8 # read/write

    def __init__(self, name, id, s7conn):
        self._name = name
        self._id = id
        self._s7conn = s7conn

    def getName(self):
        return self._name

    def getID(self):
        return self._id

    def isOn(self):
        return self._s7conn.readBit(self.STATUS_DB, self._id, self.STATUS_BIT)

    def isActivatedByMotion(self):
        return self._s7conn.readBit(self.STATUS_DB, self._id, self.MOTION_TRIGGER_BIT)

    def blinkOnAlarm(self):
        return self._s7conn.readBit(self.STATUS_DB, self._id, self.BLINK_ON_MOTION_BIT)

    def getTimeout(self):
        return 10

    def toggleLight(self):
        self._s7conn.writeBit(self.STATUS_DB, self._id, self.TOGGLE_LIGHT_BIT, 1)
        self._s7conn.writeBit(self.STATUS_DB, self._id, self.TOGGLE_LIGHT_BIT, 0)
        return True

    def toggleMotion(self):
        val = 0
        if self.isActivatedByMotion():
            val = 1
        #return self._s7conn.writeBit(self.STATUS_DB, self._id, self.MOTION_TRIGGER_BIT, val)
        return False

    def toggleBlinkOnAlarm(self):
        val = 0
        if self.blinkOnAlarm():
            val = 1
        #return self._s7conn.writeBit(self.STATUS_DB, self._id, self.BLINK_ON_MOTION_BIT, val)
        return False

def AllOff(s7conn):
    s7conn.writeBit(Light.STATUS_DB, 0, 0, 1)
    return s7conn.writeBit(Light.STATUS_DB, 0, 0, 0)

def loadGroupNames():
    groupNames = []
    for group in lightconf.groups:
        groupNames.append(group.getName())
    return groupNames

def loadGroup(s7conn, groupName):
    for group in lightconf.groups:
        if group.getName() != groupName:
            continue

        lights = []
        for name, id in group.getLights():
            l = Light(name, id, s7conn)
            lights.append(l)
        return lights

    return None

def loadByID(s7conn, searchId):
    for group in lightconf.groups:
        res = group.getLightByID(searchId)
        if res is None:
            continue
        return Light(res[0], res[1], s7conn)
    return None
