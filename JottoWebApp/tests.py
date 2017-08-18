from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Puzzle, Session
from random import choices, random


def sessions_factory_base():
    puzzle_names = ["apple", "sand", "bicarbonate", "cola", "cool", "repetitive", "mountain",
                    "bike", "sky", "eat", "various", "endless", "penguin", "german", "quorum"]
    puzzles = [Puzzle.objects.create(name=name) for name in puzzle_names]
    sessions = [Session.objects.create(puzzle=p) for p in puzzles]

    return sessions


def sessions_factory_random_closed():
    sessions = sessions_factory_base()

    for s in sessions:
        if 0 <= random() < 0.5:
            s.end_date = timezone.now()
            s.save()

    return sessions


class IndexViewTest(TestCase):
    def test_is_reachable(self):
        response = self.client.get(reverse("jotto:index"))
        unaccepted_codes = (404,)

        self.assertNotIn(
            response.status_code,
            unaccepted_codes
        )


class PreSessionViewTest(TestCase):
    def test_is_reachable(self):
        response = self.client.get(reverse("jotto:pre_session"))
        unaccepted_codes = (404,)

        self.assertNotIn(
            response.status_code,
            unaccepted_codes
        )


class OpenSessionsViewTest(TestCase):
    def test_open_sessions_count(self):
        sessions = sessions_factory_random_closed()
        open_sessions = sum([1 for s in sessions if not s.is_closed()])
        response = self.client.get(reverse("jotto:open_sessions"))

        self.assertEqual(
            open_sessions,
            len(response.context["sessions"])
        )

    def test_closed_sessions_count(self):
        sessions_factory_random_closed()
        closed_sessions = 0  # The template is only passed open sessions
        response = self.client.get(reverse("jotto:open_sessions"))

        self.assertEqual(
            closed_sessions,
            sum([1 for s in response.context["sessions"] if s.is_closed()])
        )


class ClosedSessionsViewTest(TestCase):
    def test_open_sessions_count(self):
        sessions_factory_random_closed()
        open_sessions = 0
        response = self.client.get(reverse("jotto:closed_sessions"))

        self.assertEqual(
            open_sessions,
            sum([1 for s in response.context["sessions"] if not s.is_closed()])
        )

    def test_closed_sessions_count(self):
        sessions = sessions_factory_random_closed()
        closed_sessions = sum([1 for s in sessions if s.is_closed()])
        response = self.client.get(reverse("jotto:closed_sessions"))

        self.assertEqual(
            closed_sessions,
            sum([1 for s in response.context["sessions"] if s.is_closed()])
        )


class CloseSessionTest(TestCase):
    def test_close_all(self):
        """
        Tests whether all of the stored sessions are closed when the app is requested to do so.
        """
        sessions = sessions_factory_base()

        for s in sessions:
            self.assertFalse(s.is_closed(), "Session no. %d is closed" % s.id)
            self.client.get(reverse("jotto:session_close", args=(s.id,)))

            s.refresh_from_db(fields=("end_date",))
            self.assertTrue(s.is_closed(), "Session no. %d is not closed" % s.id)
