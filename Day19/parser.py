import re
import pprint

fn = 'input.txt'

towelFlag = False
towels = []
with open(fn, 'r') as f:
    for line in f:
        line = line.strip()
        if line == '':
            towelFlag = True
        elif not towelFlag:
            patterns = line.split(', ')
        else:
            towels.append(line)

longestPattern = len(max(patterns, key=len))

# startSize is the size of stripe we're looking for at beginning of towel
# curSize is the size of the next stripe we're looking for
def findPattern(towel, restTowel, size):
    good = False

    # Get stripe of current size
    stripe = restTowel[:size]

    # We found last remaining stripe, we're good!
    if len(restTowel) == 0:
        return True

    # Otherwise keep checking other size stripes
    while size <= len(restTowel) and size <= longestPattern:
        if stripe in patterns:
            # We have the pattern, check the rest of the towel starting with size 1 again
            good = findPattern(towel, restTowel[size:], 1)
            if good:
                return good

        # Get stripe of next size
        size = size + 1
        stripe = restTowel[:size]

    # We've reached max size and haven't matched all patterns
    return False

canBeMade = 0
for towel in towels:
    good = findPattern(towel, towel, 1)
    if good:
        print(towel)
    canBeMade = canBeMade + good
print(canBeMade)