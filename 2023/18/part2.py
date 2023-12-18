import argparse
import sys
import bisect

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
        task.append((int(parts[2][-2:-1]), int(parts[2][2:-2], 16)))
    return task

def solve(task):
    vertices = [(0, 0)]
    for (direction, dist) in task:
        x, y = vertices[-1]
        if direction == 0:
            x += dist
        elif direction == 2:
            x -= dist
        elif direction == 1:
            y += dist
        elif direction == 3:
            y -= dist
        vertices.append((x, y))

    x_coords = set(x for (x, y) in vertices)
    x_coords.update(x + 1 for (x, y) in vertices)
    x_coords = sorted(x_coords)

    y_coords = set(y for (x, y) in vertices)
    y_coords.update(y + 1 for (x, y) in vertices)
    y_coords = sorted(y_coords)

    cvertices = []
    for (x, y) in vertices:
        cx = bisect.bisect_left(x_coords, x)
        cy = bisect.bisect_left(y_coords, y)
        cvertices.append((cx, cy))

    grid = [["."] * (len(y_coords) + 2) for _ in range(len(x_coords) + 2)]
    px, py = cvertices[-1]
    for (x, y) in cvertices:
        if x != px:
            for xx in range(min(x, px), max(x, px)+1):
                grid[xx+1][y+1] = "#"
        elif y != py:
            for yy in range(min(y, py), max(y, py)+1):
                grid[x+1][yy+1] = "#"
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

    area = 0
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            if grid[x][y] != " ":
                area += (x_coords[x] - x_coords[x-1]) * (y_coords[y] - y_coords[y-1])

    return area


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
