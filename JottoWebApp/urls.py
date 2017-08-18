from django.conf.urls import url
from .views import *


app_name = "jotto"

urlpatterns = [
    url(r"^$", IndexView.as_view(), name="index"),
    url(r"^pre_session$", PreSessionView.as_view(), name="pre_session"),
    url(r"^session_new$", session_new, name="session_new"),
    url(r"^session/(?P<pk>\d+)$", SessionView.as_view(), name="session"),
    url(r"^session_close/(?P<session_id>\d+)$", session_close, name="session_close"),
    url(r"^open_sessions$", OpenSessionsView.as_view(), name="open_sessions"),
    url(r"^closed_sessions$", ClosedSessionsView.as_view(), name="closed_sessions"),
    url(r"^session_guess/(?P<session_id>\d+)$", session_guess, name="session_guess"),
]
