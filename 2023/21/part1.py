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
    return lines

def solve(task):
    n, m = len(task), len(task[0])

    seen = set()
    q = []
    def try_push(r, c):
        if (0 <= r < n) and (0 <= c < m) and (task[r][c] != "#"):
            if (r, c) not in seen:
                seen.add((r, c))
                q.append((r, c))

    cur = 0
    sr, sc = findS(task, n, m)
    try_push(sr, sc)
    while cur < 64:
        pq, q = q, []
        cur += 1
        for (r, c) in pq:
            try_push(r+1, c)
            try_push(r-1, c)
            try_push(r, c+1)
            try_push(r, c-1)

    ans = 0
    for (r, c) in seen:
        if (abs(r - sr) + abs(c - sc)) % 2 == 0:
            ans += 1
    return ans

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
