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

def solve(orig, steps=26501365):
    task = expand(orig)
    n, m = len(task), len(task[0])

    dist = [[None] * m for _ in range(n)]

    q = []
    def try_push(r, c, d):
        if (0 <= r < n) and (0 <= c < m) and (task[r][c] != "#"):
            if dist[r][c] is None:
                dist[r][c] = d
                q.append((r, c))

    cur = 0
    sr, sc = findS(task, n, m)
    try_push(sr, sc, cur)
    while q:
        pq, q = q, []
        cur += 1
        for (r, c) in pq:
            try_push(r+1, c, cur)
            try_push(r-1, c, cur)
            try_push(r, c+1, cur)
            try_push(r, c-1, cur)

    ans = 0
    for i in range(n):
        for j in range(m):
            if (dist[i][j] is not None) and (dist[i][j] <= steps) and ((steps - dist[i][j]) % 2 == 0):
                ans += 1

    nn, mm = len(orig), len(orig[0])
    off = (n // nn) // 2
    def coords_for_copy(a, b, i, j):
        return ((off+a)*nn + i, (off+b)*mm + j)

    a = -off # top edge
    for b in range(-off+1, off):
        for i in range(nn):
            for j in range(mm):
                ii, jj = coords_for_copy(a, b, i, j)
                if (dist[ii][jj] is not None) and (dist[ii][jj] < steps):
                    # assume dist to copy z shifts above is = dist[ii][jj] + z * nn
                    # nn is odd so the parity switches with each shift
                    max_z = (steps - dist[ii][jj]) // nn
                    if (steps - dist[ii][jj]) % 2 == 0:
                        ans += max_z // 2
                    else:
                        ans += (max_z + 1) // 2
    a = off # bottom edge
    for b in range(-off+1, off):
        for i in range(nn):
            for j in range(mm):
                ii, jj = coords_for_copy(a, b, i, j)
                if (dist[ii][jj] is not None) and (dist[ii][jj] < steps):
                    max_z = (steps - dist[ii][jj]) // nn
                    if (steps - dist[ii][jj]) % 2 == 0:
                        ans += max_z // 2
                    else:
                        ans += (max_z + 1) // 2
    b = -off # left edge
    for a in range(-off+1, off):
        for i in range(nn):
            for j in range(mm):
                ii, jj = coords_for_copy(a, b, i, j)
                if (dist[ii][jj] is not None) and (dist[ii][jj] < steps):
                    max_z = (steps - dist[ii][jj]) // nn
                    if (steps - dist[ii][jj]) % 2 == 0:
                        ans += max_z // 2
                    else:
                        ans += (max_z + 1) // 2
    b = off # right edge
    for a in range(-off+1, off):
        for i in range(nn):
            for j in range(mm):
                ii, jj = coords_for_copy(a, b, i, j)
                if (dist[ii][jj] is not None) and (dist[ii][jj] < steps):
                    max_z = (steps - dist[ii][jj]) // nn
                    if (steps - dist[ii][jj]) % 2 == 0:
                        ans += max_z // 2
                    else:
                        ans += (max_z + 1) // 2

    # corners
    for (a, b) in [(-off, -off), (-off, off), (off, -off), (off, off)]:
        for i in range(nn):
            for j in range(mm):
                ii, jj = coords_for_copy(a, b, i, j)
                if (dist[ii][jj] is not None) and (dist[ii][jj] < steps):
                    # each z value up to max_z now represents a whole diagonal of maps (z+1 of them)
                    max_z = (steps - dist[ii][jj]) // nn
                    if (steps - dist[ii][jj]) % 2 == 0:
                        # z = 2, 4, 6, ... zz
                        zz = max_z
                        if zz & 1: zz -= 1

                        if zz >= 2:
                            ans += ((zz + 4) * zz) // 4
                    else:
                        # z = 1, 3, 5, ... zz
                        zz = max_z
                        if not zz & 1: zz -= 1

                        if zz >= 1:
                            ans += ((zz + 3) * (zz + 1)) // 4

    return ans

def expand(task):
    factor = 7 # must be odd
    n, m = len(task), len(task[0])

    si, sj = findS(task, n, m)
    task[si][sj] = "."

    new = [[None] * (factor*m) for _ in range(factor*n)]
    for i in range(factor*n):
        for j in range(factor*m):
            new[i][j] = task[i % n][j % m]

    half = factor // 2
    new[si+half*n][sj+half*m] = "S"
    return new

def findS(grid, n, m):
    for i in range(n):
        for j in range(m):
            if grid[i][j] == "S":
                return (i, j)
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
