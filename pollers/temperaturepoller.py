import rrdtool
import logging
import os
import tempfile
from PIL import Image
import domotica.heating as heating
from pollers.poller import Poller
import s7

RRD_FILE = "stable_temperature.rrd"


class TemperaturePoller(Poller):

    def __init__(self): # TODO Add poll interval parameter
        if not os.path.exists(RRD_FILE):
            self.create()

    def create(self):
        try:
            rrdtool.create(RRD_FILE,
                    '--no-overwrite',
                    '--step', '5',
                    'DS:temperature:GAUGE:30:-20:100',
                    'RRA:AVERAGE:0.5:1:1440',   # Daily
                    'RRA:AVERAGE:0.5:12:10080', # Weekly,
                    'RRA:AVERAGE:0.5:720:365')  # Yearly
        except Exception as e:
            logging.error("Failed to create file: %s" % e)

    def poll(self, s7conn):
        h = heating.Heating(s7conn)
        temp = h.getCurrent()
        logging.debug("Stable temperature: %0.1f" % temp)
        try:
            rrdtool.update(RRD_FILE, "N:%.1f" % temp)
        except Exception as e:
            logging.error("Failed to log temperature: %s" % e)

    def read_file(self, name):
        return Image.open(name)

    def draw(self, start):
        try:
            t = tempfile.NamedTemporaryFile()
            rrdtool.graph(t.name,
                    '--imgformat', 'PNG',
                    '--width', '540',
                    '--height', '100',
                    '--start', "-%s" % start,
                    #'--end', "-1",
                    '--vertical-label', 'Graden Celcius',
                    '--title', 'Temperature',
                    #'--lower-limit', '0',
                    "DEF:temperature=%s:temperature:AVERAGE" % RRD_FILE,
                    'AREA:temperature#990033:Temperatuur')
            return self.read_file(t.name)
        except Exception as e:
            logging.error("Failed to draw temperature: %s" % e)
            raise
