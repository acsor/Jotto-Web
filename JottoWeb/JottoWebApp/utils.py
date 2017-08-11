def lines_count(filename):
    """
    :param filename: string. The path of a file to count the number of lines for.
    :return: the number of lines in filename.
    """
    with open(filename) as f:
        return sum((1 for i in f))


def in_common(first, second):
    """
    :param first: a string.
    :param second: a string.
    :return: the number of characters that first and second share, without them having the same index.
    """
    fmap: dict = chars_count(first)
    smap: dict = chars_count(second)
    result = 0

    for i in set(fmap.keys()).intersection(smap.keys()):
        result += min(fmap[i], smap[i])

    return result


def correct_position(first, second):
    """
    :param first: a string.
    :param second: a string.
    :return: the number of characters in first and second which are equal and are located at the same index.
    """
    return sum([f == s for f, s in zip(first, second)])


def chars_count(word: str):
    """
    :param word: string to count the occurrences of a character symbol for.
    :return: a dictionary mapping each character found in word to the number of times it appears in it.
    """
    res = dict()

    for c in word:
        res[c] = res.get(c, 0) + 1

    return res
