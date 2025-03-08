from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.conf import settings
import logging
from notifier import sms
from pollers.temperaturepoller import TemperaturePoller
import s7

import domotica.light as light
import domotica.alarm as alarm
from domotica.heating import Heating
import domotica.power as power

class StubS7:
    def readFlagBit(self, db, id):
        return 0
    def writeFlagBit(self, db, id, value):
        return True
    def readBit(self, db, id, bit):
        return 0
    def writeBit(self, db, id, bit, value):
        return True
    def readOutput(self, do):
        return 0

def getS7Conn():
    if len(settings.PLC_IP) == 0:
        return StubS7()
    return s7.S7Comm(settings.PLC_IP, settings.PLC_TYPE)

def _lightCount(s7conn, groupName):
    lights = light.loadGroup(s7conn, groupName)

    onCount = 0
    for l in lights:
        if l.isOn():
            onCount = onCount + 1

    return onCount

@login_required
def front(request):
    return alarm_index(request)

@login_required
def lights(request):
    s7conn = getS7Conn()

    lights = []
    for (name, merker, do) in settings.LIGHTS:
        lights.append(light.Light(name, merker, do, s7conn))

    context = {
            'tag': 'light',
            'lights': lights
            }
    return render(request, "lights.html", context)

def do_login(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is None:
            raise

        if not user.is_active:
            raise

        login(request, user)
        # Redirect to a success page.
        return front(request)
    except Exception as e:
        return render(request, "login.html")

@csrf_exempt
@login_required
def lightswitch(request, action):
    s7conn = getS7Conn()
    if action == "all_off":
        if not light.AllOff(s7conn):
            raise Http404
        return HttpResponse()
    if action == "all_on":
        if not light.AllOn(s7conn):
            raise Http404
        return HttpResponse()

    idInt = 0
    try:
        idInt = int(request.POST.get("id", ""))
    except:
        raise Http404

    # Rather than find the light just take the ID from the post
    # Bit of a security issue, because it's an arbitrary merker write now
    l = light.Light("", idInt, 0, s7conn)

    if action == "toggle":
        print("Light %d toggled by %s" % (l.getID(), request.META.get('REMOTE_ADDR')))
        if not l.toggleLight():
            raise Http404
    else:
        raise Http404

    return HttpResponse()


@login_required
def alarm_index(request):
    s7conn = getS7Conn()
    a = alarm.Alarm(s7conn)

    balance = "N/A"
    try:
        balance = float(sms.query_balance())
    except Exception as e:
        logging.error("Failed to retrieve SMS account balance: %s" % e)

    context = {
            'tag': 'alarm',
            'alarm': a,
            'detectors': alarm.getDetectors(s7conn),
            'balance': balance
            }
    return render(request, "alarm.html", context)

@csrf_exempt
@login_required
def alarm_action(request, action):
    s7conn = getS7Conn()
    a = alarm.Alarm(s7conn)
    if action == 'arm':
        a.arm()
    elif action == 'disarm':
        a.disarm()
    else:
        raise Http404

    context = {
            'tag': 'lights',
            'alarm': a,
            'detectors': alarm.getDetectors(s7conn)
            }
    return render(request, "alarm.html", context)

