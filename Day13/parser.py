import pprint

fn = 'input.txt'

count = 0
machines = [{}]
with open(fn, 'r') as f:
    for line in f:
        line = line.strip()
        if line == '':
            # New machine
            count = count + 1
            machines.append({})
        else:
            config = line.split(': ')
            if config[0].startswith('Button'):
                button = config[0].split(' ')[1]
                moves = config[1].split(', ')
                machines[count][button] = {}
                machines[count][button]['X'] = int(moves[0].replace('X+', '').replace(',', ''))
                machines[count][button]['Y'] = int(moves[1].replace('Y+', '').replace(',', ''))
            else:
                # Prize
                coords = config[1].split(', ')
                machines[count][config[0]] = {}
                machines[count][config[0]]['X'] = int(coords[0].replace('X=', ''))
                machines[count][config[0]]['Y'] = int(coords[1].replace('Y=', ''))

costA = 3
costB = 1
#pprint.pprint(machines)

count = 0
totalCost = 0
for machine in machines:
    xModA = machine['A']['X']
    yModA = machine['A']['Y']
    xMaxA = int(machine['Prize']['X'] / xModA)
    yMaxA = int(machine['Prize']['Y'] / yModA)
    # Max times we can press A
    maxA = xMaxA if xMaxA < yMaxA else yMaxA
    if(maxA > 100):
        print('maxA '+ str(maxA))

    xModB = machine['B']['X']
    yModB = machine['B']['Y']
    xMaxB = int(machine['Prize']['X'] / xModB)
    yMaxB = int(machine['Prize']['Y'] / yModB)
    # Max times we can press B
    maxB = xMaxB if xMaxB < yMaxB else yMaxB
    if(maxB > 100):
        print('maxB '+ str(maxB))

    for pressB in range(maxB, 0, -1):
        xPosB = xModB * pressB
        yPosB = yModB * pressB

        for pressA in range(maxA):
            xPos = xPosB + (xModA * pressA)
            yPos = yPosB + (yModA * pressA)

            if(xPos >= machine['Prize']['X']) or (yPos >= machine['Prize']['Y']):
                break

        if xPos == machine['Prize']['X'] and yPos == machine['Prize']['Y']:
            print('WINNER!!!')
            print('pressB '+str(pressB))
            print('pressA '+str(pressA))
            totalCost = totalCost + (pressB * costB) + (pressA * costA)
            break

print(totalCost)