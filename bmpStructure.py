# Lib imports
from struct import unpack, pack

import constants

class BMPStructure:

    def __init__(self, filepath):
        self.filepath = filepath
        self.bitmap = open(filepath, 'rb')
        self.imageWidth = 0
        self.imageHeight = 0
        self.offset = 0
        self.bitsPerPixel = 0
        self.pixelsArray = []
        self.blockPixelsArray = []
        
        self.__parseFileHeader()
        self.__parseDIBHeader()
        self.__parsePixelMap()

    def __parseFileHeader(self):
        # The offset, i.e. starting address, of the byte where the bitmap image data (pixel array) can be found.
        self.bitmap.seek(constants.FILE_HEADER_OFFSET + constants.PIXELS_OFFSET_OFFSET)
        self.offset = unpack("<i", self.bitmap.read(constants.INT_BYTES))[0]

    def __parseDIBHeader(self):
        self.bitmap.seek(constants.DIP_HEADER_OFFSET + constants.WIDTH_OFFSET)
        # the bitmap width in pixels (signed integer)
        self.imageWidth = self.__unpackInt()
        # the bitmap height in pixels (signed integer)
        self.imageHeight = self.__unpackInt()

        # the number of bits per pixel, which is the color depth of the image. Typical values are 1, 4, 8, 16, 24 and 32.
        self.bitmap.seek(constants.DIP_HEADER_OFFSET + constants.BITS_PER_PIXEL_OFFSET)
        self.bitsPerPixel = self.__unpackShort()

    def __parsePixelMap(self):
        self.bitmap.seek(self.offset)
        num = 0
        bits = []

        # Will only be working with grey scale
        if (self.bitsPerPixel > 8): 
            return []

        # Reading columns
        for _ in range(0, self.imageHeight):
            # Reading row
            for _ in range(0, self.imageWidth):
                img_byte = unpack("B", self.bitmap.read(constants.BYTE))[0]
                bits.append(img_byte)
                # Amount of bytes being read
                num += 1

            # If the bytes read are not a multiple of 4, continue reading
            # Note here that since Windows scans are in units of 4 bytes, 
            # when reading each row of data, if the number read is not a 
            # multiple of 4, you should continue to read useless information 
            # until it is a multiple of 4.
            while (num % 4 != 0):  
                num += 1
                self.bitmap.read(constants.BYTE)

            num=0

        self.pixelsArray = bits

    def getPixelArray(self):
        return self.pixelsArray
    
    def __unpackInt(self):
        return unpack("<i", self.bitmap.read(constants.INT_BYTES))[0]
    
    def __unpackShort(self):
        return unpack("<h", self.bitmap.read(constants.SHORT_BYTES))[0]

    def writeNewImage(self, directory, filename):
        bitmap = open(self.filepath, 'rb')
        raw = bytearray(bitmap.read())
        newBytes = []
        for byte in self.pixelsArray:
            newByte = pack("B", byte)
            newBytes.append(newByte)

        with open(directory + filename, 'wb') as d:
            d.write(raw)
            d.seek(self.offset)
            for byte in newBytes:
                d.write(byte)
        bitmap.close()

    def mapPixelArrayIntoBlocks(self): 
        blockArray = []

        # Image must have width and height divisible by 4 
        if (self.imageHeight % constants.BLOCK_SIDE != 0):
            print('Image height not divisible by block size')
            return
        if (self.imageWidth % constants.BLOCK_SIDE != 0):
            print('Image width not divisible by block size')
            return

        # Creating each block from top left to bottom right
        print( int(self.imageWidth/2))
        for blockHeightIdx in range(0, int(self.imageHeight/2)):
            for blockWidthIdx in range(0, int(self.imageWidth/2)):
                blockArray.append(self.__getPixelBlock(blockHeightIdx, blockWidthIdx))

        self.blockPixelsArray = blockArray

        return blockArray
    
    def __getPixelBlock(self, blockHeightIdx, blockWidthIdx):
        # Calculate current index
        blockWidthOffset = blockWidthIdx * 2
        blockHeightOffset = blockHeightIdx * self.imageWidth * 2
        index = blockHeightOffset + blockWidthOffset 
                
        block = []
        block.append(self.pixelsArray[index])                       # X
        block.append(self.pixelsArray[index + 1])                   # W
        block.append(self.pixelsArray[index + self.imageWidth])     # V
        block.append(self.pixelsArray[index + self.imageWidth + 1]) # U

        return block

    def __str__(self):
        subs = '[file=%s] [width=%i] [height=%i] [offset=%i] [bitsPerPixel=%i]' % (self.filepath, self.imageWidth, self.imageHeight, self.offset, self.bitsPerPixel)
        s = '%s{%s}' % (type(self).__name__, subs)
        return s


    
# https://www.programmersought.com/article/89437442663/
