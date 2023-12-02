import argparse
import sys
from collections import defaultdict

def main(filename):
    with open(filename, "r") as f:
        games = [line.strip() for line in f]

    total = 0
    for game in games:
        head, _, tail = game.partition(":")
        game_id = int(head.removeprefix("Game "))
        if possible_game(tail):
            total += game_id

    print(total)

def possible_game(game_str):
    hands = game_str.split(";")
    return all(possible_hand(hand) for hand in hands)

def possible_hand(hand_str):
    groups = hand_str.split(",")
    counts = defaultdict(int)
    for group in groups:
        num, _, color = group.strip().partition(" ")
        counts[color] += int(num)

    # check for extra colors
    colors = set(counts.keys())
    colors.discard("red")
    colors.discard("green")
    colors.discard("blue")
    if len(colors) > 0: return False

    return (counts["red"] <= 12) and (counts["green"] <= 13) and (counts["blue"] <= 14)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
