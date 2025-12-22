#!/usr/bin/env -S uv run

from aoclib import util

def solution(input_lines):

    part1_ans, part2_ans = 0, 0

    for line in input_lines:
        val, _, nums = line.partition(":")
        val = int(val)
        nums = [int(s) for s in nums.split()]

        if possible(val, nums, reduce_part1):
            part1_ans += val
            part2_ans += val
        elif possible(val, nums, reduce_part2):
            part2_ans += val

    return (part1_ans, part2_ans)

def possible(goal, nums, reduce):
    vals = { goal }
    for num in reversed(nums[1:]):
        vals = set(reduce(num, vals))
    return (nums[0] in vals)

def reduce_part1(num, vals):
    for ov in vals:
        yield ov - num
        if not ov % num: yield ov // num

def reduce_part2(num, vals):
    k = 10**len(str(num))
    for ov in vals:
        yield ov - num
        if not ov % num: yield ov // num
        if ov % k == num: yield ov // k

if __name__ == "__main__": util.run_solution(solution)
