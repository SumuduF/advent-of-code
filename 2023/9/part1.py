#!/usr/bin/env -S uv run

import argparse
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
    return [list(map(int, line.split())) for line in lines]

def solve(task):
    return sum(next_val(hist) for hist in task)

def next_val(hist):
    if all(v == 0 for v in hist): return 0
    n = len(hist)
    diffs = [hist[i] - hist[i-1] for i in range(1, n)]
    return hist[-1] + next_val(diffs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
