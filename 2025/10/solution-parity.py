#!/usr/bin/env -S uv run

from aoclib import util
from functools import cache
from collections import defaultdict
from itertools import combinations

def solution(lines):
    part1_ans = 0
    part2_ans = 0
    for line in lines:
        lights, buttons, joltages = machine_parser().parse(line)

        parity_ways = defaultdict(list)
        nl = len(lights)
        nb = len(buttons)
        for pressed in range(nb+1):
            for subset in combinations(buttons, pressed):
                val = [0] * nl
                for button in subset:
                    for z in button:
                        val[z] += 1
                parity = tuple(v & 1 for v in val)
                parity_ways[parity].append((pressed, tuple(val)))

        @cache
        def min_presses(jolts):
            if not any(jolts): return 0

            parity = tuple(j & 1 for j in jolts)
            best = 1E100
            for (presses, val) in parity_ways[parity]:
                if any(v > j for (v, j) in zip(val, jolts)): continue
                new_jolts = tuple((j-v) // 2 for (v, j) in zip(val, jolts))
                best = min(best, presses + 2 * min_presses(new_jolts))
            return best

        part1_ans += min(p for (p, _) in parity_ways[lights])
        part2_ans += min_presses(joltages)

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
