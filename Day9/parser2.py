fn = 'input.txt'

with open(fn, 'r') as f:
    for line in f:
        input = line

diskMap = []
id = 0
sizes = {}
for i, v in enumerate(input):
    if i % 2 == 0:
        # File block
        sizes[str(id)] = int(v) # Keep track of block size
        for j in range(int(v)):
            diskMap.append(str(id))
        id = id + 1
    else:
        # Free space
        for j in range(int(v)):
            diskMap.append('.')

searched = []
for i in range(len(diskMap) - 1, -1, -1):
    if diskMap[i] != '.' and not diskMap[i] in searched:
        searched.append(diskMap[i])
        blockId = diskMap[i]

        # Look for x number of . in a row
        count = 0
        found = False
        for mapIndex in range(len(diskMap)):
            if diskMap[mapIndex] == '.':
                count = count + 1
            else:
                count = 0

            if count == sizes[blockId]:
                found = True
                break

        if found:
            start = mapIndex - sizes[blockId] + 1
            if start < i:
                for j in range(sizes[blockId]):
                    diskMap[start + j] = blockId
                    diskMap[i - j] = '.'

sum = 0
for pos, id in enumerate(diskMap):
    if id != '.':
        sum = sum + (pos * int(id))

print(sum)