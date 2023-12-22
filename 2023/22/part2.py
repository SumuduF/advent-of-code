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
    bricks = []
    for line in lines:
        a, _, b = line.partition("~")
        a = tuple(int(v) for v in a.split(","))
        b = tuple(int(v) for v in b.split(","))
        bricks.append((a, b))
    return bricks

def solve(bricks):
    # sort by increasing min-z
    bricks = sorted(bricks, key=lambda z: min(z[0][2], z[1][2]))

    max_x = max(max(x1, x2) for ((x1, _, _), (x2, _, _)) in bricks)
    max_y = max(max(y1, y2) for ((_, y1, _), (_, y2, _)) in bricks)

    heights = [[0] * (max_y+1) for _ in range(max_x+1)]
    ids = [[None] * (max_y+1) for _ in range(max_x+1)]
    sitson = [[] for _ in range(len(bricks))]

    for (i, (a, b)) in enumerate(bricks):
        floor = -1
        ax, ay = a[0], a[1]
        bx, by = b[0], b[1]
        if bx < ax: ax, bx = bx, ax
        if by < ay: ay, by = by, ay

        for x in range(ax, 1+bx):
            for y in range(ay, 1+by):
                floor = max(floor, heights[x][y])

        zinc = abs(a[2] - b[2]) + 1
        supporters = set()
        for x in range(ax, 1+bx):
            for y in range(ay, 1+by):
                if heights[x][y] == floor:
                    supporters.add(ids[x][y])
                ids[x][y] = i
                heights[x][y] = floor + zinc

        for j in supporters:
            sitson[i].append(j)

    ans = 0
    for i in range(len(bricks)):
        memo = [None] * len(bricks)
        def can_reach_ground(k):
            if k is None: return True
            if memo[k] is None:
                memo[k] = False
                for z in sitson[k]:
                    if (z != i) and can_reach_ground(z):
                        memo[k] = True
                        break
            return memo[k]

        for j in range(len(bricks)):
            if (j != i) and not can_reach_ground(j):
                ans += 1

    return ans

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
