import argparse
import sys
from itertools import islice

def run_solution(solution):
    """Basic AoC main: takes care of getting input and printing the answer."""
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("filename", nargs="?")
    args = arg_parser.parse_args()

    if args.filename is not None:
        input_lines = _read_rstripped_lines(open(args.filename, "r"))
    else:
        input_lines = _read_rstripped_lines(sys.stdin)

    answer = solution(input_lines)

    print(answer)

def _read_rstripped_lines(infile):
    """Returns lines (rstripped) from the given file (closes the file)."""
    with infile as f:
        return [line.rstrip() for line in f]

# backported from 3.12
def batched(iterable, n):
    """Yields values from iterable, grouped into n-tuples."""
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch

# python3 killed cmp for some reason
def cmp(a, b):
    return (a > b) - (a < b)

class Fenwick():
    """Implements a Fenwick tree."""

    def __init__(self, n: int):
        """Creates an empty (all zeros) tree on n elements."""
        self._n = n
        self._v = [0]*n

    def add(self, val: int, i: int):
        """Adds val to position i."""
        # Note, internally the math is done with 1-based indices
        i += 1
        while i <= self._n:
            self._v[i-1] += val
            i += i & (-i)

    def cumul(self, i: int):
        """Returns the sum of values up to position i (inclusive)."""
        # Note, internally the math is done with 1-based indices
        i += 1
        ret = 0
        while i > 0:
            ret += self._v[i-1]
            i -= i & (-i)
        return ret
