import time
import functools

fn = 'input.txt'

stones = {}
with open(fn, 'r') as f:
    for line in f:
        for s in line.strip().split(' '):
            stones[int(s)] = 1

#@functools.cache
#@functools.lru_cache(maxsize=None)  # maxsize=None for unlimited cache
def processStones(stones):
    newStones = {}
    for stone, count in stones.items():
        stone2 = None
        if stone == 0:
            stone1 = 1
        elif len(str(stone)) % 2 == 0:
            middle = int(len(str(stone)) / 2)
            stone1 = int(str(stone)[:middle])
            stone2 = int(str(stone)[middle:])

            if not stone2 in newStones:
                newStones[stone2] = count
            else:
                newStones[stone2] = newStones[stone2] + count
        else:
            stone1 = stone * 2024

        if not stone1 in newStones:
            newStones[stone1] = count
        else:
            newStones[stone1] = newStones[stone1] + count

    return newStones

blinks = 75

print(stones)
start = time.time()

for i in range(blinks):
    stones = processStones(stones)

end = time.time()

print(end - start)

print(sum(stones.values()))