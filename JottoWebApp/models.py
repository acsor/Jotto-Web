import re
from random import randint

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import CharField
from django.utils import timezone

from .utils import in_common, correct_position


class Puzzle(models.Model):
    name = CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    @classmethod
    def get_random(cls):
        # TO-DO Find a more fast-performing alternative to this.
        puzzles = cls.objects.all()
        puzzle = puzzles[randint(0, puzzles.count())]

        del puzzles

        return puzzle


class Session(models.Model):
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    start_date = models.DateTimeField(default=timezone.localtime)
    end_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.puzzle.name

    def guesses_by_newest(self):
        """
        :return: the list of guesses associated with the session, ordered from newest to oldest.
        """
        # TO-DO Find a better way to integrate this ordering with the Django template system
        return self.guess_set.order_by("-time")

    def is_closed(self):
        return self.end_date is not None and self.end_date <= timezone.now()


class Guess(models.Model):
    # TO-DO See if it is possible to avoid this hardcoded value (max_length=128)
    name = models.CharField(max_length=128, editable=False)
    # TO-DO Enable data validation in this and even other models
    # name = models.CharField(max_length=128, editable=False, validators=(validate_name,))
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.localtime)
    # TO-DO replace this pattern with a Unicode-compatible one, such as \p{L}
    re_name = re.compile("[a-zA-Z]+")

    def __str__(self):
        return self.name

    def common(self):
        hidden = Puzzle.objects.get(id=self.session.puzzle.id)

        return in_common(self.name, hidden.name)

    def correct_position(self):
        hidden = Puzzle.objects.get(id=self.session.puzzle.id)

        return correct_position(self.name, hidden.name)

    @staticmethod
    def validate_name(name):
        if len(name) == 0:
            raise ValidationError("Input string has zero length.")
        if re.fullmatch(Guess.re_name, name) is None:
            raise ValidationError("Input is not a valid string.")
