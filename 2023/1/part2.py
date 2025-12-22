#!/usr/bin/env -S uv run

DIGMAP = {
  "one" : 1, "1" : 1,
  "two" : 2, "2" : 2,
  "three" : 3, "3" : 3,
  "four" : 4, "4" : 4,
  "five" : 5, "5" : 5,
  "six" : 6, "6" : 6,
  "seven" : 7, "7" : 7,
  "eight" : 8, "8" : 8,
  "nine" : 9, "9" : 9,
  "0" : 0
}

def extractDigit(line):
    for (k, v) in DIGMAP.items():
        if line.startswith(k):
            return (v, line[1:])
    return (None, line[1:])

f = open("input.txt", "r")

vals = []
for line in f:
    digits = []
    while len(line) > 0:
        dig, rest = extractDigit(line)
        if dig is not None: digits.append(dig)
        line = rest
    vals.append(10*digits[0] + digits[-1])

f.close()

print(sum(vals))
