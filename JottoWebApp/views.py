from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponseNotAllowed
from django.shortcuts import loader, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .models import Puzzle, Session, Guess


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
    context = {
        "session": session,
    }

    if session.end_date is None:
        session.end_date = timezone.localtime()
        session.save()
    else:
        context[var_error] = True

    return HttpResponse(template.render(context, request))


def sessions_still_open(request):
    template = loader.get_template("jotto/sessions_still_open.html")
    context = {
        "open_sessions": [s for s in Session.objects.all() if s.end_date is None]
    }

    return HttpResponse(template.render(context, request))


def session_guess(request: HttpRequest, session_id):
    # TO-DO Validate against empty and unaccepted values (e.g. numbers or words with letters not in the alphabet.)
    session = get_object_or_404(Session, id=session_id)
    param_guess = "guess"
    param_error = "error"

    if session.end_date is not None:
        template = loader.get_template("jotto/error.html")
        context = {
            param_error: "Game %d was closed. You cannot add any more guesses." % session.id
        }

        return HttpResponseNotAllowed(("GET", "POST"), template.render(context, request))

    guess = Guess(name=request.GET[param_guess], session=session)
    guess.save()

    return HttpResponseRedirect(reverse("jotto:session", args=(session.id,)))
