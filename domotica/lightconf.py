
class LightGroup:
    def __init__(self, name, lights):
        self._name = name
        self._lights = lights

    def getName(self):
        return self._name

    def getLights(self):
        return self._lights

    def getLightByID(self, searchId):
        for name, id in self._lights:
            if id == searchId:
                return (name, id)
        return None

groups = [
        LightGroup("Keuken",
            [
                ( "Bijkeuken", 2 ),
                ( "Keuken", 4 ),
                ( "Werkblad keuken", 36 ),
                ( "Douche gelijkvoers", 24 ),
                ( "Achterdeur keuken", 50 ),
                ( "Berging", 28 ),
            ]),
        LightGroup("Hal",
            [
                ( "Inkomhal 1", 14 ),
                ( "Inkomhal 2", 16 ),
                ( "Inkomhal 3", 18 ),
                ( "Vestiaire", 20 ),
                ( "Overloop 1ste", 30 ),
                ( "Wachthal 1ste", 42 ),
                ( "Overloop 2de", 56 ),
            ]),
        LightGroup("Living",
            [
                ( "Zithoek", 22 ),
                ( "Wand eetplaats 1", 6 ),
                ( "Wand eetplaats 2", 8 ),
                ( "Plafond eetplaats 1", 10 ),
                ( "Plafond eetplaats 2", 12 ),
                ( "Terras gelijkvloers", 52 ),
            ]),
        LightGroup("Slaapkamers",
            [
                ( "Slaapkamer 1", 38 ),
                ( "Slaapkamer 2", 40 ),
                ( "Slaapkamer 3", 46 ),
                ( "Badkamer 2de", 62 ),
                ( "Dakterras", 54 ),
                ( "Dressing", 48 ),
            ]),
        LightGroup("Badkamer",
            [
                ( "Plafond badkamer 1ste", 58 ),
                ( "Lavabo badkamer 1ste", 60 ),
            ]),
        LightGroup("Andere",
            [
                ( "WC gelijkvloers", 26 ),
                ( "WC 1ste", 34 ),
                ( "Inrit", 32 ),
                ( "CV lokaal", 44 ),
            ]),
        ]
