from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, Http404
import s7

import light

PLC_IP = "10.0.3.9"

def index(request):
    s7conn = s7.S7Comm(PLC_IP)

    lights = light.loadAll(s7conn)
    context = { 'lights' : lights }
    return render(request, "lights.html", context)

@csrf_exempt
def lightswitch(request, action):
    idInt = 0
    try:
        idInt = int(id)
    except:
        raise Http404

    s7conn = s7.S7Comm(PLC_IP)
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
