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
    seed_ranges = []
    for i in range(0, len(seed_nums), 2):
        seed_ranges.append((seed_nums[i], seed_nums[i] + seed_nums[i+1] - 1))

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

    return (seed_ranges,
            [seed_to_soil, soil_to_fert, fert_to_water, water_to_light, light_to_temp, temp_to_hum, hum_to_loc])

def solve(task):
    seed_ranges, maps = task

    ranges = seed_ranges
    for idmap in maps:
        new_ranges = []
        for rng in ranges:
            new_ranges.extend(lookup(rng, idmap))
        ranges = new_ranges
    return min(a for (a, _) in ranges)

def lookup(rng, idmap, pos=0):
    a, b = rng
    for i in range(pos, len(idmap)):
        dst, src, k = idmap[i]

        if b < src: continue
        if a >= (src+k): continue

        if a < src: yield from lookup((a, src-1), idmap, pos+1)
        if b >= (src+k): yield from lookup((src+k, b), idmap, pos+1)

        a = max(a, src)
        b = min(b, src+k-1)
        yield (a - src + dst, b - src + dst)
        break
    else: yield (a, b)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs="?", default="input.txt")
    args = parser.parse_args()
    sys.exit(main(args.filename))
