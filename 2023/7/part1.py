#!/usr/bin/env -S uv run

import argparse
import sys

def main(filename):
    lines = read_file(filename)
    task = parse_task(lines)
    answer = solve(task)

    print(answer)

def read_file(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f]
    return lines

def parse_task(lines):
    hands = []
    for line in lines:
        hand, bid = line.split()
        hands.append((hand, int(bid)))
    return hands

def solve(task):
    ranked = sorted((hand_value(hand), bid) for (hand, bid) in task)

    score = 0
    for (i, z) in enumerate(ranked):
        score += (i+1) * z[1]
    return score

def hand_value(hand):
    return (hand_type(hand), tuple(card_val(c) for c in hand))

def hand_type(hand):
    shand = sorted(hand)
    if shand[0] == shand[4]: return 6

    if shand[0] == shand[3]: return 5
    if shand[1] == shand[4]: return 5

    if (shand[0] == shand[2]) and (shand[3] == shand[4]): return 4
    if (shand[0] == shand[1]) and (shand[2] == shand[4]): return 4

    if (shand[0] == shand[2]): return 3
    if (shand[1] == shand[3]): return 3
    if (shand[2] == shand[4]): return 3

    num_pairs = 0
    for i in range(4):
        if shand[i] == shand[i+1]: num_pairs += 1

    return num_pairs

def card_val(card):
    if card.isnumeric(): return int(card)

    if card == 'T': return 10
    if card == 'J': return 11
    if card == 'Q': return 12
    if card == 'K': return 13
    if card == 'A': return 14

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
