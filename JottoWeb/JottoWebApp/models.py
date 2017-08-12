from django.db.models import CharField
from django.db import models
from django.utils import timezone
from .utils import in_common, correct_position


class Puzzle(models.Model):
    name = CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Session(models.Model):
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.puzzle.name

    def guesses_by_newest(self):
        """
        :return: the list of guesses associated with the session, ordered from newest to oldest.
        """
        # TO-DO Find a better way to integrate this ordering with the Django template system
        return self.guess_set.order_by("-time")


class Guess(models.Model):
    # TO-DO See if it is possible to avoid this hardcoded value (max_length=128)
    name = models.CharField(max_length=128, editable=False)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    def common(self):
        hidden = Puzzle.objects.get(id=self.session.puzzle.id)

        return in_common(self.name, hidden.name)

    def correct_position(self):
        hidden = Puzzle.objects.get(id=self.session.puzzle.id)

        return correct_position(self.name, hidden.name)
