# Lib imports
import random

import constants
from helpers import getParity, setBit, clearBit, getBitsRepresentation

class ShamirAlgorithm:
    
    def __init__(self, secret, k, n, shadows):
        self.secret = secret
        self.k = k
        self.n = n
        self.shadows = shadows
        self.polinomialMod = 255
        self.coeficients = []
        self.polinomialPairs = []

    def encode(self):
        self.createOrderKPolinomial()
        print(self.__str__())
        pairs = self.createPolinomialPairs()
        print(pairs)
        
    # F(x) = S + a_1*x + ... + a_k-1*(x)^(k-1)
    def createOrderKPolinomial(self):
        self.coeficients = [random.randint(1, self.polinomialMod-1) for _ in range(1, self.k)]

    def evaluatePolinomial(self, value):
        # a0 = secrete
        result = self.secret
        for i in range (1, self.k):
            result += self.coeficients[i-1] * (value**i)

        return result % self.polinomialMod

    # TODO - No se si es solo con el primer bloque de cada sombra
    def createPolinomialPairs(self):
        pairs = []
        for i in range (0, self.n):
            # Get the i-th shadow, its first block, and the X pixel
            shadowX = self.shadows[i][0][0]
            pairs.append((shadowX, self.evaluatePolinomial(shadowX)))
        return pairs

    def __encodePixelBlock(self, secretByte, block): 
        W = block[1]
        V = block[2]
        U = block[3]

        bits = getBitsRepresentation(secretByte)
        parity = str(getParity(secretByte))

        # print("BEFORE")
        # print(W, " = ", getBitsRepresentation(W))
        # print(V, " = ", getBitsRepresentation(V))
        # print(U, " = ", getBitsRepresentation(U))
        # print("AFTER. ", bits,  parity)

        # Replacing bits for W
        W = self.__setBit(W, bits[0], 2)
        W = self.__setBit(W, bits[1], 1)
        W = self.__setBit(W, bits[2], 0)
        # Replacing bits for V
        V = self.__setBit(V, bits[3], 2)
        V = self.__setBit(V, bits[4], 1)
        V = self.__setBit(V, bits[5], 0)
        # Replacing bits for U
        U = self.__setBit(U, parity, 2)
        U = self.__setBit(U, bits[6], 1)
        U = self.__setBit(U, bits[7], 0)
        
        # print("W = ", getBitsRepresentation(W))
        # print("V = ", getBitsRepresentation(V))
        # print("U = ", getBitsRepresentation(U))

    
    def __setBit(self, byte, value, position):
        return clearBit(byte, position) if value == '0' else setBit(byte, position)

    def __str__(self):
        subs = '[schema=(%i,%i)] [secret=%i] [coeficients=%s] [mod=%i]' % (self.k, self.n, self.secret, self.coeficients, self.polinomialMod)
        s = '%s{%s}' % (type(self).__name__, subs)
        return s