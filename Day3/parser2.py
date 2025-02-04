import re

fn = 'input.txt'
mods = []
with open(fn, 'r') as f:
    for line in f:
        # Grab our input strings
        mods.extend(re.findall(r'mul\(\d+,\d+\)|do\(\)|don\'t\(\)', line))

print(mods)

total = 0
do = True
for m in mods:
    if m == 'do()':
        do = True
    elif m == "don't()":
        do = False
    else:
        if do:
            nums = re.split(r',', m)

            total += int(re.sub(r'[^\d]', '', nums[0])) *  int(re.sub(r'[^\d]', '', nums[1]))

print(total);