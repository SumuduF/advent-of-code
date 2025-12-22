#!/usr/bin/env -S uv run

import argparse
import sys

def main(filename):
    lines = read_file(filename)
    task = parse_task(lines)
    answer = solve(*task)

    print(answer)

def read_file(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f]
    return lines

def parse_task(lines):
    workflows = dict()
    for (i, line) in enumerate(lines):
        if not line: break

        wf, _, rest = line.partition("{")
        steps = rest[:-1].split(",")

        parsed_steps = []
        for step in steps:
            if ":" in step:
                cond, _, jmp = step.partition(":")
                z = cond[0]
                cmp = cond[1]
                val = int(cond[2:])
                parsed_steps.append((z, cmp, val, jmp))
            else:
                parsed_steps.append(step)
        workflows[wf] = parsed_steps

    parts = []
    for line in lines[i+1:]:
        vals = line[1:-1].split(",")
        part = dict()
        for val in vals:
            part[val[0]] = int(val[2:])
        parts.append(part)

    return workflows, parts

def solve(workflows, parts):
    score = 0
    for part in parts:
        if accepted(part, workflows):
            score += sum(part.values())
    return score

def accepted(part, workflows):
    wf = "in"

    while (wf != "A") and (wf != "R"):
        steps = workflows[wf]
        for step in steps:
            if isinstance(step, str):
                wf = step
                break
            z = part[step[0]]
            if step[1] == "<":
                test = z < step[2]
            else:
                test = z > step[2]
            if test:
                wf = step[3]
                break

    return wf == "A"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
