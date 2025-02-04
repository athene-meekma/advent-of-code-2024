fn = 'test2.txt'

A = None
B = None
C = None
with open(fn, 'r') as f:
    for line in f:
        line = line.strip()
        if line != '':
            parts = line.split(': ')
            if line.startswith('Register'):
                exec(parts[0][9] + " = "+parts[1])
            else:
                instructions = parts[1]

def doOperation(opcode, operand):
    global A
    global B
    global C
    global i
    global increment

    result = None

    if opcode in [0, 6, 7]:
        # Division
        val = A / (2 ** operand)
        parts = str(val).split('.')
        newVal = int(parts[0])

        if opcode == 0:
            A = newVal
        elif opcode == 6:
            B = newVal
        else:
            C = newVal
    elif opcode == 1:
        newVal = B ^ operand
        B = newVal
    elif opcode == 2:
        newVal = operand % 8
        B = newVal
    elif opcode == 3:
        if A != 0:
            i = operand
            increment = False
    elif opcode == 4:
        newVal = B ^ C
        B = newVal
    elif opcode == 5:
        result = operand % 8

    return result

instructions = list(map(int, instructions.split(',')))

count = 0
i = 0
increment = True
results = []
while i < len(instructions) - 1:
    count = count + 1
    startI = i
    opcode = instructions[i]
    operand = instructions[i+1]

    if operand == 7:
        print('Invalid operand encountered')
        break

    if opcode != 3:
        if operand == 4:
            operand = A
        elif operand == 5 and opcode != 1:
            operand = B
        elif operand == 6:
            operand = C
    result = doOperation(opcode, operand)

    if result != None:
        results.append(str(result))

    if increment:
        i = i + 2
    else:
        increment = True

print(','.join(results))