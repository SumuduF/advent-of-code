from aoclib import util, struct
from aoclib.struct import Point3
from collections import defaultdict, deque

def solution(lines):
    boxes = []
    for line in lines:
        a, b, c = map(int, line.split(","))
        boxes.append(Point3(a, b, c))
    boxes.sort()

    # union-find (simple version)
    n = len(boxes)
    rep = list(range(n))
    size = [1] * n
    def find(i):
        while rep[i] != i:
            i = rep[i]
        return i
    def unite(i, j):
        i, j = find(i), find(j)
        if i == j: return False
        rep[j] = i
        size[i] += size[j]
        return True

    pair_it = gen_pair_dists(boxes)
    count = n

    part_one_len = 1000 if n > 100 else 10
    for _ in range(part_one_len):
        i, j = next(pair_it)
        count -= unite(i, j)

    ss = sorted(size[i] for i in range(n) if rep[i] == i)
    part1_ans = ss[-1] * ss[-2] * ss[-3]

    while count > 1:
        i, j = next(pair_it)
        count -= unite(i, j)

    part2_ans = boxes[i].x * boxes[j].x

    return (part1_ans, part2_ans)

# assumes boxes sorted by x
def gen_pair_dists(boxes):
    # finds all pairs separated by a distance in [lo, hi)
    def bounded_scan(lo, hi):
        lo2, hi2 = lo*lo, hi*hi
        active = deque()
        for (i, p) in enumerate(boxes):
            while active and active[0][1].x <= p.x - hi:
                active.popleft()
            for (j, q) in active:
                delta = p - q
                z = delta.dot(delta)
                if lo2 <= z < hi2: yield (z, i, j)
            active.append((i, p))

    # first power of 2 that finds something for our data, but even using hi=1
    # here works ok
    lo, hi = 0, 2048
    while True:
        yield from ((i, j) for (_, i, j) in sorted(bounded_scan(lo, hi)))
        lo, hi = hi, hi*2

if __name__ == "__main__": util.run_solution(solution)
