import argparse
import sys

def main(filename):
    grid = [""]
    with open(filename, "r") as f:
        grid.extend(("." + line.strip() + ".") for line in f)
    m = len(grid[1])
    grid[0] = ("." * m)
    grid.append(grid[0])
    n = len(grid)

    total = 0
    i, j = 0, 0
    while i < n:
        if grid[i][j].isnumeric():
            k = j
            while grid[i][k].isnumeric(): k += 1

            if has_symbol(grid, i, j, k):
                total += int(grid[i][j:k])
            j = k
        else: j += 1

        if j == m: i, j = i+1, 0

    print(total)

def has_symbol(grid, i, j, k):
    for c in surround(grid, i, j, k):
        if (c != '.') and not c.isnumeric():
            return True
    return False

def surround(grid, i, j, k):
    for z in range(j-1, k+1):
        yield grid[i-1][z]
        yield grid[i+1][z]
    yield grid[i][j-1]
    yield grid[i][k]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
