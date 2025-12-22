#!/usr/bin/env -S uv run

import argparse
import sys
from collections import defaultdict

def main(filename):
    grid = [""]
    with open(filename, "r") as f:
        grid.extend(("." + line.strip() + ".") for line in f)
    m = len(grid[1])
    grid[0] = ("." * m)
    grid.append(grid[0])
    n = len(grid)

    gear_vals = defaultdict(list)

    i, j = 0, 0
    while i < n:
        if grid[i][j].isnumeric():
            k = j
            while grid[i][k].isnumeric(): k += 1

            val = int(grid[i][j:k])
            for pos in gears_around(grid, i, j, k):
                gear_vals[pos].append(val)
            j = k
        else: j += 1

        if j == m: i, j = i+1, 0

    ratio_sum = 0
    for (pos, vals) in gear_vals.items():
        if len(vals) == 2:
            ratio_sum += vals[0] * vals[1]

    print(ratio_sum)

def gears_around(grid, i, j, k):
    for z in range(j-1, k+1):
        if grid[i-1][z] == '*': yield (i-1, z)
        if grid[i+1][z] == '*': yield (i+1, z)
    if grid[i][j-1] == '*': yield (i, j-1)
    if grid[i][k] == '*': yield (i, k)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
