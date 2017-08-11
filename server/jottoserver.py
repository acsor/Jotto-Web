from enum import Enum, unique
from http.server import BaseHTTPRequestHandler, HTTPServer
from linecache import getline
from urllib.parse import parse_qs

from JottoWeb.JottoWebApp.utils import lines_count


@unique
class Error(Enum):
    ILL_FORMATTED = (0, "Ill-formatted request")
    NON_NUMBER = (1, "Non-number puzzle ID or puzzle ID out of range")
    INVALID_GUESS = (2, "Invalid guess. Invalid length of guess or guess not a dictionary word")


class Request:
    """
    A bare class to abstract out the work of reading the query string.
    The objects of this class should not perform validation on the data but just ease the process of reading it.
    (Think of it like the associative arrays $_GET or $_POST in PHP.)
    """
    KEY_PUZZLE = "puzzle"
    KEY_GUESS = "guess"

    def __init__(self, path):
        query_dict = parse_qs(path)

        self.puzzle_id = query_dict[self.KEY_PUZZLE][0] if self.KEY_PUZZLE in query_dict else None
        self.guess = query_dict[self.KEY_GUESS][0] if self.KEY_GUESS in query_dict else None
        # TO-DO Add delay parameter in query string


class Response(object):
    def __str__(self):
        return self.get_representation()

    def get_representation(self):
        raise NotImplementedError("get_representation() must be implemented by subclasses")


class ErrorResponse(Response):
    def __init__(self, error):
        super().__init__()
        self.error = error

    def get_representation(self):
        return "error %d %s\n" % (self.error.value[0], self.error.value[1])


class SuccessfulResponse(Response):
    def __init__(self, in_common, correct_pos):
        super().__init__()
        self.in_common = in_common
        self.correct_pos = correct_pos

    def get_representation(self):
        return "guess %d %d\n" % (self.in_common, self.correct_pos)

    @classmethod
    def from_guess(cls, hidden, guess):
        """
        Factory method for Response instances.

        :param hidden: hidden word stored in the server
        :param guess: guessed word
        :return:
        """
        if len(hidden) != len(guess):
            raise ValueError("The lengths of the two strings must match")

        return SuccessfulResponse(
            cls._in_common(hidden, guess),
            cls._correct_position(hidden, guess)
        )

    @staticmethod
    def _in_common(first, second):
        fmap: dict = SuccessfulResponse._letters_count(first)
        smap: dict = SuccessfulResponse._letters_count(second)
        in_common = 0

        for i in set(fmap.keys()).intersection(smap.keys()):
            in_common += min(fmap[i], smap[i])

        return in_common

    @staticmethod
    def _correct_position(first, second):
        return sum([f == s for f, s in zip(first, second)])

    @staticmethod
    def _letters_count(word: str):
        res = dict()

        for c in word:
            res[c] = res.get(c, 0) + 1

        return res


# noinspection PyAttributeOutsideInit
class JottoHTTPRequestHandler(BaseHTTPRequestHandler):

    CONFIG = {
        "assets": "./assets/",
        "dictionary": "English dictionary.txt",
        "word_length": 5,
    }

    def setup(self):
        super().setup()
        self.word_length = self.CONFIG["word_length"]
        self.dictionary = self.CONFIG["assets"] + self.CONFIG["dictionary"]
        self.dictionary_length = lines_count(self.dictionary)

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()

        req = Request(self.path[2:])

        self.wfile.write(
            self.get_response(req).get_representation().encode()
        )
        # self.wfile.write(("I'm working, dear %s:%d!\n" % self.client_address).encode())

    def get_response(self, request: Request):
        if request.puzzle_id is None or request.guess is None:
            return ErrorResponse(Error.ILL_FORMATTED)
        elif not request.puzzle_id.isdecimal():
            return ErrorResponse(Error.NON_NUMBER)

        try:
            server_word = self.get_word(int(request.puzzle_id))
        except ValueError:
            return ErrorResponse(Error.NON_NUMBER)

        if type(request.guess) is not str or len(request.guess) != len(server_word):
            return ErrorResponse(Error.INVALID_GUESS)

        response = SuccessfulResponse.from_guess(server_word, request.guess)

        if response is None:
            response = ErrorResponse(Error.ILL_FORMATTED)

        return response

    def get_word(self, puzzle_id):
        if not (1 <= puzzle_id <= self.dictionary_length):
            raise ValueError("puzzle_id (%d) out of bounds" % puzzle_id)

        return getline(self.dictionary, puzzle_id).strip()


def main():
    config = {
        "address": "",
        "port": 3111,
    }
    server = HTTPServer(
        (config["address"], config["port"]),
        JottoHTTPRequestHandler
    )

    server.serve_forever()


if __name__ == "__main__":
    main()
