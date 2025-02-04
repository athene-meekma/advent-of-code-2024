import pprint

test = 0
if test == 1:
    fn = 'test.txt'
elif test == 2:
    fn = 'test2.txt'
else:
    fn = 'input.txt'

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

def doAnd(val1, val2):
    return val1 and val2

def doOr(val1, val2):
    return val1 or val2

def doXor(val1, val2):
    return val1 ^ val2

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

        match operation['operator']:
            case 'AND':
                values[operation['output']] = doAnd(val1, val2)
            case 'OR':
                values[operation['output']] = doOr(val1, val2)
            case 'XOR':
                values[operation['output']] = doXor(val1, val2)
        del(gates[pointer])
    else:
        # Values not yet set, try next
        pointer = pointer + 1

i = 'z00'
count = 0
binary = ''
while i in values:
    binary = str(values[i]) + binary
    count = count + 1
    i = 'z'+str(count).rjust(2, '0')

print(binary)
print(int(binary, 2))