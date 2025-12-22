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
    groups = []
    for line in lines:
        _, _, lists = line.partition(":")
        winning, _, have = lists.partition("|")
        groups.append(([int(num) for num in winning.split()], [int(num) for num in have.split()]))

    return groups

def solve(task):
    total = 0
    for (winning, have) in task:
        count = 0
        for val in have:
            if val in winning:
                count += 1

        if count > 0:
            total += 2**(count - 1)
    return total

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
