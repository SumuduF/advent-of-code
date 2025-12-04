from aoclib import util

def solution(lines):
    part1_ans = sum(joltage(line, 2) for line in lines)
    part2_ans = sum(joltage(line, 12) for line in lines)
    return (part1_ans, part2_ans)

def joltage(bank, m):
    # track digits to keep in a stack; a higher digit is always better until it
    # would leave too few digits in total
    digits = []

    n = len(bank)
    for (i, c) in enumerate(bank):
        lim = max(0, m - n + i)
        while (len(digits) > lim) and (digits[-1] < c):
            digits.pop()
        if len(digits) < m:
            digits.append(c)

    return int("".join(digits))

if __name__ == "__main__": util.run_solution(solution)
