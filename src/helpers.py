# https://www.geeksforgeeks.org/program-to-find-parity/
# Function to get parity of number n.
# It returns 1 if n has odd parity,
# and returns 0 if n has even parity
def getParity( n ):
    parity = 0
    while n:
        parity = ~parity
        n = n & (n - 1)

    return 0 if parity == 0 else 1

# https://stackoverflow.com/questions/12173774/how-to-modify-bits-in-an-integer
# Will set to 1 the bit of value in the position indicated
def setBit(value, bitPos):
    return value | (1<<bitPos)
# Will set to 0 the bit of value in the position indicated
def clearBit(value, bitPos):
    return value & ~(1<<bitPos)

#https://stackoverflow.com/questions/16926130/convert-to-binary-and-keep-leading-zeros-in-python
def getBitsRepresentation(byte):
    return format(byte, '08b')