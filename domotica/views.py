from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, Http404
import s7

import light

def index(request):
    s7conn = s7.S7Comm("10.0.3.9")

    lights = light.loadAll(s7conn)
    context = { 'lights' : lights }
    return render(request, "lights.html", context)

@csrf_exempt
def lightswitch(request, action):
    s7conn = s7.S7Comm("10.0.3.9")
    l = light.Light("", request.REQUEST["id"], s7conn)

    if action != "toggle":
        raise Http404

    if not l.toggle():
        raise Http404

    return HttpResponse()
