#!/usr/bin/env -S uv run

import argparse
import itertools
import sys

def main(filename):
    lines = read_file(filename)
    task = parse_task(lines)
    answer = solve(task)

    print(answer)

def read_file(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f]
    return lines

def parse_task(lines):
    task = []
    for line in lines:
        record, nums = line.split()
        task.append((record, list(map(int, nums.split(",")))))
    return task

def solve(task):
    return sum(ways(record, nums) for (record, nums) in task)

def ways(record, nums):
    n = len(record)

    partial = []
    def rec(i):
        if not works(partial, nums, i == n): return 0
        if i == n: return 1
        ans = 0
        if record[i] != "?":
            partial.append(record[i])
            ans += rec(i+1)
            partial.pop()
        else:
            partial.append(".")
            ans += rec(i+1)
            partial[-1] = "#"
            ans += rec(i+1)
            partial.pop()
        return ans

    return rec(0)

def works(attempt, nums, needs_all_goals):
    groups = []
    for (k, g) in itertools.groupby(attempt):
        groups.append((k, len(list(g))))

    if needs_all_goals:
        groups.append((".", 0))

    goals = iter(nums)
    for (c, num) in groups[:-1]:
        if c == ".": continue
        g = next(goals, None)
        if g is None: return False
        if g != num: return False

    if groups and (groups[-1][0] == "#"):
        g = next(goals, None)
        if g is None: return False
        if g < groups[-1][1]: return False

    if needs_all_goals:
        g = next(goals, None)
        return g is None
    else:
        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
