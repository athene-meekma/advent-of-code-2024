import pprint
import numpy as np

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

mod = 10000000000000
#mod = 0
totalCost = 0
for i, machine in enumerate(machines):
    #print('Machine# '+str(i))

    prizeX = machine['Prize']['X'] + mod
    prizeY = machine['Prize']['Y'] + mod

    A = np.array([
        [machine['A']['X'], machine['B']['X']],
        [machine['A']['Y'], machine['B']['Y']]
    ])

    P = np.array([prizeX, prizeY])

    solutions = np.linalg.solve(A, P )

    partsA = str(solutions[0]).split('.')
    pressA = int(partsA[0])
    if int(partsA[1][:1]) == 9:
        # Round up
        pressA = pressA + 1

    partsB = str(solutions[1]).split('.')
    pressB = int(partsB[0])
    if int(partsB[1][:1]) == 9:
        # Round up
        pressB = pressB + 1

    if (
           (machine['A']['X'] * int(pressA)) + (machine['B']['X'] * int(pressB)) == prizeX
       and (machine['A']['Y'] * int(pressA)) + (machine['B']['Y'] * int(pressB)) == prizeY
    ):
        #print('WINNER!!!')
        totalCost = totalCost + (pressB * costB) + (pressA * costA)

print(int(totalCost))