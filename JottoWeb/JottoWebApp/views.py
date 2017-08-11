from django.shortcuts import render, loader
from django.http import HttpResponse


def index(request):
    template = loader.get_template("jotto/index.html")

    return HttpResponse(template.render(dict(), request))


def new_session(request):
    pass
