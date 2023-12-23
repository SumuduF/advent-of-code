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
    # gulp
    sys.setrecursionlimit(1000000000)
    # making some assumptions about lack of loops
    n, m = len(task), len(task[0])

    sr, sc = 0, 0
    while task[sr][sc] != ".":
        sc += 1

    def neighbors(r, c):
        if r > 0: yield (r-1, c)
        if c > 0: yield (r, c-1)
        if r < n-1: yield (r+1, c)
        if c < m-1: yield (r, c+1)

    def force_step(r, c):
        if task[r][c] == ">": return (r, c+1)
        if task[r][c] == "^": return (r-1, c)
        if task[r][c] == "<": return (r, c-1)
        if task[r][c] == "v": return (r+1, c)
        return None

    def step(r, c, pr=None, pc=None):
        f = force_step(r, c)
        if f is not None: return f

        possible = []
        for (nr, nc) in neighbors(r, c):
            if ((nr, nc) != (pr, pc)) and (task[nr][nc] != "#"):
                if force_step(nr, nc) != (r, c):
                    possible.append((nr, nc))
        if not possible:
            return None
        if len(possible) == 1:
            return possible[0]
        return possible

    longest = [[None] * m for _ in range(n)]
    def calc_longest(r, c):
        if longest[r][c] is not None: return longest[r][c]

        rr, cc = r, c

        pr, pc = None, None
        steps = 0
        while r < (n-1):
            nxt = step(r, c, pr, pc)
            if isinstance(nxt, tuple):
                steps += 1
                pr, pc = r, c
                r, c = nxt[0], nxt[1]
            else: break

        if r == (n-1):
            longest[rr][cc] = steps
        else:
            # hit a fork
            best = 0
            for (nr, nc) in nxt:
                best = max(best, calc_longest(nr, nc))
            longest[rr][cc] = steps + 1 + best
        return longest[rr][cc]

    return calc_longest(sr, sc)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
