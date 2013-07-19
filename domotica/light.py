import lightconf

class Light:
    def __init__(self, name, id):
        self._name = name
        self._id = id

    def getName(self):
        return self._name

    def isOn(self):
        return (self._id / 2) % 2 == 0

    def getTimeout(self):
        return 10

def loadAll():
    lights = [ ]
    for name, id in lightconf.lights:
        l = Light(name, id)
        lights.append(l)
    return lights

