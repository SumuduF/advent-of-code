#!/usr/bin/env -S uv run

from aoclib import util
from functools import cache

def solution(lines):
    g = dict()
    for line in lines:
        s, rest = line.split(":")
        g[s] = rest.split()

    # (0 checkpoints, 1 checkpoint, 2 checkpoints)
    @cache
    def paths_from(u):
        if u == "out": return (1, 0, 0)

        ret = [0]*3
        for v in g.get(u, []):
            for (i, z) in enumerate(paths_from(v)):
                ret[i] += z

        # shift counts up if we hit a checkpoint
        if (u == "fft") or (u == "dac"):
            ret.insert(0, 0)
            ret.pop()
        return tuple(ret)

    part1_ans = sum(paths_from("you"))
    part2_ans = paths_from("svr")[-1]

    return (part1_ans, part2_ans)

if __name__ == "__main__": util.run_solution(solution)
