#!/usr/bin/env -S uv run

from aoclib import util
from functools import cache
import z3

def solution(lines):
    part1_ans = 0
    part2_ans = 0
    for line in lines:
        lights, buttons, joltages = machine_parser().parse(line)

        opt = z3.Optimize()
        b_count = z3.IntVector("b_count", len(buttons))
        opt.add(z >= 0 for z in b_count)
        outputs = []
        for j in range(len(joltages)):
            my_buttons = [i for (i, b) in enumerate(buttons) if j in b]
            outputs.append(z3.Sum(b_count[j] for j in my_buttons))

        min_presses = opt.minimize(z3.Sum(b_count))

        opt.push()
        opt.add(out % 2 == light for (out, light) in zip(outputs, lights))
        opt.check()
        part1_ans += min_presses.value().as_long()

        opt.pop()
        opt.add(out == jolt for (out, jolt) in zip(outputs, joltages))
        opt.check()
        part2_ans += min_presses.value().as_long()

    return (part1_ans, part2_ans)

@cache
def machine_parser():
    from aoclib.parsing import ex, regex, seplist, star

    num = regex("[0-9]+").conv(int)
    nums = seplist(num, ",").conv(tuple)

    light = ex(".").const(0) | ex("#").const(1)

    lights = ex("[") + star(light).conv(tuple) + ex("]")
    buttons = star(ex("(") + nums + ex(")")).conv(tuple)
    joltages = ex("{") + nums + ex("}")

    return lights + buttons + joltages

if __name__ == "__main__": util.run_solution(solution)
