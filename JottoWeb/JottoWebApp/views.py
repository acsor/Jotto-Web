from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import loader, get_object_or_404
from django.urls import reverse
from django.utils import timezone

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
    puzzle = Puzzle.get_random()

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


def close_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    template = loader.get_template("jotto/post_close_session.html")
    var_error = "error_already_ended"
    config = {
        "session": session,
    }

    if session.end_date is None:
        session.end_date = timezone.localtime()
        session.save()
    else:
        config[var_error] = True

    return HttpResponse(template.render(config, request))
