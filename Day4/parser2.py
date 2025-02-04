import re

fn = 'input.txt'

rows = []
with open(fn, 'r') as f:
    for line in f:
        # Grab our input strings
        rows.append(line.strip())

count = 0
centers = []

# Find the location of all As (centers)
for i, row in enumerate(rows):
    for j, v in enumerate(row):
        if v.lower() == 'a':
            centers.append((i, j))

for a in centers:
    diagDown = diagUp = ''

    # Starting row and col nums
    rowNum = a[0]
    colNum = a[1]

    if rowNum - 1 >= 0 and colNum - 1 >= 0:
        diagDown = rows[rowNum - 1][colNum - 1]

    if rowNum + 1 < len(rows) and colNum - 1 >= 0:
        diagUp = rows[rowNum + 1][colNum - 1]

    diagDown += 'a'
    diagUp   += 'a'

    if rowNum + 1 < len(rows) and colNum + 1 < len(rows[rowNum + 1]):
        diagDown += rows[rowNum + 1][colNum + 1]

    if rowNum - 1 >= 0 and colNum + 1 < len(rows[rowNum - 1]):
        diagUp += rows[rowNum - 1][colNum + 1]

    count += (diagDown.lower() == 'mas' or diagDown.lower() == 'sam') and (diagUp.lower() == 'mas' or diagUp.lower() == 'sam')
print(count)