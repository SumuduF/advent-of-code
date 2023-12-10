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
    k = len(lines[0])
    grid = [("." * (k+2))]
    for line in lines:
        grid.append("." + line + ".")
    grid.append(grid[0])
    return grid

def solve(grid):
    s_loc = None
    n, m = len(grid), len(grid[0])
    for i in range(n):
        for j in range(m):
            if grid[i][j] == "S":
                s_loc = (i, j)
                break
        if s_loc is not None: break

    dists = [[None] * m for _ in range(n)]
    dists[s_loc[0]][s_loc[1]] = 0

    q = []
    for i in range(n):
        for j in range(m):
            if s_loc in neighbors(grid, i, j):
                q.append((i, j))
                dists[i][j] = 1

    while q:
        nq = []
        for (i, j) in q:
            for (ii, jj) in neighbors(grid, i, j):
                if dists[ii][jj] is None:
                    dists[ii][jj] = dists[i][j] + 1
                    nq.append((ii, jj))
        q = nq

    return max(dists[i][j] for i in range(n) for j in range(m) if dists[i][j] is not None)

def neighbors(grid, r, c):
    if grid[r][c] == "|":
        yield (r-1, c)
        yield (r+1, c)
    elif grid[r][c] == "-":
        yield (r, c-1)
        yield (r, c+1)
    elif grid[r][c] == "L":
        yield (r-1, c)
        yield (r, c+1)
    elif grid[r][c] == "J":
        yield (r-1, c)
        yield (r, c-1)
    elif grid[r][c] == "7":
        yield (r+1, c)
        yield (r, c-1)
    elif grid[r][c] == "F":
        yield (r+1, c)
        yield (r, c+1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
