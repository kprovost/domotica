from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.conf import settings
import s7

import light

PLC_IP = "10.0.3.9"

@login_required
def index(request):
    groups = light.loadGroupNames()
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
        if not l.toggleLight():
            raise Http404
    elif action == "toggle_motion":
        if not l.toggleMotion():
            raise Http404
    elif action == "toggle_blink":
        if not l.toggleBlinkOnAlarm():
            raise Http404
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
