import functools
import numpy as np

test = 1
if test:
    fn = 'test.txt'
else:
    fn = 'input.txt'

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

dirKeypad = np.array([
    [' ', '^', 'A'],
    ['<', 'v', '>']
])

codes = []
with open(fn, 'r') as f:
    for line in f:
        line = line.strip()
        codes.append(line)

def generateSequence(code, pad, level):
    if pad == 'num':
        keypad = numKeypad
    else:
        keypad = dirKeypad

    curPos = np.asarray(np.where(keypad == 'A')).T.tolist()[0]

    gapPos = np.asarray(np.where(keypad == ' ')).T.tolist()[0]

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
            newY = y
            newX = x
            for s in seq1:
                dirMod = directions[s]
                newY = newY + dirMod[0]
                newX = newX + dirMod[1]
                if [newY, newX] == gapPos:
                    seq1 = None
                    break
            if seq1 != None:
                seq1 = seq1 + 'A'

            seq2 = seqY + seqX
            newY = y
            newX = x
            for s in seq2:
                dirMod = directions[s]
                newY = newY + dirMod[0]
                newX = newX + dirMod[1]
                if [newY, newX] == gapPos:
                    seq2 = None
                    break
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
                if level > 1:
                    nextSeq1 = generateSequence(nextSeq1, 'dir', 0)

            nextSeq2 = seq2
            if level > 0:
                nextSeq2 = generateSequence(nextSeq2, 'dir', 0)
                if level > 1:
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
    if code != '029A':
        continue
    print(code)
    seq = generateSequence(code, 'num', 2)  # Numeric keypad
    print(seq)
    seq = generateSequence(seq, 'dir', 1) # Robot 1
    print(seq)
    seq = generateSequence(seq, 'dir', 0) # Robot 2
    print(seq)
    print()

    print(code[0:-1] + ' * '+str(len(seq)))
    sum = sum + int(code[0:-1]) * len(seq)

print(sum)