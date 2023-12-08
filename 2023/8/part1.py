import argparse
import itertools
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
    directions = lines[0]

    graph = dict()
    for node in lines[2:]:
        z = node[0:3]
        l = node[7:10]
        r = node[12:15]
        graph[z] = (l, r)
    return (directions, graph)

def solve(task):
    directions, graph = task

    cur = "AAA"
    steps = 0
    next_dir = itertools.cycle(directions)

    while cur != "ZZZ":
        d = next(next_dir)
        if d == "L":
            cur = graph[cur][0]
        else:
            cur = graph[cur][1]
        steps += 1
    return steps

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
