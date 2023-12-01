f = open("input.txt", "r")

vals = []
for line in f:
    digits = [c for c in line if c.isnumeric()]
    vals.append(int(digits[0] + digits[-1]))

f.close()

print(sum(vals))
