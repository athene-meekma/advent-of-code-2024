import re
fn = 'input.txt'

with open(fn, 'r') as f:
    for line in f:
        input = line

#print(input)

diskMap = []
id = 0
for i, v in enumerate(input):
    if i % 2 == 0:
        # File block
        for j in range(int(v)):
            diskMap.append(str(id))
        id = id + 1
    else:
        # Free space
        for j in range(int(v)):
            diskMap.append('.')

mapIndex = 0
for i in range(len(diskMap) - 1, -1, -1):
    if diskMap[i] != '.':
        # Shift file block to beginning of disk map
        while mapIndex < len(diskMap) and diskMap[mapIndex] != '.':
            mapIndex = mapIndex + 1

        if mapIndex < len(diskMap):
            diskMap[mapIndex] = diskMap[i]
            diskMap[i] = '.'

        # If we've filled in all the gaps
        if re.search(r'^\d+\.+$', ''.join(diskMap)):
            # We're done
            break

#print(diskMap)
sum = 0
for id, val in enumerate(diskMap):
    if val == '.':
        break
    sum = sum + (id * int(val))

print(sum)