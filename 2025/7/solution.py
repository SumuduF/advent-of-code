from aoclib import util
from collections import defaultdict

def solution(lines):
    active = defaultdict(int)
    active[lines[0].index("S")] = 1

    splits = 0
    for row in lines[1:]:
        # copy items since we will be mutating active in this loop
        for (i, v) in list(active.items()):
            if row[i] == "^":
                splits += 1
                del active[i]
                active[i-1] += v
                active[i+1] += v

    return (splits, sum(active.values()))

if __name__ == "__main__": util.run_solution(solution)
