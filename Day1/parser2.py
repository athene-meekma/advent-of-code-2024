import re
import numpy as np

fn = 'input.txt'
a = []
with open(fn, 'r') as f:
    for line in f:
        nums = re.split(r'\s+', line.strip())
        a.append([int(nums[0]), int(nums[1])])

a = np.asarray(a)
col1 = np.sort(a[:,0])
col2 = np.sort(a[:,1]).tolist()

counts = {}
sum = 0
for i in range(len(col1)):
    if col1[i] not in counts:
        counts[col1[i]] = col2.count(col1[i])

    sum += ( (col1[i]) * counts[col1[i]] )

print(sum)