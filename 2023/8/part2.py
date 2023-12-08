import argparse
import itertools
import sys
import math

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

    # LCM of cycle lengths is not even remotely guaranteed to work...but it does work for the data in question.
    # Each "A" node only encounters one (unique) "Z" node in its circuit
    # The "directions" cycles line up with the "Z" such that we can skip tracking that too (unused offset param for follow())
    # The # of steps from A to Z just happens to be same as the cycle length from Z to Z (even though the A node is
    # not part of the cycle!)

    # The right way would be CRT (and we'd also have to deal with multiple Z options for each circuit...) but I could
    # not get that to work properly (yet). Another way to look at it is that the properties above make it so that the
    # CRT formulation has a particular form that can be simplified into LCM.

    lens = []
    for node in graph:
        if node[-1] == "A":
            lens.append(0)
            found_z = None
            for nxt in follow(node, graph, directions, 0):
                if found_z: lens[-1] += 1

                if nxt[-1] == "Z":
                    if not found_z:
                        found_z = nxt
                    elif found_z == nxt:
                        break

    return math.lcm(*lens)

def step(node, graph, d):
    if d == "L":
        return graph[node][0]
    else:
        return graph[node][1]

def follow(node, graph, directions, offset):
    next_dir = itertools.cycle(directions[offset:] + directions[:offset])
    while True:
        d = next(next_dir)
        node = step(node, graph, d)
        yield node

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
