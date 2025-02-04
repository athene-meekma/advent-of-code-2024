fn = 'input.txt'

B = None
C = None

startB = None
startC = None

results = ''
i = 0
count = 0
increment = True
with open(fn, 'r') as f:
    for line in f:
        line = line.strip()
        if line != '':
            parts = line.split(': ')
            if line.startswith('Register B'):
                B = int(parts[1])
                startB = B
            elif line.startswith('Register C'):
                C = int(parts[1])
                startC = C
            elif line.startswith('Program'):
                instString = parts[1]
                instructions = list(map(int, instString.split(',')))

newA = 6 * (8 ** (len(instructions)-1) )
#newA = 216058692944094
#newA = 216058692944092 (mod 6 is 2)
#newA = 216058692944112 # (mod 6 and mod 8 is 0)
A = newA

def restart(newA):
    global A
    global B
    global C
    global i
    global count
    global increment
    global results

    results = ''
    i = 0
    count = 0
    increment = True
    A = newA
    B = startB
    C = startC
    return

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

digits = 3
mod = 10 ** (len(str(newA)) - 3)
print(mod)
print(newA)
print(instString[len(instString)-digits:])
found = False
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
        if results == '':
            results = str(result)
        else:
            results = results + ',' + str(result)
    if increment:
        i = i + 2
    else:
        increment = True

    if instString == results:
        found = True
        break
    elif i >= len(instructions) - 1:
        if results.endswith(instString[len(instString)-digits:]):
            newA = newA - mod # Set back to the previous value
            if mod > 1:
                mod = int(mod / 10) # Decrease our modifier
            digits = digits + 2 # Increase the number of digits we're looking for
            print('=========== Found Partial ===========')
            print(results)
        elif len(results) > len(instString):
            # We've gone too far, start over
            print('=========== Too high ===========')
            if mod > 1:
                mod = int(mod / 10) # Decrease our modifier
            newA = 0

        newA = newA + mod
        restart(newA)

print(newA)
print(results)