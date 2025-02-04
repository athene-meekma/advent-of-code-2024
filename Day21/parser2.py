import functools
import numpy as np

test = 0
if test:
    fn = 'test.txt'
    numRobots = 25
else:
    fn = 'input.txt'
    numRobots = 25

directions = {
    '<': ( 0, -1),
    '^': (-1,  0),
    '>': ( 0,  1),
    'v': ( 1,  0)
}

numKeypad = np.array([
    [ 7 , 8,  9 ],
    [ 4 , 5,  6 ],
    [ 1 , 2,  3 ],
    [' ', 0, 'A']
])
numAPos = [3, 2]
numGapPos = [3, 0]

dirKeypad = np.array([
    [' ', '^', 'A'],
    ['<', 'v', '>']
])
dirAPos = [0, 2]
dirGapPos = [0, 0]

codes = []
with open(fn, 'r') as f:
    for line in f:
        line = line.strip()
        codes.append(line)

@functools.cache
def isValid(seq, gapY, gapX, y, x):
    newY = y
    newX = x
    for s in seq:
        dirMod = directions[s]
        newY = newY + dirMod[0]
        newX = newX + dirMod[1]
        if [newY, newX] == [gapY, gapX]:
            return False
    return True

@functools.cache
def generateSequence(code, pad, level):
    if pad == 'num':
        keypad = numKeypad
        curPos = numAPos
        gapPos = numGapPos
    else:
        keypad = dirKeypad
        curPos = dirAPos
        gapPos = dirGapPos

    seq = ''

    for c in code:
        y = curPos[0]
        x = curPos[1]

        target = np.asarray(np.where(keypad == c)).T.tolist()[0]
        targetY = target[0]
        targetX = target[1]

        seq1 = None
        seq2 = None
        seqX = ''
        seqY = ''
        moveX = targetX - x
        moveY = targetY - y

        if moveX < 0:
            seqX = '<' * abs(moveX)
        elif moveX > 0:
            seqX = '>' * abs(moveX)

        if moveY < 0:
            seqY = '^' * abs(moveY)
        elif moveY > 0:
            seqY = 'v' * abs(moveY)

        if seqX != '' and seqY == '':
            seq1 = seqX + 'A'
        elif seqX == '' and seqY != '':
            seq1 = seqY + 'A'
        else:
            # We need to worry about gap position
            seq1 = seqX + seqY

            if not isValid(seq1, gapPos[0], gapPos[1], y, x):
                seq1 = None
            if seq1 != None:
                seq1 = seq1 + 'A'

            seq2 = seqY + seqX
            if not isValid(seq2, gapPos[0], gapPos[1], y, x):
                seq2 = None
            if seq2 != None:
                seq2 = seq2 + 'A'

        if seq1 == None:
            seq = seq + seq2
        elif seq2 == None:
            seq = seq + seq1
        else:
            # Check the length of each string
            nextSeq1 = seq1
            if level > 0:
                nextSeq1 = generateSequence(nextSeq1, 'dir', 0)
                nextSeq1 = generateSequence(nextSeq1, 'dir', 0)

            nextSeq2 = seq2
            if level > 0:
                nextSeq2 = generateSequence(nextSeq2, 'dir', 0)
                nextSeq2 = generateSequence(nextSeq2, 'dir', 0)

            if len(nextSeq1) < len(nextSeq2):
                seq = seq + seq1
            else:
                seq = seq + seq2

        curPos = target

    return seq

def backGen(seq, keypad):
    prevSeq = ''
    curPos = np.asarray(np.where(keypad == 'A')).T.tolist()[0]

    y = curPos[0]
    x = curPos[1]

    for s in seq:
        if s == 'A':
            prevSeq = prevSeq + keypad[y][x]
        else:
            dirMod = directions[s]
            y = y + dirMod[0]
            x = x + dirMod[1]
    return prevSeq

sum = 0
for code in codes:
    #if code != '029A':
    #    continue
    print(code)
    nextSeq = generateSequence(code, 'num', 2)  # Numeric keypad
    sequences = {}
    for press in nextSeq.split('A')[:-1]:
        press = press + 'A'
        if not press in sequences:
            sequences[press] = 1
        else:
            sequences[press] = sequences[press] + 1
    #print(seq)

    for l in range(numRobots):
        newSequences = {}
        if l % 5 == 0:
            print(l)

        for sequence, count in sequences.items():
            nextSeq = generateSequence(sequence, 'dir', 2) # Directional keypad
            for press in nextSeq.split('A')[:-1]:
                press = press + 'A'
                if not press in newSequences:
                    newSequences[press] = count
                else:
                    newSequences[press] = newSequences[press] + count

        sequences = newSequences

    size = 0
    for seq, count in sequences.items():
        size = size + (len(seq) * count)

    print(code[0:-1] + ' * '+str(size))
    sum = sum + int(code[0:-1]) * size

print(sum)