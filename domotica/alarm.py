import s7

class Alarm:
    ALARM_DB = 12

    def __init__(self, s7conn):
        self._s7conn = s7conn

    def arm(self):
        # Toggle bit
        self._s7conn.writeBit(self.ALARM_DB, 0, 1, 1)
        self._s7conn.writeBit(self.ALARM_DB, 0, 1, 0)

    def disarm(self):
        # Toggle bit
        self._s7conn.writeBit(self.ALARM_DB, 0, 2, 1)
        self._s7conn.writeBit(self.ALARM_DB, 0, 2, 0)

    def isArmed(self):
        return self._s7conn.readFlagBit(5, 2)

    def isAlarmTriggered(self):
        return self._s7conn.readFlagBit(5, 3)
