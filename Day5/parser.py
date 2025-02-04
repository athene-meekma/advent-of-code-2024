fn = 'input.txt'

data = open(fn, 'r').read()
parts = data.split('\n\n')

ordering = {}
for part in parts[0].split('\n'):
    nums = part.split('|')
    if int(nums[0]) not in ordering:
        ordering[int(nums[0])] = []
    ordering[int(nums[0])].extend([int(nums[1])])

updates  = parts[1].split('\n')

updates = []
for part in parts[1].split('\n'):
    # Convert values in array to integers
    updates.append(list(map(int, part.split(','))))

sum = 0
for update in updates:
    isGood = True
    for pageIndex, page in enumerate(update):
        if page in ordering:
            # For each page that must occur after
            for order in ordering[page]:
                if order in update:
                    if update.index(order) < pageIndex:
                        isGood = False
                        break
        if not isGood:
            #print('bad update: '+str(update))
            break

    if isGood:
        middle = int((len(update) - 1) / 2)
        sum += update[middle]

print(sum)