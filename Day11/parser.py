import time

fn = 'input.txt'

with open(fn, 'r') as f:
    for line in f:
        stones = list(map(int, line.strip().split(' ')))

test = True

if test:
    print('blink #0')
    print(stones)
    print('count: '+str(len(stones)))
    print()

def rule1(stones, i):
    # If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
    applied = False

    if stones[i] == 0:
        stones[i] = 1
        applied = True

    return applied, stones

def rule2(stones, i):
    # If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
    applied = False

    stringVal = str(stones[i])
    length = len(stringVal)
    if length % 2 == 0:
        middle = int(length / 2)
        stone1 = int(stringVal[middle:])
        stone2 = int(stringVal[:middle])

        stones[i] = stone1
        stones = stones[:i] + [stone2] + stones[i:]

        applied = True

    return applied, stones

def rule3(stones, i):
    # If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.
    stones[i] = stones[i] * 2024
    return stones

start = time.time()
blinks = range(10)
shift = 0
stoneRange = range(len(stones))
for blink in blinks:
    if test:
        print('blink #'+str(blink + 1))

    for i in stoneRange:
        i = i + shift
        if i >= len(stones):
            break
        applied, stones = rule1(stones, i)

        if not applied:
            applied, stones = rule2(stones, i)
            if applied:
                shift = shift + 1

        if not applied:
            stones = rule3(stones, i)

        applied = False
        stoneRange = range(len(stones))

    print(stones)
    print('count: '+str(len(stones)))
    print()
    shift = 0

end = time.time()
print(end - start) # 111.03746509552002
print(len(stones)) # 229043