import numpy as np

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

def checkOrder(update, ordering):
    isGood = True
    newUpdate = update.copy()

    for pageIndex, page in enumerate(update):
        if page in ordering:
            lowestIndex = None
            # For each page that must occur after
            for order in ordering[page]:
                if order in update and update.index(order) < pageIndex:
                    isGood = False
                    if lowestIndex is None or update.index(order) < lowestIndex:
                        # Find the lowest index of any page that needs to appear after
                        lowestIndex = update.index(order)

            if lowestIndex is not None:
                del newUpdate[pageIndex]
                newUpdate = newUpdate[:lowestIndex] + [page] + newUpdate[lowestIndex:]
    return isGood, newUpdate

sum = 0
newUpdates = []

for update in updates:
    isGood = False
    newUpdate = update.copy()

    count = 0
    while not isGood:
        count = count + 1
        isGood, newUpdate = checkOrder(newUpdate, ordering)

    if count > 1:
        # Only count the updates that weren't good to begin with
        newUpdates.append(newUpdate)

# Calculate the sum of the middle numbers
for newUpdate in newUpdates:
    middle = int((len(newUpdate) - 1) / 2)
    sum += newUpdate[middle]

print(sum)