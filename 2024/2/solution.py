#!/usr/bin/env -S uv run

from aoclib import util

def solution(input_lines):
    reports = [[int(v) for v in line.split()] for line in input_lines]

    part1_ans = sum(is_safe(report) for report in reports)
    part2_ans = sum(is_tolerable(report) for report in reports)

    return (part1_ans, part2_ans)

def is_safe(report):
    dels = [ b-a for (a, b) in zip(report, report[1:])]
    return all(1 <= d <= 3 for d in dels) or all(-3 <= d <= -1 for d in dels)

def is_tolerable(report):
    if is_safe(report): return True
    n = len(report)
    return any(is_safe(report[:i] + report[(i+1):]) for i in range(n))

if __name__ == "__main__": util.run_solution(solution)
