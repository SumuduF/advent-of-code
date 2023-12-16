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
    n, m = len(task), len(task[0])

    # state is row, col, dr, dc
    seen = set()
    q = list()
    def push(row, col, dr, dc):
        if not 0 <= row < n: return
        if not 0 <= col < m: return

        state = (row, col, dr, dc)
        if state not in seen:
            q.append(state)
            seen.add(state)

    push(0, 0, 0, 1)
    while q:
        pq = q
        q = []
        for (row, col, dr, dc) in pq:
            for (nrow, ncol, ndr, ndc) in propagate(task, row, col, dr, dc):
                push(nrow, ncol, ndr, ndc)

    return len(set((row, col) for (row, col, _, _) in seen))

def propagate(task, r, c, dr, dc):
    if task[r][c] == ".": yield (r + dr, c + dc, dr, dc)
    elif task[r][c] == "/":
        dr, dc = -dc, -dr
        yield (r + dr, c + dc, dr, dc)
    elif task[r][c] == "\\":
        dr, dc = dc, dr
        yield (r + dr, c + dc, dr, dc)
    elif dr == 0: # horizontal
        if task[r][c] == "-": yield (r + dr, c + dc, dr, dc)
        else:
            yield (r + 1, c, 1, 0)
            yield (r - 1, c, -1, 0)
    else: # vertical
        if task[r][c] == "|": yield (r + dr, c + dc, dr, dc)
        else:
            yield (r, c + 1, 0, 1)
            yield (r, c - 1, 0, -1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
