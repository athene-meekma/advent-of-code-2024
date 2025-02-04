import re
import numpy as np

fn = 'input.txt'
arr = []
with open(fn, 'r') as f:
    for line in f:
        # Grab our input strings
        nums = re.split(r'\s+', line.strip())
        # Convert array to integers
        arr.append(list(map(int, nums)))

good = 0
for report in arr:
    prev = None
    diff = None
    increasing = None

    safe = True
    for v in report:
        if prev is not None:
            diff = prev - v
            if increasing is None:
                increasing = v > prev

        if diff is not None:
            if abs(diff) == 0 or abs(diff) > 3 or (increasing and prev >= v) or (not increasing and prev <= v):
                safe = False

        prev = v

    if safe is True:
        good += 1

print(good)