import re

fn = 'input.txt'

rows = []
with open(fn, 'r') as f:
    for line in f:
        # Grab our input strings
        rows.append(line.strip())

count = 0

columns = {}
exes = []

# Get horizontal counts
for i, row in enumerate(rows):
    # Forwards XMAS
    horizontal = re.findall(r'(?i)xmas', row)
    count += len(horizontal)
    # Backwards XMAS
    horizontal = re.findall(r'(?i)samx', row)
    count += len(horizontal)
    for j, v in enumerate(row):
        if j not in columns:
            columns[j] = ''
        columns[j] += v
        if v.lower() == 'x':
            exes.append((i, j))

# Get vertical counts
for k in columns:
    # Forwards XMAS
    vertical = re.findall(r'(?i)xmas', columns[k])
    count += len(vertical)
    # Backwards XMAS
    vertical = re.findall(r'(?i)samx', columns[k])
    count += len(vertical)

# Get diagonal counts
for x in exes:
    upBack = upFor = downBack = downFor = 'x'
    #print(x)
    # Starting row and col nums
    rowNum = x[0]
    colNum = x[1]
    for i in range(1, 4):
        upR = rowNum - i
        downR = rowNum +i
        leftC = colNum - i
        rightC = colNum + i

        if upR >= 0:
            if leftC >= 0:
                upBack   += rows[upR][leftC]
            if rightC < len(rows[upR]):
                upFor    += rows[upR][rightC]

        if downR < len(rows):
            if leftC >= 0:
                downBack += rows[downR][leftC]
            if rightC < len(rows[downR]):
                downFor  += rows[downR][rightC]

    count += (upBack.lower()   == 'xmas')
    count += (upFor.lower()    == 'xmas')
    count += (downBack.lower() == 'xmas')
    count += (downFor.lower()  == 'xmas')

print(count)