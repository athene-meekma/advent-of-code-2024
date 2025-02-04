import math

test = 0
if test:
    fn = 'test.txt'
else:
    fn = 'input.txt'

secrets = []
with open(fn, 'r') as f:
    for line in f:
        line = line.strip()
        secrets.append(int(line))

def mix(secret, val):
    secret = secret ^ val
    return secret

def prune(secret):
    return secret % 16777216

def nextSecret(secret):
    val = secret * 64
    secret = prune(mix(secret, val))

    val = math.floor(secret / 32)
    secret = prune(mix(secret, val))

    val = secret * 2048
    secret = prune(mix(secret, val))

    return secret

sum = 0
bestPrices = {}
for secret in secrets:
    changes = []
    found = []
    prevPrice = None
    for _ in range(2000):
        price = secret % 10
        if prevPrice != None:
            priceDiff = price - prevPrice
            changes.append(priceDiff)
            if len(changes) >= 4:
                k = ''.join(map(str, changes[-4:]))
                if k not in found:
                    if k in bestPrices:
                        bestPrices[k] = bestPrices[k] + price
                    else:
                        bestPrices[k] = price
                    found.append(k)

        secret = nextSecret(secret)
        prevPrice = price

t = max(bestPrices, key=bestPrices.get)
print(t)
print(bestPrices[t])