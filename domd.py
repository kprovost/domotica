#!/usr/bin/python

###
# Domotica monitoring daemon.
# responsible for all features which require regular polling of the PLC (i.e.
# everything we can't do from the web interface)
###

import daemon
import domotica.alarm
import domotica.settings as settings
import domotica.alarm as alarm
import s7

def test():
    a = alarm.Alarm(s7.S7Comm(settings.PLC_IP))

    if a.isArmed():
        print("Alarm armed!")
    if a.isAlarmTriggered():
        print("Alarm triggered too!")

def main():
    d = daemon.DaemonContext(prevent_core=False)
    d.open()

    test()

if __name__ == "__main__":
    main()
