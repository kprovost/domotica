import s7

class PowerPlug:
    POWER_DB = 12
    POWER_WORD = 0

    def __init__(self, ID, name, bit, s7conn):
        self._id = ID
        self._name = name
        self._bit = bit
        self._s7conn = s7conn

    def getID(self):
        return self._id

    def getName(self):
        return self._name

    def isOn(self):
        return self._s7conn.readBit(self.POWER_DB, self.POWER_WORD, self._bit)

    def togglePower(self):
        val = 1
        if self.isOn():
            val = 0
        self._s7conn.writeBit(self.POWER_DB, self.POWER_WORD, self._bit, val)

def getPlugs(s7conn):
    plugs = [
        PowerPlug(0, "Keuken 1", 6, s7conn),
        PowerPlug(1, "Keuken 2", 7, s7conn)
        ]
    return plugs

def getPlug(ID, s7conn):
    plugs = getPlugs(s7conn)

    for plug in plugs:
        if plug.getID() == ID:
            return plug
    
    return None
