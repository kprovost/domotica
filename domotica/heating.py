import s7

class Heating:
    HEATING_DB = 10
    HEATING_SETPOINT = 6
    HEATING_CURRENT = 4

    def __init__(self, s7conn):
        self._s7conn = s7conn

    def getSetPoint(self):
        return self._s7conn.readInt16(self.HEATING_DB, self.HEATING_SETPOINT) / 10

    def getCurrent(self):
        return self._s7conn.readInt16(self.HEATING_DB, self.HEATING_CURRENT) / 10

    def isModeAuto(self):
        return self._s7conn.readFlagBit(2, 4)

    def isForcedOn(self):
        return self._s7conn.readFlagBit(2, 3)

    def isOn(self):
        #return self._s7conn.readOutput(4, 4)
        return False
