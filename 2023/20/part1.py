import argparse
import sys
from collections import defaultdict

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
    nodes = dict()
    for line in lines:
        name, _, dests = line.partition(" -> ")
        mtype = None
        if (name[0] == "&") or (name[0] == "%"):
            mtype = name[0]
            name = name[1:]
        dests = tuple(d.strip() for d in dests.split(","))
        nodes[name] = (mtype, dests)
    return nodes

def solve(nodes):
    flipmem = defaultdict(bool)
    conmem = dict()
    connodes = [name for name in nodes if nodes[name][0] == "&"]
    for cnode in connodes:
        conmem[cnode] = dict()
        for name in nodes:
            if cnode in nodes[name][1]:
                conmem[cnode][name] = False

    lo_count = 0
    hi_count = 0
    for _ in range(1000):
        lo_inc, hi_inc = push(nodes, flipmem, conmem)
        lo_count += lo_inc
        hi_count += hi_inc
    return lo_count * hi_count

def push(nodes, flipmem, conmem):
    lo, hi = 0, 0

    q = [("button", "broadcaster", False)]
    while q:
        pq, q = q, []
        for (sender, name, pulse) in pq:
            if pulse: hi += 1
            else: lo += 1

            if name not in nodes: continue

            if nodes[name][0] == None:
                q.extend((name, dest, pulse) for dest in nodes[name][1])
            elif nodes[name][0] == "%":
                if not pulse:
                    val = not flipmem[name]
                    flipmem[name] = val
                    q.extend((name, dest, val) for dest in nodes[name][1])
            elif nodes[name][0] == "&":
                conmem[name][sender] = pulse
                val = not all(conmem[name].values())
                q.extend((name, dest, val) for dest in nodes[name][1])

    return (lo, hi)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
