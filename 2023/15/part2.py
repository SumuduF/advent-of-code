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
    return (''.join(lines)).split(",")

def solve(task):
    boxes = [[] for _ in range(256)]
    focal = dict()
    for step in task:
        if step[-1] == "-":
            label = step[:-1]
            box_num = hash(label)
            if label in boxes[box_num]:
                boxes[box_num].remove(label)
        else:
            label, _, val = step.partition("=")
            box_num = hash(label)
            focal[label] = int(val)
            if label not in boxes[box_num]:
                boxes[box_num].append(label)

    ans = 0
    for i in range(256):
        for (j, lens) in enumerate(boxes[i]):
            ans += (i+1) * (j+1) * focal[lens]
    return ans

def hash(s):
    val = 0
    for c in s:
        val = 17*(val + ord(c))
        val %= 256
    return val

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
