from aoclib import util

def solution(grid):
    h, w = len(grid), len(grid[0]) # the grids are actually square
    # two parts are quite different, couldn't think of much to re-use
    return (solve_part1(grid, h, w), solve_part2(grid, h, w))

def solve_part1(grid, h, w):
    # XMAS can't overlap with itself so str.count works wonderfully
    def contrib(s):
        s = "".join(s)
        return s.count("XMAS") + s.count("SAMX")

    def walk(r, c, dr, dc):
        while (0 <= r < h) and (0 <= c < w):
            yield grid[r][c]
            r += dr
            c += dc

    ans = 0
    # all horiz
    ans += sum(contrib(row) for row in grid)
    # all vert
    ans += sum(contrib(walk(0, c, 1, 0)) for c in range(w))
    # all diag \
    ans += sum(contrib(walk(0, c, 1, 1)) for c in range(w))
    ans += sum(contrib(walk(r, 0, 1, 1)) for r in range(1, h))
    # all diag /
    ans += sum(contrib(walk(h-1, c, -1, 1)) for c in range(w))
    ans += sum(contrib(walk(r, 0, -1, 1)) for r in range(h-1))

    return ans

def solve_part2(grid, h, w):
    ans = 0
    MS = set("MS")
    for i in range(1, h-1):
        for j in range(1, w-1):
            if grid[i][j] != "A": continue
            if {grid[i-1][j-1], grid[i+1][j+1]} != MS: continue
            if {grid[i-1][j+1], grid[i+1][j-1]} != MS: continue
            ans += 1
    return ans

if __name__ == "__main__": util.run_solution(solution)
