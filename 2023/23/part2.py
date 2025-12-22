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
    return [list(line) for line in lines]

def solve(task):
    # gulp; just brute force?
    sys.setrecursionlimit(1000000000)
    n, m = len(task), len(task[0])

    sr, sc = 0, 0
    while task[sr][sc] != ".":
        sc += 1

    def neighbors(r, c):
        if r > 0: yield (r-1, c)
        if c > 0: yield (r, c-1)
        if r < n-1: yield (r+1, c)
        if c < m-1: yield (r, c+1)

    adj = [[None] * m for _ in range(n)]
    for r in range(n):
        for c in range(m):
            if task[r][c] != "#":
                adj[r][c] = list()
                for (nr, nc) in neighbors(r, c):
                    if task[nr][nc] != "#":
                        adj[r][c].append((nr, nc))

    best_ans = 0
    cur_steps = 0
    def explore(r, c):
        nonlocal best_ans
        nonlocal cur_steps

        if r == (n-1):
            if cur_steps > best_ans:
                best_ans = cur_steps
                print(best_ans)
            return

        task[r][c] = "#"
        cur_steps += 1
        for (nr, nc) in adj[r][c]:
            if task[nr][nc] != "#":
                explore(nr, nc)
        task[r][c] = "."
        cur_steps -= 1

    explore(sr, sc)
    return best_ans

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
