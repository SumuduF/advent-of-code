#!/usr/bin/env -S uv run

import argparse
import sys
from collections import defaultdict

def main(filename):
    with open(filename, "r") as f:
        games = [line.strip() for line in f]

    total = 0
    for game in games:
        _, _, tail = game.partition(":")
        total += min_power(tail)

    print(total)

COLORS = ["red", "green", "blue"]

def min_power(game_str):
    hands = game_str.split(";")
    min_counts = defaultdict(int)
    for hand in hands:
        counts = cube_counts(hand)
        for color in COLORS:
            min_counts[color] = max(min_counts[color], counts[color])
    result = 1
    for color in COLORS:
        result *= min_counts[color]
    return result

def cube_counts(hand_str):
    groups = hand_str.split(",")
    counts = defaultdict(int)
    for group in groups:
        num, _, color = group.strip().partition(" ")
        counts[color] += int(num)

    return counts

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
