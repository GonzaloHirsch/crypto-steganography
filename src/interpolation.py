
"""
Calculates a power using the galois field multiplication
Receives:
    - num --> Number to be used as power
    - n --> Power to be used
    - field --> Galois field instance
Returns:
    - res --> Power calculated
"""
def field_pow(num, n, field):
    # return num**n
    if n == 0:
        return 1
    res = num
    for _ in range(1, n):
        res = field.Multiply(res, num)
    return res

"""
Calculates a step of the interpolation
Receives:
    - x --> Pixel X from block j for each image
    - y_prime --> Y' calculated, or Y if the first step
    - r --> Step of the interpolation
    - k --> Amount of secrets
    - field --> Galois field instance
Returns:
    - res --> Secret for that step
"""
def calculate_step(x, y_prime, r, k, field):
    # Multiplier
    mult = field_pow(field.Subtract(0,1), k - (r + 1), field)
    # Result
    res = 0
    # Iteration for summation
    for i in range(k - r):
        temp = 1
        # Iteration for multiplication
        for q in range(k - r):
            # Perform multiplication operation
            if q != i:
                temp = field.Multiply(temp, field.Divide(x[q], field.Subtract(x[i], x[q])))
        # Perform summation
        res = field.Add(res, field.Multiply(y_prime[i], temp))
    # Perform final multiplication
    res = field.Multiply(mult, res)
    return res


"""
Calculates the Y' array of values.
Receives:
    - x --> Pixel X from block j for each image
    - y --> Representation of Tij
    - s_1 --> First calculated secret
    - field --> Galois field instance
"""
def calculate_y_prime(x, y, s, k, field):
    # Perform calculations inline
    y_prime = [field.Divide(field.Subtract(y[i], s), x[i]) for i in range(k)]
    return y_prime


"""
Performs the Lagrange interpolation to obtain the secrets
Receives:
    - x --> Pixel X from block j for each image
    - y --> Representation of Tij
    - field --> Galois field instance
Returns:
    - s --> Array of secrets
"""
def interpolate(x, y, field):
    # Calculate number of secrets
    k = len(x)
    # Generate array at the beginning
    s = [None] * k
    # Calculate initial value
    s[0] = calculate_step(x, y, 0, k, field)
    # Iterate for next steps
    for r in range(1, k):
        # Calculate Y'
        y = calculate_y_prime(x, y, s[r - 1], k, field)
        s[r] = calculate_step(x, y, r, k, field)
    return s

