#!/usr/bin/env -S uv run

import argparse
import sys
from collections import defaultdict
from collections import deque

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
    edges = []
    for line in lines:
        a, _, bs = line.partition(": ")
        for b in bs.split():
            edges.append((a, b))
    return edges

def solve(task):
    flows = defaultdict(dict)
    for (u, v) in task:
        flows[u][v] = 0
        flows[v][u] = 0

    nodes = set(flows.keys())
    source = nodes.pop()
    for sink in nodes:
        flow_val = maxflow(flows, source, sink)
        if flow_val == 3:
            break
        for u in flows:
            for v in flows[u]:
                flows[u][v] = 0

    side = set()
    q = deque([source])
    while q:
        u = q.popleft()
        side.add(u)
        for v in flows[u]:
            if v not in side and (flows[u][v] < 1):
                q.append(v)
                side.add(v)

    a = len(side)
    b = len(flows.keys()) - a

    return a * b

def maxflow(flows, source, sink):
    ans = 0
    while True:
        delta = augment(flows, source, sink)
        if not delta: break
        ans += delta
    return ans

def augment(flows, source, sink):
    prev = dict()
    aug = defaultdict(int)
    aug[source] = 1E9

    q = deque([source])
    while q and not aug[sink]:
        u = q.popleft()
        for v in flows[u]:
            if not aug[v]:
                if flows[u][v] < 1:
                    prev[v] = u
                    aug[v] = min(aug[u], 1 - flows[u][v])
                    q.append(v)

    if aug[sink] > 0:
        cur = sink
        while cur != source:
            pre = prev[cur]
            flows[pre][cur] += aug[sink]
            flows[cur][pre] -= aug[sink]
            cur = pre
    return aug[sink]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
