import constants
from helpers import getParity, setBit, clearBit, getBitsRepresentation
from interpolation import field_pow

class ShamirAlgorithm:
    
    def __init__(self, action, field, shadows, k, n=None, secret=None):

        self.action = action
        self.field = field
        self.shadows = shadows
        self.k = int(k)
        self.coeficients = []
        self.polinomialCount = 0

        if (action == constants.ENCODE):
            # Divide the secret into blocks of k bytes
            self.secret = self.__splitSecret(secret)
            self.n = n
            # How many polinomials there are
            # Equivalent to how many blocks we will use of each shadow
            self.polinomialCount = len(self.secret)
            print(self.polinomialCount)

            # Extra validation
            if (self.k > self.n or len(shadows) != n):
                print("Incorrect parameters. The following must be satisfied:\n  - n = k\n  - len(shadow) = n")
                exit(1)
            # In case the secret is longer than the amount of blocks in the shadows
            if (len(self.shadows[0]) < self.polinomialCount):
                print("Secret is too long. Shadows contain {} blocks but secret has {} blocks.".format(len(self.shadows[0]), self.polinomialCount))
                exit(1)

    def encode(self):
        self.__createPolinomials()
        self.__encodeShadows()
    
    def __encodeShadows(self):
        print(len(self.shadows), len(self.shadows[1]))
        for shadowIdx in range (0, self.n):
            print('\n####### Shadow %i #######' % (shadowIdx))

            for blockIdx in range(0, self.polinomialCount):
                # Get the imageIdx-th shadow, its "blockIdx" block, and the X pixel
                shadowBlock = self.shadows[shadowIdx][blockIdx]
                shadowX = shadowBlock[0]
                # Evaluate the block with its corresponding polinomial
                evaluationX = self.__evaluatePolinomial(blockIdx, shadowX)

                print('[blockIdx=(%i)] [block=(%s)] [polinomial=(%s)] [eval=(%i) bin=(%s)]' % (blockIdx, shadowBlock, self.coeficients[blockIdx], evaluationX, getBitsRepresentation(evaluationX)))

                # Return the new shadow block with the changes bits
                shadowBlock = self.__encodePixelBlock(evaluationX, shadowBlock)
                # Update the images array corresponding block
                self.shadows[shadowIdx][blockIdx] = shadowBlock
               

    # Secret is an array of bytes
    def __splitSecret(self, secret):
        # Divide the secret into blocks of k bytes (each char = 1 byte)
        secretBlocks = [secret[i:i+self.k] for i in range(0, len(secret), self.k)]

        if (len(secretBlocks[-1]) != self.k):
            print("[Warning] Secret is not divisible by k = ", self.k)

        return secretBlocks

    # F(x) = a_0 + a_1*x + ... + a_k-1*(x)^(k-1)
    def __createPolinomials(self):
        # Array of arrays of polinomial coeficient. 
        # 1 array of coeficient per secret block
        coeficients = []

        # For each block, create the polinomial coeficients 
        for secretBlock in self.secret:
            coeficients.append([secretBlock[i] for i in range(0, self.k)])

        self.coeficients = coeficients


    # Evaluate the polinomial F_i(X_i)
    # Hacer dentro de Galois
    def __evaluatePolinomial(self, index, value):
        result = 0
        for i in range (0, self.k):
            power = field_pow(value, i, self.field)
            mult = self.field.Multiply(self.coeficients[index][i], power)
            result =  self.field.Add(result, mult)

        return result

    def __encodePixelBlock(self, secretByte, block): 
        W = block[1]
        V = block[2]
        U = block[3]

        bits = getBitsRepresentation(secretByte)
        parity = str(getParity(secretByte))

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

        print('[W=(%i) bin=(%s) newW=(%i) encoded=(%s)]\n[V=(%i) bin=(%s) newV=(%i) encoded=(%s)]\n[U=(%i) bin=(%s) newU=(%i) encoded=(%s)]\n' % (block[1], getBitsRepresentation(block[1]), W, getBitsRepresentation(W), block[2], getBitsRepresentation(block[2]), V, getBitsRepresentation(V), block[3], getBitsRepresentation(block[3]), U, getBitsRepresentation(U)))

        block[1] = W
        block[2] = V
        block[3] = U

        return block

    
    def __setBit(self, byte, value, position):
        return clearBit(byte, position) if value == '0' else setBit(byte, position)

    def __str__(self):
        subs = '[schema=(%i,%i)] [secret=%s] [generator=%i]' % (self.k, self.n, self.secret, self.field.generator)
        s = '%s{%s}' % (type(self).__name__, subs)
        return s