from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.conf import settings
from notifier import sms
import s7

import light
import alarm
from heating import Heating
import power

def getS7Conn():
    return s7.S7Comm(settings.PLC_IP)

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
def lightgroups(request):
    s7conn = getS7Conn()

    groups = light.loadGroupNames()
    groups = map(lambda x: (x, _lightCount(s7conn, x)), groups)

    context = {
            'tag': 'light',
            'groups' : groups
            }
    return render(request, "lightgroups.html", context)

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

@login_required
def lightgroup(request, groupName):
    s7conn = getS7Conn()
    lights = light.loadGroup(s7conn, groupName)
    if lights is None:
        raise Http404

    context = {
            'tag': 'light',
            'groupName': groupName,
            'lights' : lights
            }
    return render(request, "lights.html", context)

@csrf_exempt
@login_required
def lightswitch(request, action):
    s7conn = getS7Conn()
    if action == "all_off":
        if not light.AllOff(s7conn):
            raise Http404
        return HttpResponse()

    idInt = 0
    try:
        idInt = int(request.REQUEST["id"])
    except:
        raise Http404

    l = light.Light("", idInt, s7conn)

    if action == "toggle":
        print ("Light %d toggled by %s" % (l.getID(), request.META.get('REMOTE_ADDR')))
        if not l.toggleLight():
            raise Http404
    elif action == "toggle_motion":
        if not l.toggleMotion():
            raise Http404
    elif action == "toggle_blink":
        if not l.toggleBlinkOnAlarm():
            raise Http404
    elif action == "timeout":
        timeout = 0
        try:
            timeout = int(request.REQUEST["timeout"])
        except:
            raise Http404
        l.setTimeout(timeout)
    else:
        raise Http404

    return HttpResponse()

@login_required
def lightsettings(request, id):
    idInt = 0
    try:
        idInt = int(id)
    except:
        raise Http404

    s7conn = getS7Conn()

    l = light.loadByID(s7conn, idInt)
    if l is None:
        raise Http404

    context = {
            'tag': 'light',
            'light': l
            }
    return render(request, "lightsettings.html", context)

@login_required
def alarm_index(request):
    s7conn = getS7Conn()
    a = alarm.Alarm(s7conn)
    context = {
            'tag': 'alarm',
            'alarm': a,
            'detectors': alarm.getDetectors(s7conn),
            'balance': float(sms.query_balance())
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
    elif action == 'toggle_detector':
        idInt = 0
        try:
            idInt = int(request.REQUEST["id"])
        except:
            raise Http404
        d = alarm.getDetectorByID(s7conn, idInt)
        d.toggle()
    context = {
            'tag': 'lights',
            'alarm': a,
            'detectors': alarm.getDetectors(s7conn)
            }
    return render(request, "alarm.html", context)

@login_required
def powerplug(request):
    s7conn = getS7Conn()

    plugs = power.getPlugs(s7conn)
    if power is None:
        raise Http404

    context = {
            'tag': 'power',
            'powerplugs': plugs
            }
    return render(request, "power.html", context)

@csrf_exempt
@login_required
def powerswitch(request, action, ID):
    s7conn = getS7Conn()

    plug = power.getPlug(int(ID), s7conn)

    if action == "toggle":
        print ("Power plug %s toggled by %s" % (plug.getName(),
            request.META.get('REMOTE_ADDR')))
        if not plug.togglePower():
            raise Http404
    else:
        raise Http404

    return HttpResponse()

@login_required
def heating(request):
    s7conn = getS7Conn()
    h = Heating(s7conn)

    context = {
            'tag': 'heating',
            'heating': h
            }
    return render(request, "heating.html", context)

@csrf_exempt
@login_required
def heatingtoggle(request, ID):
    s7conn = getS7Conn()
    h = Heating(s7conn)

    if ID == "force_on":
        h.toggleForceOn()
    elif ID == "auto":
        h.toggleAuto()
    elif ID == "state":
        # Read only variable. Do nothing
        pass
    else:
        raise Http404

    return HttpResponse()
