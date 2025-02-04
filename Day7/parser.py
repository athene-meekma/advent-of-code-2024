fn = 'input.txt'
equations = []
with open(fn, 'r') as f:
    for line in f:
        vals = line.strip().split(' ')
        vals[0] = vals[0].replace(':', '')
        equations.append(list(map(int, vals)))

def multiply(a, b):
    return a * b

def add(a, b):
    return a + b

def doCalc(arr, val, nums):
    if len(nums) > 0:
        sum = add(val, nums[0])
        product = multiply(val, nums[0])
        del nums[0]

        doCalc(arr, sum, nums.copy())
        doCalc(arr, product, nums.copy())
    else:
        arr.append(val)
    return arr

sum = 0
for equation in equations:
    # number we're looking for
    result = equation[0]
    del equation[0]

    # first number in equation
    startVal = equation[0]
    del equation[0]
    eqValues = doCalc([], startVal, equation)

    if result in eqValues:
        sum += result

print(sum)