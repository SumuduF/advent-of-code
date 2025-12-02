from aoclib import util
from functools import cache
from itertools import count, groupby
import heapq

def solution(lines):
    ranges = range_parser().parse("".join(lines))
    ranges.sort()

    part1_ans = sum(invalids(ranges, gen_invalids(2)))
    # longest input is 10 digits; consider all prime repetition counts up to
    # that
    reps = [2, 3, 5, 7]
    all_invalids = heapq.merge(*[gen_invalids(p) for p in reps])
    part2_ans = sum(invalids(ranges, all_invalids))

    return (part1_ans, part2_ans)

def invalids(ranges, gen):
    # groupby discards duplicates retained by heapq.merge
    gen = (k for (k, _) in groupby(gen))

    z = next(gen)
    for (a, b) in ranges:
        while z < a:
            z = next(gen)
        while z <= b:
            yield z
            z = next(gen)

def gen_invalids(reps):
    for atom in count(1):
        yield int(str(atom) * reps)

@cache
def range_parser():
    from aoclib.parsing import seplist, regex

    nums = regex("([0-9]+)-([0-9]+)").zipconv(int, int)
    return seplist(nums, ",")

if __name__ == "__main__": util.run_solution(solution)
