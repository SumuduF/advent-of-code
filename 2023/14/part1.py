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
    load = 0
    n, m = len(task), len(task[0])

    for j in range(m):
        nxt_load = n
        for i in range(n):
            if task[i][j] == "O":
                load += nxt_load
                nxt_load -= 1
            elif task[i][j] == "#":
                nxt_load = n-i-1

    return load

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
