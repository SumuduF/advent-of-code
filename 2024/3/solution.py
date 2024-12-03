from aoclib import util
from functools import cache

def solution(input_lines):
    part1_ans = 0
    part2_ans = 0

    enabled = True
    for token in prog_parser().parse(" ".join(input_lines)):
        match token:
            case (a, b):
                part1_ans += a * b
                if enabled: part2_ans += a * b
            case bool(val):
                enabled = val

    return (part1_ans, part2_ans)

@cache
def prog_parser():
    from aoclib.parsing import regex, ex, chomp, star
    mul = regex(r"mul\(([0-9]+),([0-9]+)\)").zipconv(int, int)
    do = ex("do()").const(True)
    dont = ex("don't()").const(False)
    garbage = chomp(1).skip()

    # must try garbage last since it will match anything
    return star(mul | do | dont | garbage)

if __name__ == "__main__": util.run_solution(solution)
