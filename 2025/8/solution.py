from aoclib import util, struct
from aoclib.struct import Point3
from collections import defaultdict

def solution(lines):
    boxes = []
    for line in lines:
        a, b, c = map(int, line.split(","))
        boxes.append(Point3(a, b, c))

    pair_dists = []
    n = len(boxes)
    for i in range(n):
        for j in range(i+1, n):
            delta = boxes[i] - boxes[j]
            pair_dists.append((delta.dot(delta), i, j))
    pair_dists.sort()

    # union-find (simple version)
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

    pair_it = iter(pair_dists)
    count = n

    part_one_len = 1000 if n > 100 else 10
    for _ in range(part_one_len):
        _, i, j = next(pair_it)
        count -= unite(i, j)

    ss = sorted(size[i] for i in range(n) if rep[i] == i)
    part1_ans = ss[-1] * ss[-2] * ss[-3]

    while count > 1:
        _, i, j = next(pair_it)
        count -= unite(i, j)

    part2_ans = boxes[i].x * boxes[j].x

    return (part1_ans, part2_ans)

if __name__ == "__main__": util.run_solution(solution)
