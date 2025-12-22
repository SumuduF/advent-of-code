#!/usr/bin/env -S uv run

from aoclib import util
from functools import cmp_to_key

def solution(input_lines):
    orders, updates = util.line_groups(input_lines)

    # "very specific order" means all pairs are actually there
    # raise an error in case we ever try to compare incomparable values
    pairs = set(tuple(map(int, line.split("|"))) for line in orders)
    def cmp(p, q):
        if (p, q) in pairs: return -1
        if (q, p) in pairs: return 1
        raise ValueError(f"no pair for {p} and {q}")
    by_pairs = cmp_to_key(cmp)

    part1_ans, part2_ans = 0, 0
    for line in updates:
        pages = list(map(int, line.split(",")))
        fixed = sorted(pages, key=by_pairs)

        val = fixed[len(fixed) // 2]
        if pages == fixed:
            part1_ans += val
        else:
            part2_ans += val

    return (part1_ans, part2_ans)

if __name__ == "__main__": util.run_solution(solution)
