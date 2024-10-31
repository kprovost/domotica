import domotica.lightconf
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
        self._currentTimeout = None

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
        if self._currentTimeout is None:
            self._currentTimeout = self._s7conn.readUInt16(self.TIMEOUT_DB, self._id)
        return self._currentTimeout

    def setTimeout(self, timeout):
        if timeout < 0 or timeout > 9990:
            raise "Invalid timeout"
        self._currentTimeout = timeout
        return self._s7conn.writeUInt16(self.TIMEOUT_DB, self._id, timeout)

    def getPossibleTimeouts(self):
        values = [ ]
        for i in range(0, 9990, 30):
            if (i < 60):
                pretty = "%s s" % i
            else:
                pretty = "%s m %s s" % (i / 60, i % 60)

            isSelected = (i == self.getTimeout())
            values.append((pretty, i, isSelected))
        return values

    def toggleLight(self):
        self._s7conn.writeBit(self.STATUS_DB, self._id, self.TOGGLE_LIGHT_BIT, 1)
        self._s7conn.writeBit(self.STATUS_DB, self._id, self.TOGGLE_LIGHT_BIT, 0)
        return True

    def toggleMotion(self):
        val = 1
        if self.isActivatedByMotion():
            val = 0
        self._s7conn.writeBit(self.STATUS_DB, self._id, self.MOTION_TRIGGER_BIT, val)
        return True

    def toggleBlinkOnAlarm(self):
        val = 1
        if self.blinkOnAlarm():
            val = 0
        self._s7conn.writeBit(self.STATUS_DB, self._id, self.BLINK_ON_MOTION_BIT, val)
        return True

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
