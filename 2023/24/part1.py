import argparse
import collections
import sys

def main(filename):
    lines = read_file(filename)
    task = parse_task(lines)
    answer = solve(*task)

    print(answer)

def read_file(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f]
    return lines

Vec3 = collections.namedtuple("Vec3", "x,y,z", defaults = (0, 0, 0))

def parse_task(lines):
    pts = []
    vels = []
    for line in lines:
        p, _, v = line.partition("@")
        pts.append(Vec3(*map(int, p.split(","))))
        vels.append(Vec3(*map(int, v.split(","))))
    return (pts, vels)

def solve(pts, vels):
    n = len(pts)

    min_c = 200000000000000
    max_c = 400000000000000
    ans = 0
    for i in range(n):
        for j in range(i+1, n):
            ip = intersection(pts[i], vels[i], pts[j], vels[j])
            if (ip is not None) and (min_c <= ip.x <= max_c) and (min_c <= ip.y <= max_c):
                ans += 1
    return ans

def intersection(p1, v1, p2, v2):
    # p1 + rv1 == p2 + sv2
    # p1 - p2 == sv2 - rv1
    # (p1 - p2) x v1 = s (v2 x v1)
    # (p1 - p2) x v2 = -r (v1 x v2) = r (v2 x v1)

    cv = cross2(v2, v1)

    if cv == 0: return None

    dp = Vec3(p1.x-p2.x, p1.y-p2.y, p1.z-p2.z)
    s = cross2(dp, v1) / cv
    r = cross2(dp, v2) / cv
    if s < 0 or r < 0: return None

    return Vec3(p1.x+r*v1.x, p1.y+r*v1.y, p1.z+r*v1.z)

def cross2(a, b):
    return a.x*b.y - a.y*b.x

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
