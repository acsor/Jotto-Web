from django.conf.urls import url
from .views import *


app_name = "jotto"

urlpatterns = [
    url(r"^$", index, name="index"),
    url(r"^pre_session$", pre_session, name="pre_session"),
    url(r"^new_session$", new_session, name="new_session"),
    url(r"^session/(?P<session_id>\d+)$", session, name="session"),
    url(r"^close_session/(?P<session_id>\d+)$", close_session, name="close_session"),
    url(r"^open_sessions$", open_sessions, name="open_sessions"),
    url(r"^closed_sessions$", closed_sessions, name="closed_sessions"),
    url(r"^session_guess/(?P<session_id>\d+)$", session_guess, name="session_guess"),
]
