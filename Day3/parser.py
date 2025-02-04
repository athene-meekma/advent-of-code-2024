import re

fn = 'input.txt'
mods = []
with open(fn, 'r') as f:
    for line in f:
        # Grab our input strings
        mods.extend(re.findall(r'mul\(\d+,\d+\)', line))

print(mods)

total = 0
for m in mods:
    nums = re.split(r',', m)

    total += int(re.sub(r'[^\d]', '', nums[0])) *  int(re.sub(r'[^\d]', '', nums[1]))

print(total);