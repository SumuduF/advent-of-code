from aoclib import util

def solution(lines):
    part1_ans = 0
    part2_ans = 0

    for line in lines:
        bank = [int(c) for c in line]
        n = len(bank)

        # jolt[k][i] = jolt value taking k digits from first i digits of bank
        # base cases are jolt[0][*] = 0, jolt[k][i<k] = 0
        jolt = [[0] * (n+1) for _ in range(12+1)]
        for k in range(1, 12+1):
            for i in range(k, n+1):
                jolt[k][i] = max(jolt[k][i-1], 10*jolt[k-1][i-1] + bank[i-1])

        part1_ans += jolt[2][n]
        part2_ans += jolt[12][n]

    return (part1_ans, part2_ans)

if __name__ == "__main__": util.run_solution(solution)
