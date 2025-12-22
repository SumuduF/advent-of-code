#!/usr/bin/env -S uv run

from aoclib import util

def solution(lines):
    part1_ans = 0
    part2_ans = 0

    pos = 50
    for line in lines:
        num = int(line[1:])

        full, rest = divmod(num, 100)
        part2_ans += full

        match line[0]:
            case "L":
                if 0 < pos <= rest: part2_ans += 1
                pos = (pos - rest) % 100
            case "R":
                if 100-rest <= pos: part2_ans += 1
                pos = (pos + rest) % 100

        if pos == 0: part1_ans += 1

    return (part1_ans, part2_ans)

if __name__ == "__main__": util.run_solution(solution)
