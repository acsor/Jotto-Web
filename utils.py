def lines_count(filename):
    with open(filename) as f:
        return sum((1 for i in f))
