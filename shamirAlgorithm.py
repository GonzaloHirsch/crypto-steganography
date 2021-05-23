import constants
from helpers import getParity, setBit, clearBit, getBitsRepresentation
from interpolation import field_pow, interpolate

class ShamirAlgorithm:
    
    def __init__(self, action, field, shadows, k, n=None, secret=None, debug=False):

        self.action = action
        self.field = field
        self.shadows = shadows
        self.k = int(k)
        self.coeficients = []
        self.polinomialCount = 0
        self.debug = debug

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

    def decode(self):
        self.__verifyAndExtract()
    
    def __encodeShadows(self):
        print(len(self.shadows), len(self.shadows[1]))
        for shadowIdx in range (0, self.n):
            if (self.debug) :
                print('\n####### Shadow %i #######' % (shadowIdx))

            for blockIdx in range(0, self.polinomialCount):
                # Get the imageIdx-th shadow, its "blockIdx" block, and the X pixel
                shadowBlock = self.shadows[shadowIdx][blockIdx]
                shadowX = shadowBlock[0]
                # Evaluate the block with its corresponding polinomial
                evaluationX = self.__evaluatePolinomial(blockIdx, shadowX)
                if (self.debug) :
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
            if (self.debug) :
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
        
        if (self.debug) :
            print('[W=(%i) bin=(%s) newW=(%i) encoded=(%s)]\n[V=(%i) bin=(%s) newV=(%i) encoded=(%s)]\n[U=(%i) bin=(%s) newU=(%i) encoded=(%s)]\n' % (block[1], getBitsRepresentation(block[1]), W, getBitsRepresentation(W), block[2], getBitsRepresentation(block[2]), V, getBitsRepresentation(V), block[3], getBitsRepresentation(block[3]), U, getBitsRepresentation(U)))

        block[1] = W
        block[2] = V
        block[3] = U

        return block

    def __verifyAndExtract(self):
        # This array will hold the J block for all shadows
        # [[1_block_img_1, 1_block_img_2, ...], [2_block_img_1, 2_block_img_2, ...]]
        j_blocks = []

        # Extract the J block for each shadow
        # J is the number of blocks per shadow
        for j in range(len(self.shadows[0])):
            j_blocks.append([shadow[j] for shadow in self.shadows])

        # Verify all blocks and prepare X and Y
        verified_j_blocks = []
        for j_block in j_blocks:
            xs, ys = [], []
            # Verify each block
            for block in j_block:
                # If verified add the X and Y to the arrays
                valid, x, y = self.__verifyBlock(block)
                if valid:
                    xs.append(x)
                    ys.append(y)
            if len(xs) > 0:
                verified_j_blocks.append([xs, ys])

        # Obtain all secrets and join them
        secrets = [interpolate(v_block[0], v_block[1], self.field) for v_block in verified_j_blocks]
        joined_secrets = [s for secret in secrets for s in secret]
        self.secret = joined_secrets

    def __verifyBlock(self, block):
        # Getting bit representation for each one
        x, w, v, u = [getBitsRepresentation(b) for b in block]
        t = 0
        # Setting T bits
        t = self.__setBit(t, w[0], 2)
        t = self.__setBit(t, w[1], 1)
        t = self.__setBit(t, w[2], 0)
        t = self.__setBit(t, v[0], 5)
        t = self.__setBit(t, v[1], 4)
        t = self.__setBit(t, v[2], 3)
        t = self.__setBit(t, u[0], 7)
        t = self.__setBit(t, u[1], 6)

        # Making the verification
        if int(u[2]) == self.__completeNumberXor(t):
            return True, block[0], t
        return False, None, None

    def __completeNumberXor(self, number):
        # Get representation in bits
        bits = getBitsRepresentation(number)
        val = int(bits[0])
        # XOR the other bits in chain
        for i in range(1, len(bits)):
            val = val ^ int(bits[i])
        return val

    def __setBit(self, byte, value, position):
        return clearBit(byte, position) if value == '0' else setBit(byte, position)

    def __str__(self):
        subs = '[schema=(%i,%i)] [secret=%s] [generator=%i]' % (self.k, self.n, self.secret, self.field.generator)
        s = '%s{%s}' % (type(self).__name__, subs)
        return s