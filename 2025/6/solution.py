#!/usr/bin/env -S uv run

from aoclib import util
from math import prod

def solution(lines):
    digits, ops = lines[:-1], lines[-1]

    # note: input is right-trimmed but for ease of coding we want to pad each
    # line with spaces
    n = len(digits)
    m = max(len(row) for row in digits)
    for (i, row) in enumerate(digits):
        digits[i] = row + (" " * (m - len(row)))

    # use the operators as convenient markers
    cols = [i for (i, ch) in enumerate(ops) if ch != " "]
    cols.append(m+1) # sentinel to bound the last set

    part1_ans = 0
    part2_ans = 0
    for (i, j) in zip(cols, cols[1:]):
        # use i:(j-1) to leave out the column of spaces
        p1_nums = nums_horiz(digits, i, j-1)
        p2_nums = nums_vert(digits, i, j-1)
        match ops[i]:
            case "*":
                part1_ans += prod(p1_nums)
                part2_ans += prod(p2_nums)
            case "+":
                part1_ans += sum(p1_nums)
                part2_ans += sum(p2_nums)

    return (part1_ans, part2_ans)

def nums_horiz(digits, start, end):
    for row in digits:
        yield int(row[start:end])

def nums_vert(digits, start, end):
    for c in range(start, end):
        yield int("".join(row[c] for row in digits))

if __name__ == "__main__": util.run_solution(solution)
