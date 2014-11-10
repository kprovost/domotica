import rrdtool
import logging
import domotica.heating as heating
from poller import Poller
import s7

class TemperaturePoller(Poller):
    def __init__(self):
        return
        rrdtool.create( 'temperature.rrd',
                '--no-overwrite',
                '--step', '5',
                'DS:temperature:GAUGE:30:-20:100',
                'RRA:AVERAGE:0.5:1:1440',   # Daily
                'RRA:AVERAGE:0.5:12:10080', # Weekly,
                'RRA:AVERAGE:0.5:720:365')  # Yearly

    def poll(self, s7conn):
        rrdtool.update('temperature.rrd',
                'N:19.0')

        rrdtool.graph('temperature.png',
                '--imgformat', 'PNG',
                '--width', '540',
                '--height', '100',
                #'--start', "-%i" % 2014,
                #'--end', "-1",
                '--vertical-label', 'Degrees Celcius',
                '--title', 'Temperature',
                #'--lower-limit', '0',
                'DEF:temperature=temperature.rrd:temperature:AVERAGE',
                'AREA:temperature#990033:Downloads')
        pass
