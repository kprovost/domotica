from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, Http404

import light

def index(request):
    lights = light.loadAll()
    context = { 'lights' : lights }
    return render(request, "lights.html", context)

@csrf_exempt
def lightswitch(request):
    print "Request.id %s" % request.REQUEST["id"]
    raise Http404
