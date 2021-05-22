# Lib imports

import constants
from helpers import getParity, setBit, clearBit, getBitsRepresentation

class ShamirAlgorithm:
    
    def __init__(self, pixelBlocks):
        self.pixelBlocks = pixelBlocks
        # self.__encodePixelBlock(37, self.pixelBlocks[6])
        

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

       