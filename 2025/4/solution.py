from aoclib import util
from aoclib import grids

def solution(lines):
    layers = []
    locs = set(loc for (loc, val) in grids.gnumerate(lines) if val == "@")
    possibles = locs

    while True:
        peeled, possibles = peel_layer(locs, possibles)
        if not peeled: break

        layers.append(len(peeled))
        locs.difference_update(peeled)

    return (layers[0], sum(layers))

def peel_layer(locs, possibles):
    peeled = []
    adjacents = set()

    for loc in possibles:
        around = [z for z in grids.neighbors8(loc) if z in locs]
        if len(around) < 4:
            peeled.append(loc)
            adjacents.update(around)

    adjacents.difference_update(peeled)
    return (peeled, adjacents)

if __name__ == "__main__": util.run_solution(solution)
