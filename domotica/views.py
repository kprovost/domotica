from django.shortcuts import render
from django.http import HttpResponse
import light

def index(request):
    lights = light.loadAll()
    context = { 'lights' : lights }
    return render(request, "lights.html", context)
