from django.contrib import admin
from .models import Puzzle, Session, Guess

admin.site.register(Puzzle)
admin.site.register(Session)
admin.site.register(Guess)
