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
    # seeds
    _, _, seed_list = lines[0].partition(":")
    seed_nums = list(map(int, seed_list.strip().split()))

    lines.append("") # sentinel val
    # seed-to-soil
    pos = 3
    seed_to_soil = []
    while len(lines[pos]) > 0:
        seed_to_soil.append(tuple(map(int, lines[pos].split())))
        pos += 1

    # soil-to-fertilizer
    pos += 2
    soil_to_fert = []
    while len(lines[pos]) > 0:
        soil_to_fert.append(tuple(map(int, lines[pos].split())))
        pos += 1
    # fertilizer-to-water
    pos += 2
    fert_to_water = []
    while len(lines[pos]) > 0:
        fert_to_water.append(tuple(map(int, lines[pos].split())))
        pos += 1
    # water-to-light
    pos += 2
    water_to_light = []
    while len(lines[pos]) > 0:
        water_to_light.append(tuple(map(int, lines[pos].split())))
        pos += 1
    # light-to-temp
    pos += 2
    light_to_temp = []
    while len(lines[pos]) > 0:
        light_to_temp.append(tuple(map(int, lines[pos].split())))
        pos += 1
    # temp-to-hum
    pos += 2
    temp_to_hum = []
    while len(lines[pos]) > 0:
        temp_to_hum.append(tuple(map(int, lines[pos].split())))
        pos += 1
    # hum-to-loc
    pos += 2
    hum_to_loc = []
    while len(lines[pos]) > 0:
        hum_to_loc.append(tuple(map(int, lines[pos].split())))
        pos += 1

    return (seed_nums,
            [seed_to_soil, soil_to_fert, fert_to_water, water_to_light, light_to_temp, temp_to_hum, hum_to_loc])

def solve(task):
    seed_nums, maps = task

    min_loc = None
    for seed in seed_nums:
        loc = seed
        for idmap in maps:
            loc = lookup(loc, idmap)
        if (min_loc is None) or (loc < min_loc):
            min_loc = loc
    return min_loc

def lookup(val, idmap):
    for (dst, src, k) in idmap:
        if src <= val < (src+k):
            return val - src + dst
    return val

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
