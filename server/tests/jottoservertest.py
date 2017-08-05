import unittest
from unittest import TestCase
from server.jottoserver import SuccessfulResponse


class JottoServerTest(TestCase):

    def test_in_common(self):
        exp_result = {
            ("house", "mouse"): 4,
            ("sun", "gun"): 2,
            ("running", "raining"): 5,
            ("coast", "toast"): 4,
            ("merry", "carry"): 3,
            ("eagle", "screw"): 1,
            ("sea", "arm"): 1,
            ("chair", "hairy"): 4,
        }

        for key in exp_result:
            self.assertEqual(
                exp_result[key],
                SuccessfulResponse._in_common(*key),
                "The count number of '%s' does not equal that of '%s'" % key
            )

    def test_shortest_position(self):
        exp_result = {
            ("house", "mouse"): 4,
            ("sun", "gun"): 2,
            ("running", "raining"): 5,
            ("coast", "toast"): 4,
            ("merry", "carry"): 3,
            ("eagle", "screw"): 0,
            ("sea", "arm"): 0,
            ("chair", "hairy"): 0,
        }

        for key in exp_result:
            self.assertEqual(
                exp_result[key],
                SuccessfulResponse._correct_position(*key)
            )

if __name__ == "__main__":
    unittest.main()
