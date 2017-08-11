from django.db.models import CharField
from django.db import models
from .utils import in_common, correct_position


class Puzzle(models.Model):
    name = CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Session(models.Model):
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE)

    def __repr__(self):
        pass


# noinspection PyUnresolvedReferences
class Guess(models.Model):
    guess = models.CharField(max_length=128)  # TO-DO See if it is possible to avoid this hardcoded value
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def __str__(self):
        return self.guess

    def common(self):
        session = Session.objects.get(id=self.session)
        hidden = Puzzle.get(id=session.puzzle)

        return in_common(self.guess, hidden.name)

    def correct_position(self):
        session = Session.objects.get(id=self.session)
        hidden = Puzzle.get(id=session.puzzle)

        return correct_position(self.guess, hidden)
