import argparse
import sys
import math

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
    _, _, times = lines[0].partition(":")
    _, _, dists = lines[1].partition(":")
    time = ''.join(times.strip().split())
    dist = ''.join(dists.strip().split())
    return (int(time), int(dist))

def solve(task):
    t, d = task
    # z(t-z) > d
    if t*t < 4*d: return 0
    lb = int(0.5*(t - math.sqrt(t*t - 4*d)))

    if lb < 0: lb = 0
    while lb*(t-lb) <= d: lb += 1

    return (t+1 - 2*lb)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
