import argparse
import heapq
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
    return [[int(c) for c in line] for line in lines]

def solve(task):
    n, m = len(task), len(task[0])
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def poss(val, prev_dir, r, c):
        for i in range(4):
            if (i != (prev_dir ^ 1)) and (i != prev_dir):
                dr, dc = dirs[i]
                nval = val
                for j in range(10):
                    nr, nc = r + (j+1)*dr, c + (j+1)*dc
                    if (0 <= nr < n) and (0 <= nc < m):
                        nval += task[nr][nc]
                    else:
                        break

                    if (j >= 3):
                        yield (nval, i, nr, nc)

    q = []
    heapq.heappush(q, (0, 4, 0, 0))
    prune = dict()
    while q:
        val, prev_dir, r, c = heapq.heappop(q)
        if (r == n-1) and (c == m-1): return val
        for (nval, ndir, r, c) in poss(val, prev_dir, r, c):
            if ((ndir, r, c) not in prune) or (nval < prune[(ndir, r, c)]):
                prune[(ndir, r, c)] = nval
                heapq.heappush(q, (nval, ndir, r, c))

    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
