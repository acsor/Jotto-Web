from django.conf.urls import url
from .views import *


app_name = "jotto"

urlpatterns = [
    url(r"^$", index, name="index"),
    url(r"^pre_session$", pre_session, name="pre_session"),
    url(r"^new_session$", new_session, name="new_session"),
    url(r"^session/(?P<session_id>\d+)$", session, name="session"),
]
