import argparse
import sys

def main(filename):
    lines = read_file(filename)
    task = parse_task(lines)
    answer = solve(*task)

    print(answer)

def read_file(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f]
    return lines

def parse_task(lines):
    stars = []
    empty_rows = list()
    empty_cols = list()

    n = len(lines)
    m = len(lines[0])
    for i in range(n):
        for j in range(m):
            if lines[i][j] == "#":
                stars.append((i, j))

    for i in range(n):
        if not any(s[0] == i for s in stars):
            empty_rows.append(i)

    for j in range(m):
        if not any(s[1] == j for s in stars):
            empty_cols.append(j)

    return (stars, empty_rows, empty_cols)

def solve(stars, empty_rows, empty_cols):
    remap = []
    for (i, j) in stars:
        i += sum(1 for r in empty_rows if r < i)
        j += sum(1 for c in empty_cols if c < j)
        remap.append((i, j))

    dist = 0
    k = len(remap)
    for a in range(k):
        for b in range(a+1, k):
            i1, j1 = remap[a]
            i2, j2 = remap[b]
            dist += abs(i1-i2) + abs(j1-j2)
    return dist

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
