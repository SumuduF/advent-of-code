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
    grids = [[]]
    for line in lines:
        if line:
            grids[-1].append(list(line))
        else:
            grids.append([])
    return grids

def solve(task):
    return sum(smudged_val(grid) for grid in task)

def smudged_val(grid):
    orig_val = next(find_vals(grid))
    n, m = len(grid), len(grid[0])
    for i in range(n):
        for j in range(m):
            grid[i][j] = opp(grid[i][j])
            for val in find_vals(grid):
                if val != orig_val:
                    return val[0] * val[1]
            grid[i][j] = opp(grid[i][j])
    return None

def opp(c):
    if c == ".":
        return "#"
    else:
        return "."

def find_vals(grid):
    for h_line in find_h_lines(grid):
        yield (100, h_line)
    for v_line in find_v_lines(grid):
        yield (1, v_line)

def find_h_lines(grid):
    n = len(grid)
    for i in range(1, n):
        if all(grid[i-1-k] == grid[i+k] for k in range(min(i, n-i))):
            yield i

def find_v_lines(grid):
    v_grid = []
    for j in range(len(grid[0])):
        v_grid.append([row[j] for row in grid])
    yield from find_h_lines(v_grid)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
