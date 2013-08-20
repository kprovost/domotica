from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.conf import settings
import s7

import light
from alarm import Alarm
from heating import Heating

PLC_IP = "10.0.3.9"

def _lightCount(s7conn, groupName):
    lights = light.loadGroup(s7conn, groupName)

    onCount = 0
    for l in lights:
        if l.isOn():
            onCount = onCount + 1

    return onCount

@login_required
def index(request):
    s7conn = s7.S7Comm(PLC_IP)

    groups = light.loadGroupNames()
    groups = map(lambda x: (x, _lightCount(s7conn, x)), groups)

    context = { 'groups' : groups }
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
        return index(request)
    except Exception as e:
        return render(request, "login.html")

@login_required
def lightgroup(request, groupName):
    s7conn = s7.S7Comm(PLC_IP)
    lights = light.loadGroup(s7conn, groupName)
    if lights is None:
        raise Http404

    context = {
            'groupName': groupName,
            'lights' : lights
            }
    return render(request, "lights.html", context)

@csrf_exempt
@login_required
def lightswitch(request, action):
    s7conn = s7.S7Comm(PLC_IP)
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

    s7conn = s7.S7Comm(PLC_IP)

    l = light.loadByID(s7conn, idInt)
    if l is None:
        raise Http404

    context = { 'light': l }
    return render(request, "lightsettings.html", context)

@login_required
def alarm(request):
    s7conn = s7.S7Comm(PLC_IP)
    a = Alarm(s7conn)
    context = { 'alarm': a }
    return render(request, "alarm.html", context)

@csrf_exempt
@login_required
def alarm_action(request, action):
    print "alarm_action"
    s7conn = s7.S7Comm(PLC_IP)
    a = Alarm(s7conn)
    if action == 'arm':
        a.arm()
    elif action == 'disarm':
        a.disarm()
    context = { 'alarm': a }
    return render(request, "alarm.html", context)

@login_required
def power(request):
    return render(request, "power.html")

@login_required
def heating(request):
    s7conn = s7.S7Comm(PLC_IP)
    h = Heating(s7conn)

    context = { 'heating': h }
    return render(request, "heating.html", context)
