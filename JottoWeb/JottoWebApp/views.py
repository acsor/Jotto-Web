from django.shortcuts import render, loader, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from random import randint
from .models import Session, Puzzle


# TO-DO Update the view functions by using the default view classes
# as described in the Django tutorial, part 4.
def index(request):
    template = loader.get_template("jotto/index.html")

    return HttpResponse(template.render(dict(), request))


def pre_session(request):
    template = loader.get_template("jotto/pre_session.html")

    return HttpResponse(template.render(dict(), request))


def new_session(request):
    puzzles = Puzzle.objects.all()
    puzzle = puzzles[randint(0, puzzles.count())]

    del puzzles

    curr_session = Session(puzzle=puzzle)
    curr_session.save()

    return HttpResponseRedirect(reverse("jotto:session", args=(curr_session.id,)))


def session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    template = loader.get_template("jotto/session.html")
    context = {
        "session": session,
    }

    return HttpResponse(template.render(context, request))
