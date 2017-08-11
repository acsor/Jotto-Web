from django.conf.urls import url
from .views import *


app_name = "jotto"

urlpatterns = [
    url(r"^$", index, name="index"),
    url(r"^new_session", new_session, name="new_session"),
]
