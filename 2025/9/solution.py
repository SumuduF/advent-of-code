#!/usr/bin/env -S uv run

from aoclib import util
from aoclib.struct import Point2
from bisect import bisect

def solution(lines):
    points = []
    for line in lines:
        x, y = map(int, line.split(","))
        # x/y switched because it's faster for the shape of our data
        points.append(Point2(y, x))

    # work in compressed coordinate grid
    xcoords = sorted(set(p.x for p in points))
    ycoords = sorted(set(p.y for p in points))
    xlook = dict((x, i) for (i, x) in enumerate(xcoords))
    ylook = dict((y, i) for (i, y) in enumerate(ycoords))

    def compress(p): return Point2(xlook[p.x], ylook[p.y])

    # find x-coordinates where "insideness" changes, in each row
    # detail: we're conceptually testing points slightly above/right of the
    # integer points, so:
    # - we can ignore horizontal edges
    # - we can ignore the max y-coordinate (of candidate rectangles too)
    # - we count <= the x-coordinate of interest (bisect = bisect_right)
    ny = len(ycoords)
    cross = [[] for _ in range(ny)]
    prev = compress(points[-1])
    for cp in map(compress, points):
        if cp.x == prev.x:
            for cy in range(*util.minmax(cp.y, prev.y)):
                cross[cy].append(cp.x)
        prev = cp
    for cy in range(ny):
        cross[cy] = sorted(set(cross[cy]))

    part1_ans = 0
    part2_ans = 0
    for (i, p) in enumerate(points):
        for q in points[i+1:]:
            pq = p - q
            area = (abs(pq.x) + 1) * (abs(pq.y) + 1)

            part1_ans = max(part1_ans, area)
            if area > part2_ans and is_full(cross, compress(p), compress(q)):
                part2_ans = area

    return (part1_ans, part2_ans)

def is_full(cross, p, q):
    # for each y-coordinate, [lx, rx) must be within one "inside" segment
    lx, rx = util.minmax(p.x, q.x)
    for cy in range(*util.minmax(p.y, q.y)):
        k = bisect(cross[cy], lx)
        if not (k & 1) or cross[cy][k] < rx:
            return False
    return True

if __name__ == "__main__": util.run_solution(solution)
