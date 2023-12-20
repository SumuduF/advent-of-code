import argparse
import sys
import math
from collections import defaultdict

def main(filename, probe_val):
    lines = read_file(filename)
    task = parse_task(lines)
    if probe_val is None:
        answer = solve(task)
        print(answer)
    else:
        probe(task, probe_val)

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
    # from manual debugging: there are 4 independent counters with cycles
    # 3823, 3847, 4001, 3877
    # so the answer is the lcm of these
    return math.lcm(3823, 3847, 4001, 3877)

def probe(nodes, skip=0):
    flipmem = defaultdict(bool)
    conmem = dict()
    connodes = [name for name in nodes if nodes[name][0] == "&"]
    for cnode in connodes:
        conmem[cnode] = dict()
        for name in nodes:
            if cnode in nodes[name][1]:
                conmem[cnode][name] = False

    count = 0
    while count < skip:
        push(nodes, flipmem, conmem)
        count += 1

    while True:
        push(nodes, flipmem, conmem)
        count += 1
        print(count)
        memdump(flipmem)
        input(">")

def memdump(fmem):
    def legdump(leg):
        z = ''.join(str(int(fmem[node])) for node in reversed(leg.split()))
        print(z, int(z, 2))

    legdump("gd rm sl cp qv kv jn ll kq zf bd qr")
    legdump("sr cm tm mq nt jt pq zs kc jk hh jb")
    legdump("hf jg kk dm qx pp md hs mb qb rj mm")
    legdump("mg kf xt dq qn rr nh bm kx vk vl zk")

def push(nodes, flipmem, conmem):
    q = [("button", "broadcaster", False)]
    while q:
        pq, q = q, []
        for (sender, name, pulse) in pq:
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    parser.add_argument("--probe", type=int)
    args = parser.parse_args()
    sys.exit(main(args.filename, args.probe))
