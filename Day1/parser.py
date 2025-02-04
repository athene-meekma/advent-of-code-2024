import re
import numpy as np

fn = 'input.txt'
a = []
with open(fn, 'r') as f:
    for line in f:
        a.append(re.split(r'\s+', line.strip()))

a = np.asarray(a)
col1 = np.sort(a[:,0])
col2 = np.sort(a[:,1])

sum = 0
for i in range(len(col1)):
    sum += abs(int(col1[i]) - int(col2[i]))

print(sum)