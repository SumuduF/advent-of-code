#!/usr/bin/env -S uv run

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

    p1, v1 = pts[0], vels[0]
    for i in range(1, n):
        if indep(v1, vels[i]):
            p2, v2 = pts[i], vels[i]
            break
    for j in range(i+1, n):
        if indep(v1, vels[j]) and indep(v2, vels[j]):
            p3, v3 = pts[j], vels[j]
            break

    rock, S = find_rock(p1, v1, p2, v2, p3, v3)
    return sum(rock) / S

def find_rock(p1, v1, p2, v2, p3, v3):
    a, A = find_plane(p1, v1, p2, v2)
    b, B = find_plane(p1, v1, p3, v3)
    c, C = find_plane(p2, v2, p3, v3)

    w = lin(A, cross(b, c), B, cross(c, a), C, cross(a, b))
    t = dot(a, cross(b, c))
    # given that w is integer, so force it here to avoid carrying through imprecision
    # rest of the computation is integer except the final division
    w = Vec3(round(w.x / t), round(w.y / t), round(w.z / t))

    w1 = sub(v1, w)
    w2 = sub(v2, w)
    ww = cross(w1, w2)

    E = dot(ww, cross(p2, w2))
    F = dot(ww, cross(p1, w1))
    G = dot(p1, ww)
    S = dot(ww, ww)

    rock = lin(E, w1, -F, w2, G, ww)
    return (rock, S)

def find_plane(p1, v1, p2, v2):
    p12 = sub(p1, p2)
    v12 = sub(v1, v2)
    vv = cross(v1, v2)
    return (cross(p12, v12), dot(p12, vv))

def cross(a, b):
    return Vec3(a.y*b.z - a.z*b.y, a.z*b.x - a.x*b.z, a.x*b.y - a.y*b.x)

def dot(a, b):
    return a.x*b.x + a.y*b.y + a.z*b.z

def sub(a, b):
    return Vec3(a.x-b.x, a.y-b.y, a.z-b.z)

def lin(r, a, s, b, t, c):
    x = r*a.x + s*b.x + t*c.x
    y = r*a.y + s*b.y + t*c.y
    z = r*a.z + s*b.z + t*c.z
    return Vec3(x, y, z)

def indep(a, b):
    return any(v != 0 for v in cross(a, b))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
