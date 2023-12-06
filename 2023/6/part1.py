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
    _, _, times = lines[0].partition(":")
    _, _, dists = lines[1].partition(":")
    return [(int(t), int(d)) for (t, d) in zip(times.strip().split(), dists.strip().split())]

def solve(task):
    answer = 1
    for (t, d) in task:
        # z(t-z) > d
        wins = 0
        for z in range(0, t+1):
            if z*(t-z) > d:
                wins += 1
        answer *= wins
    return answer

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
