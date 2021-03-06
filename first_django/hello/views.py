from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return HttpResponse("Hello, world!")

def greet(request, name):
    return HttpResponse(f"Hello, {name.capitalize()}!")

def farewell(request, name):
    return render(request, "hello/farewell.html", {
        "name": name.capitalize()
    })