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
for secret in secrets:
    for _ in range(2000):
       secret = nextSecret(secret)
    #print(secret)
    sum = sum + secret
print(sum)