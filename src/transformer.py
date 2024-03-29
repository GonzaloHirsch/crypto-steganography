# Lib imports

import constants

class Transformer:
    
    def mapPixelArrayIntoBlocks(pixelsArray, imageHeight, imageWidth): 
        blockArray = []

        newPixelsArray = Transformer.__convertPixelArray(pixelsArray, imageHeight, imageWidth)

        # Image must have width and height divisible by 4 
        if (imageHeight % constants.BLOCK_SIDE != 0):
            print('Image height not divisible by block size')
            return
        if (imageWidth % constants.BLOCK_SIDE != 0):
            print('Image width not divisible by block size')
            return

        # Creating each block from top left to bottom right
        for blockHeightIdx in range(0, int(imageHeight/2)):
            for blockWidthIdx in range(0, int(imageWidth/2)):
                blockArray.append(Transformer.__getPixelBlock(newPixelsArray, blockHeightIdx, blockWidthIdx, imageWidth))

        return blockArray

    def __convertPixelArray(pixelsArray, imageHeight, imageWidth):
        newPixelArray = []
        # Will move from the top rows to the bottom ones 
        for i in range(1, imageHeight + 1):
            # Gives me the first index of the row
            index = (imageHeight - i) * imageWidth
            # Will add all the elements of that row
            for j in range(0, imageWidth):
                newPixelArray.append(pixelsArray[index + j])

        return newPixelArray


    def __getPixelBlock(pixelsArray, blockHeightIdx, blockWidthIdx, imageWidth):
        # Calculate current index
        blockWidthOffset = blockWidthIdx * 2
        blockHeightOffset = blockHeightIdx * imageWidth * 2
        index = blockHeightOffset + blockWidthOffset 
                
        block = []
        block.append(pixelsArray[index])                  # X
        block.append(pixelsArray[index + 1])              # W
        block.append(pixelsArray[index + imageWidth])     # V
        block.append(pixelsArray[index + imageWidth + 1]) # U

        return block

    def mapBlocksIntoPixelArray(blockPixelsArray, imageHeight, imageWidth): 
        pixelsArray = []

        blockWidths = int(imageWidth/2)
        blockHeights = int(imageHeight/2)

        for blockHeightIdx in range(0, blockHeights):
            startBlockIdx = blockHeightIdx * blockWidths
            # Get first row of the blocks in current block row
            for blockIdx in range(startBlockIdx, startBlockIdx+blockWidths):
                pixelsArray.append(blockPixelsArray[blockIdx][0])
                pixelsArray.append(blockPixelsArray[blockIdx][1])
            # Get second row of the blocks in current block row
            for blockIdx in range(startBlockIdx, startBlockIdx+blockWidths):
                pixelsArray.append(blockPixelsArray[blockIdx][2])
                pixelsArray.append(blockPixelsArray[blockIdx][3])

        return Transformer.__convertPixelArray(pixelsArray, imageHeight, imageWidth)