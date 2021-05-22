# Lib imports
import sys
from transformer import Transformer
# Local imports
from config import Config
from bmpStructure import BMPStructure
from transformer import Transformer
from shamirAlgorithm import ShamirAlgorithm

# Parses CLI options
def parse_cli():
    action = sys.argv[1]
    secret_image = sys.argv[2]
    k = sys.argv[3]
    directory = sys.argv[4]
    return Config(action, secret_image, k, directory)

def main():
    # Parse program arguments and get config object
    config = parse_cli()

    # Parsing the BMP image
    bmpStructure = BMPStructure(config.secret_image)
    print(bmpStructure)

    # array = [
    #     15, 14, 13, 12,
    #     11, 10,  9,  8,
    #      7,  6,  5,  4,
    #      3,  2,  1,  0
    # ]

    blockArray = Transformer.mapPixelArrayIntoBlocks(
        bmpStructure.getPixelArray(), 
        bmpStructure.getHeight(), 
        bmpStructure.getWidth()
    )

    shamir = ShamirAlgorithm(blockArray)

    pixels = Transformer.mapBlocksIntoPixelArray(
        blockArray,
        bmpStructure.getHeight(), 
        bmpStructure.getWidth()
    )

    bmpStructure.writeNewImage(pixels, config.directory, 'eggs.bmp')

# Program entrypoint
if __name__ == "__main__":
   main()
