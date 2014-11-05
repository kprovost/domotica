#!/usr/bin/python

###
# Domotica monitoring daemon.
# responsible for all features which require regular polling of the PLC (i.e.
# everything we can't do from the web interface)
###

import daemon
import optparse
import time

import s7
import domotica.settings as settings

from pollers import AlarmPoller

POLL_INTERVAL = 5

def poll(s7conn, pollers):
    for poller in pollers:
        poller.poll(s7conn)

def main():
    parser = optparse.OptionParser()
    parser.add_option("-f", "--foreground", action="store_true",
            dest="foreground", help="Do not daemonize", default=False)
    (options, args) = parser.parse_args()

    if not options.foreground:
        d = daemon.DaemonContext(prevent_core=False)
        d.open()

    pollers = [
            AlarmPoller()
        ]
    s7conn = s7.S7Comm(settings.PLC_IP)
    while True:
        poll(s7conn, pollers)
        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
