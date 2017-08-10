from django.db.models import CharField
from django.db import models


class Puzzle(models.Model):
    name = CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Session(models.Model):
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE)

    def __repr__(self):
        pass


class Guess(models.Model):
    guess = models.CharField(max_length=128)  # See if it is possible to avoid this hardcoded value
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def __str__(self):
        return self.guess

    def common(self):
        session = Session.objects.all()[0]  # TO-DO Modify this line to get a single value immediately
        hidden = Puzzle.get(id=session.puzzle)

        return self._in_common(self.guess, hidden.name)

    @staticmethod
    def _in_common(first, second):
        fmap: dict = Guess._letters_count(first)
        smap: dict = Guess._letters_count(second)
        in_common = 0

        for i in set(fmap.keys()).intersection(smap.keys()):
            in_common += min(fmap[i], smap[i])

        return in_common

    @staticmethod
    def _letters_count(word: str):
        """
        :param word: string to count the occurrences of a character symbol for.
        :return: a dictionary mapping each character found in word to the number of times it appears in it.
        """
        res = dict()

        for c in word:
            res[c] = res.get(c, 0) + 1

        return res
