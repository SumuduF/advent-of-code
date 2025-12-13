from aoclib import util
from aoclib.grids import gnumerate, grid_getter
from aoclib.struct import Point2

def solution(lines):
    *boxes, regions = util.line_groups(lines)
    presents = [read_present(box) for box in boxes]
    return sum(can_fill(region, presents) for region in regions)

def read_present(box):
    box = box[1:] # ignore label

    # assumed elsewhere
    assert len(box) <= 3
    assert all(len(row) <= 3 for row in box)

    orientations = set()
    pts = [pos for (pos, ch) in gnumerate(box) if ch == "#"]
    for _ in range(4):
        orientations.add(canonical(pts))
        pts = rotate(pts)
    pts = flip(pts)
    for _ in range(4):
        orientations.add(canonical(pts))
        pts = rotate(pts)
    return tuple(orientations)

def canonical(pts):
    z = min(pts)
    return tuple(sorted(p-z for p in pts))

def rotate(pts): return [Point2(-y, x) for (x, y) in pts]
def flip(pts): return [Point2(-x, y) for (x, y) in pts]

def can_fill(region, presents):
    dims, counts = region.split(": ")
    w, h = map(int, dims.split("x"))
    counts = list(map(int, counts.split()))

    # trivial case if region can fit each present in a 3x3
    easy_fit = (w // 3) * (h // 3)
    if sum(counts) <= easy_fit: return True

    # trivial case if the grid doesn't have enough cells
    # the # of extra cells is also used in pruning the recursion
    slack = w*h
    for (i, p) in enumerate(presents):
        slack -= counts[i] * len(p[0])
    if slack < 0: return False

    occ = [[False]*h for _ in range(w)]
    g = grid_getter(occ, True)
    locs = [loc for (loc, _) in gnumerate(occ)]

    # note: mutates "occ" and "counts", and must ensure to clean up after
    # itself when backtracking
    def recurse(z, slack, to_place):
        if to_place == 0: return True

        while (z < len(locs)) and g(locs[z]): z += 1
        if z == len(locs): return False

        for (i, p) in enumerate(presents):
            if not counts[i]: continue
            counts[i] -= 1
            for option in p:
                pts = [locs[z]+pt for pt in option]
                if any(g(pt) for pt in pts): continue
                for pt in pts:
                    occ[pt.x][pt.y] = True
                if recurse(z+1, slack, to_place-1): return True
                for pt in pts:
                    occ[pt.x][pt.y] = False
            counts[i] += 1

        # may only skip this cell if we have slack
        return (slack > 0) and recurse(z+1, slack-1, to_place)

    return recurse(0, slack, sum(counts))

if __name__ == "__main__": util.run_solution(solution)
