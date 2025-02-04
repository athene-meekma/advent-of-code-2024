import re
import functools

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
@functools.cache
def findPattern(restTowel, size, count=0):
    # Get stripe of current size
    stripe = restTowel[:size]

    # We found last remaining stripe, we're good!
    if len(restTowel) == 0:
        count = count + 1
        return count

    # Otherwise keep checking other size stripes
    while size <= len(restTowel) and size <= longestPattern:
        if stripe in patterns:
            # We have the pattern, check the rest of the towel starting with size 1 again
            count = count + findPattern(restTowel[size:], 1)
            if count > 0 and size == len(restTowel):
                return count

        # Get stripe of next size
        size = size + 1
        stripe = restTowel[:size]
    # We've reached max size and haven't matched all patterns
    return count

possibleCombos = 0
for towel in towels:
    print('======== '+towel+' ========')
    count = findPattern(towel, 1)
    print(count)
    possibleCombos = possibleCombos + count
print(possibleCombos)