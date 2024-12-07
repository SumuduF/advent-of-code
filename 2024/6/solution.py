from aoclib import util

def solution(grid):
    x, y = find(grid, "^")

    spots = route(grid, x, y)
    part1_ans = len(spots)

    part2_ans = 0
    for spot in spots:
        if (spot != (x, y)) and not route(grid, x, y, spot):
            part2_ans += 1

    return (part1_ans, part2_ans)

def route(grid, x, y, block=None):
    h, w = len(grid), len(grid[0])
    dirs = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    seen = set()
    d = 0

    seen.add((x, y, d))
    nx, ny = x+dirs[d][0], y+dirs[d][1]
    while (0 <= nx < h) and (0 <= ny < w):
        if (grid[nx][ny] == "#") or ((nx, ny) == block):
            d = (d+1) % 4
        else:
            x, y = nx, ny
            if (x, y, d) in seen: return None
        seen.add((x, y, d))
        nx, ny = x+dirs[d][0], y+dirs[d][1]
    return set((x, y) for (x, y, _) in seen)

def find(grid, z):
    for (i, row) in enumerate(grid):
        for (j, char) in enumerate(row):
            if char == z: return (i, j)

if __name__ == "__main__": util.run_solution(solution)
