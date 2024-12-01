from aoclib import util
from collections import Counter

def solution(input_lines):
    ps, qs = get_sorted_nums(input_lines)

    part1_ans = sum(abs(p - q) for (p, q) in zip(ps, qs))

    q_counts = Counter(qs)
    part2_ans = sum(p * q_counts[p] for p in ps)

    return (part1_ans, part2_ans)

def get_sorted_nums(lines):
    ps, qs = [], []
    for line in lines:
        p, q = line.split()
        ps.append(int(p))
        qs.append(int(q))
    ps.sort()
    qs.sort()
    return (ps, qs)

if __name__ == "__main__": util.run_solution(solution)
