from aoclib import util
from aoclib.parsing import regex

def solution(lines):
    ranges, ingredients = util.line_groups(lines)

    range_parser = regex("([0-9]+)-([0-9]+)").zipconv(int, int)
    fresh = [range_parser.parse(s) for s in ranges]
    fresh.sort()

    part1_ans = 0
    for v in ingredients:
        v = int(v)
        if any(a <= v <= b for (a, b) in fresh): part1_ans += 1

    part2_ans = 0
    last_end = -1
    for (a, b) in fresh:
        if b <= last_end: continue
        a = max(a, last_end+1)
        last_end = b
        part2_ans += b-a+1

    return (part1_ans, part2_ans)

if __name__ == "__main__": util.run_solution(solution)
