from aoclib import util
from collections import defaultdict
from functools import cache

def solution(lines):
    # inverse graph
    ig = defaultdict(list)
    for line in lines:
        s, rest = line.split(":")
        for t in rest.split():
            ig[t].append(s)

    part1_ans = sum(counts_from(ig, "you"))
    part2_ans = counts_from(ig, "svr")[3]

    return (part1_ans, part2_ans)

def counts_from(ig, start):
    # (neither, "dac" only, "fft" only, both)
    @cache
    def get_counts(v):
        if v == start: return (1, 0, 0, 0)

        vals = [0]*4
        for u in ig[v]:
            for (i, z) in enumerate(get_counts(u)):
                vals[i] += z

        if v == "fft":
            return (0, 0, vals[0]+vals[2], vals[1]+vals[3])
        elif v == "dac":
            return (0, vals[0]+vals[1], 0, vals[2]+vals[3])
        else:
            return tuple(vals)

    return get_counts("out")

if __name__ == "__main__": util.run_solution(solution)
