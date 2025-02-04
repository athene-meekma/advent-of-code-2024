import pprint

fn = 'input.txt'

def restart():
    gates = []
    values = {}
    valEnd = False
    with open(fn, 'r') as f:
        for line in f:
            line = line.strip()
            if line == '':
                valEnd = True
            elif not valEnd:
                parts = line.split(': ')
                values[parts[0]] = int(parts[1])
            else:
                parts = line.split(' ')
                gates.append({
                    'val1': parts[0],
                    'operator': parts[1],
                    'val2': parts[2],
                    'output': parts[4]
                })
    return gates, values

def doAnd(val1, val2):
    return val1 and val2

def doOr(val1, val2):
    return val1 or val2

def doXor(val1, val2):
    return val1 ^ val2

gates, values = restart()

def process(swaps):
    pointer = 0
    while len(gates) > 0:
        # If we hit the end, start over
        if pointer >= len(gates):
            pointer = 0

        operation = gates[pointer]
        if operation['val1'] in values and operation['val2'] in values:
           # We have the necessary values, perform the operation
            val1 = values[operation['val1']]
            val2 = values[operation['val2']]

            if operation['output'] in swaps:
                out = swaps[operation['output']]
            else:
                out = operation['output']

            match operation['operator']:
                case 'AND':
                    values[out] = doAnd(val1, val2)
                case 'OR':
                    values[out] = doOr(val1, val2)
                case 'XOR':
                    values[out] = doXor(val1, val2)
            del(gates[pointer])
        else:
            # Values not yet set, try next
            pointer = pointer + 1

process([])

def showResults(values):
    i = 'x00'
    count = 0
    xBin = ''
    while i in values:
        xBin = str(values[i]) + xBin
        count = count + 1
        i = 'x'+str(count).rjust(2, '0')
    print('xBin:  '+xBin + ' ('+str(int(xBin, 2)) + ')' )

    i = 'y00'
    count = 0
    yBin = ''
    while i in values:
        yBin = str(values[i]) + yBin
        count = count + 1
        i = 'y'+str(count).rjust(2, '0')
    print('yBin:  '+yBin + ' ('+str(int(yBin, 2)) + ')' )

    i = 'z00'
    count = 0
    zBin = ''
    while i in values:
        zBin = str(values[i]) + zBin
        count = count + 1
        i = 'z'+str(count).rjust(2, '0')
    print('zBin: '+zBin + ' ('+str(int(zBin, 2)) + ')' )

    # Get sum of x + y
    zAct = bin(int(xBin, 2) + int(yBin, 2))
    print('zAct: '+zAct[2:] + ' ('+str(int(zAct[2:], 2)) + ')' )

    t = bin(abs(int(zAct[2:], 2) - int(zBin, 2)))
    print('t:              '+t[2:])

    problemAreas = []
    for j, v in enumerate(t):
        if v == '1':
            problemAreas.append('z'+str(len(t)-j-2))

    return problemAreas

problemAreas = showResults(values)

gates, values = restart()

def getRelated(result):
    related = []
    for gate in gates:
        if gate['output'] == result:
            related.append(gate['val1'])
            related.append(gate['val2'])
    return related

for problem in problemAreas:
    problemAreas.extend(getRelated(problem))

problemAreas = list(set(problemAreas))

swaps1 = {}
for problem in problemAreas:
    areas = problemAreas.copy()
    i = areas.index(problem)
    del(areas[i])
    swaps1[problem] = areas

swaps2 = swaps1.copy()
swaps3 = swaps1.copy()
swaps4 = swaps1.copy()

for k, swap1 in swaps1.items():
    swaps = {}
    next = swap1.pop()
    swaps[k] = next
    swaps[next] = k
    #print(swaps)
    for k2, swap2 in swaps2.items():
        if k2 in swaps:
            continue
        next = swap2.pop()
        swaps[k] = next
        swaps[next] = k
        print(swaps)