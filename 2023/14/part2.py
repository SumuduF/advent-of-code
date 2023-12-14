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

def solve(grid):
    n, m = len(grid), len(grid[0])

    goal = 1000000000
    cur = 0
    seen = dict()
    seen[tuplize(grid)] = cur
    
    while cur < goal:
        cycle(grid, n, m)
        cur += 1
        tup = tuplize(grid)

        if tup in seen: break
        seen[tup] = cur

    if cur < goal:
        delt = cur - seen[tup]
        goal -= cur
        goal %= delt

        while goal > 0:
            cycle(grid, n, m)
            goal -= 1

    return load(grid, n, m)

def load(grid, n, m):
    ans = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] == "O":
                ans += n-i
    return ans

def cycle(grid, n, m):
    # north
    for j in range(m):
        nxt = 0
        for i in range(n):
            if grid[i][j] == "O":
                grid[nxt][j] = "O"
                if nxt != i: grid[i][j] = "."
                nxt += 1
            elif grid[i][j] == "#":
                nxt = i+1
    # west
    for i in range(n):
        nxt = 0
        for j in range(m):
            if grid[i][j] == "O":
                grid[i][nxt] = "O"
                if nxt != j: grid[i][j] = "."
                nxt += 1
            elif grid[i][j] == "#":
                nxt = j+1
    # south
    for j in range(m):
        nxt = n-1
        for i in reversed(range(n)):
            if grid[i][j] == "O":
                grid[nxt][j] = "O"
                if nxt != i: grid[i][j] = "."
                nxt -= 1
            elif grid[i][j] == "#":
                nxt = i-1
    # east
    for i in range(n):
        nxt = m-1
        for j in reversed(range(m)):
            if grid[i][j] == "O":
                grid[i][nxt] = "O"
                if nxt != j: grid[i][j] = "."
                nxt -= 1
            elif grid[i][j] == "#":
                nxt = j-1

def tuplize(grid):
    return tuple(tuple(row) for row in grid)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
