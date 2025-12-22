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
    task = []
    for line in lines:
        parts = line.split()
        task.append((parts[0], int(parts[1]), parts[2]))
    return task

def solve(task):
    vertices = [(0, 0)]
    for (direction, dist, _) in task:
        x, y = vertices[-1]
        if direction == "R":
            x += dist
        elif direction == "L":
            x -= dist
        elif direction == "D":
            y += dist
        elif direction == "U":
            y -= dist
        vertices.append((x, y))

    min_x = min(x for (x, y) in vertices)
    max_x = max(x for (x, y) in vertices)
    min_y = min(y for (x, y) in vertices)
    max_y = max(y for (x, y) in vertices)

    lx = max_x - min_x
    ly = max_y - min_y

    grid = [["."] * (ly + 3) for _ in range(lx + 3)]
    sx, sy = min_x - 1, min_y - 1
    px, py = vertices[-1]
    for (x, y) in vertices:
        if x != px:
            for xx in range(min(x, px), max(x, px)+1):
                grid[xx-sx][y-sy] = "#"
        elif y != py:
            for yy in range(min(y, py), max(y, py)+1):
                grid[x-sx][yy-sy] = "#"
        px, py = x, y

    grid[0][0] = " "
    q = [(0, 0)]
    def try_push(x, y):
        if 0 <= x < len(grid) and 0 <= y < len(grid[0]):
            if grid[x][y] == ".":
                grid[x][y] = " "
                q.append((x, y))
    while q:
        pq, q = q, []
        for (x, y) in pq:
            try_push(x+1, y)
            try_push(x-1, y)
            try_push(x, y+1)
            try_push(x, y-1)

    return sum(1 for row in grid for c in row if c != " ")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
