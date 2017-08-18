from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.http.response import HttpResponseNotAllowed
from django.shortcuts import loader, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views.generic import DetailView, ListView, TemplateView


from .models import Puzzle, Session, Guess


# TO-DO Update the view functions by using the default view classes
# as described in the Django tutorial, part 4.
class IndexView(TemplateView):
    template_name = "jotto/index.html"


class PreSessionView(TemplateView):
    template_name = "jotto/pre_session.html"


def session_new(request):
    puzzle = Puzzle.get_random()

    session = Session(puzzle=puzzle)
    session.save()

    return HttpResponseRedirect(reverse("jotto:session", args=(session.id,)))


class SessionView(TemplateView):
    template_name = "jotto/session.html"

    def get_context_data(self, **kwargs):
        context = super(SessionView, self).get_context_data(**kwargs)
        context["session"] = get_object_or_404(Session, id=self.kwargs["pk"])

        return context


def session_close(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    template = loader.get_template("jotto/post_close_session.html")
    param_error = "error_already_closed"
    context = {
        "session": session,
    }

    if not session.is_closed():
        session.end_date = timezone.localtime()
        session.save()
    else:
        context[param_error] = True

    return HttpResponse(template.render(context, request))


class OpenSessionsView(ListView):
    template_name = "jotto/open_sessions.html"
    context_object_name = "sessions"

    def get_queryset(self):
        return [s for s in Session.objects.order_by("-start_date") if not s.is_closed()]


class ClosedSessionsView(ListView):
    template_name = "jotto/closed_sessions.html"
    context_object_name = "sessions"

    def get_queryset(self):
        return [s for s in Session.objects.order_by("-start_date") if s.is_closed()]


def session_guess(request: HttpRequest, session_id):
    # TO-DO Validate against empty and unaccepted values (e.g. numbers or words with letters not in the alphabet.)
    session = get_object_or_404(Session, id=session_id)
    param_guess = "guess"
    param_error = "error"

    if session.is_closed():
        template = loader.get_template("jotto/error.html")
        context = {
            param_error: "Game %d was closed. You cannot add any more guesses." % session.id
        }

        return HttpResponseNotAllowed(("GET", "POST"), template.render(context, request))

    guess = Guess(name=request.GET[param_guess], session=session)
    guess.save()

    return HttpResponseRedirect(reverse("jotto:session", args=(session.id,)))
