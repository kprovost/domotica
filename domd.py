#!/usr/bin/python

###
# Domotica monitoring daemon.
# responsible for all features which require regular polling of the PLC (i.e.
# everything we can't do from the web interface)
###

import daemon
import optparse
import time
import logging

import s7
import domotica.settings as settings

from pollers import AlarmPoller

POLL_INTERVAL = 5

def poll(s7conn, pollers):
    for poller in pollers:
        poller.poll(s7conn)

def connect():
    return s7.S7Comm(settings.PLC_IP)

def setup_logger(options):
    lvl = logging.INFO
    if options.debug:
        lvl = logging.DEBUG

    fmt = "%(asctime)s:%(levelname)s:%(module)s:%(message)s"
    logging.basicConfig(level=lvl, format=fmt)

def main():
    parser = optparse.OptionParser()
    parser.add_option("-f", "--foreground", action="store_true",
            dest="foreground", help="Do not daemonize", default=False)
    parser.add_option("-d", "--debug", action="store_true",
            dest="debug", help="Debug logging", default=False)
    (options, args) = parser.parse_args()

    if not options.foreground:
        d = daemon.DaemonContext(prevent_core=False)
        d.open()

    setup_logger(options)

    pollers = [
            AlarmPoller()
        ]

    s7conn = connect()

    while True:
        try:
            poll(s7conn, pollers)
        except s7.S7Exception, e:
            if e.errno() == s7.S7Exception.ERR_CONNECTION_CLOSED:
                logging.warn("Connection lost. Reconnecting...")
                s7conn = connect()
            else:
                logging.error("Unknown error: %s", e)
                raise

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    main()
