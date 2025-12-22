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
    ans = 0
    start_part = { "x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000) }
    start_wf = "in"

    q = [(start_wf, start_part)]
    while q:
        pq, q = q, []
        for (wf, part) in pq:
            for (nwf, npart) in apply_workflow(part, workflows[wf]):
                if nwf == "R": continue
                if nwf == "A":
                    ans += cardinality(npart)
                    continue
                q.append((nwf, npart))
    return ans

def cardinality(part):
    ans = 1
    for (a, b) in part.values():
        ans *= (b - a + 1)
    return ans

def apply_workflow(part, steps, i = 0):
    step = steps[i]
    if isinstance(step, str):
        yield (step, part)
    else:
        (a, b) = part[step[0]]
        if step[1] == "<":
            # test = z < step[2]
            if step[2] <= a:
                yield from apply_workflow(part, steps, i+1)
            elif step[2] <= b:
                partA = part.copy()
                partB = part.copy()
                partA[step[0]] = (a, step[2]-1)
                partB[step[0]] = (step[2], b)
                yield (step[3], partA)
                yield from apply_workflow(partB, steps, i+1)
            else: # b < step[2]
                yield (step[3], part)
        else:
            # test = z > step[2]
            if step[2] < a:
                yield (step[3], part)
            elif step[2] < b:
                partA = part.copy()
                partB = part.copy()
                partA[step[0]] = (a, step[2])
                partB[step[0]] = (step[2]+1, b)
                yield from apply_workflow(partA, steps, i+1)
                yield (step[3], partB)
            else: # b <= step[2]
                yield from apply_workflow(part, steps, i+1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
