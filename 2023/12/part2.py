import argparse
import itertools
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
    task = []
    for line in lines:
        record, nums = line.split()
        record = "?".join([record]*5) + "." # sentinel for "finishing" last group
        nums = list(map(int, nums.split(","))) * 5
        task.append((record, nums))
    return task

def solve(task):
    return sum(ways(record, nums) for (record, nums) in task)

def ways(record, nums):
    n = len(record)
    k = len(nums)

    # memo[i][j] is # of ways to complete if I've finished i groups and I'm at position j in the record
    memo = [[None] * n for _ in range(k)] 

    def calc(i, j):
        if j >= n: return int(i == k)
        if i == k: return int(all(c != "#" for c in record[j:]))
        if memo[i][j] is None:
            if record[j] == ".":
                memo[i][j] = calc(i, j+1)
            else:
                # To make a group here we must have the next characters look like "#####."; that dictates
                # any "?" inside so we just need to check for blockers
                group_ways = 0
                end = j + nums[i]
                if (end > n) or any(c == "." for c in record[j:end]) or (record[end] == "#"):
                    group_ways = 0
                else:
                    group_ways = calc(i+1, end+1)

                if record[j] == "#":
                    memo[i][j] = group_ways
                else:
                    memo[i][j] = group_ways + calc(i, j+1)

        return memo[i][j]

    return calc(0, 0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
