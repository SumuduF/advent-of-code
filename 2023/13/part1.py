import argparse
import sys

def main(filename):
    lines = read_file(filename)
    task = parse_task(lines)
    answer = solve(task)

    print(answer)

def read_file(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f]
    return lines

def parse_task(lines):
    grids = [[]]
    for line in lines:
        if line:
            grids[-1].append(line)
        else:
            grids.append([])
    return grids

def solve(task):
    result = 0
    for grid in task:
        h_line = find_h_line(grid)
        if h_line is not None:
            result += 100 * h_line
        else:
            v_line = find_v_line(grid)
            result += v_line

    return result

def find_h_line(grid):
    n = len(grid)
    for i in range(1, n):
        if all(grid[i-1-k] == grid[i+k] for k in range(min(i, n-i))):
            return i
    return None

def find_v_line(grid):
    v_grid = []
    for j in range(len(grid[0])):
        v_grid.append(''.join(row[j] for row in grid))
    return find_h_line(v_grid)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
