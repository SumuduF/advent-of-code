from aoclib import util
from aoclib import grids

def solution(lines):
    layers = []
    locs = set(loc for (loc, val) in grids.gnumerate(lines) if val == "@")
    while freed := list(free(locs)):
        layers.append(len(freed))
        locs.difference_update(freed)

    return (layers[0], sum(layers))

def free(locs):
    for loc in locs:
        around = sum(z in locs for z in grids.neighbors8(loc))
        if around < 4: yield loc

if __name__ == "__main__": util.run_solution(solution)
