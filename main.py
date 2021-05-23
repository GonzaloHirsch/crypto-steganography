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

    blockArray = Transformer.mapPixelArrayIntoBlocks(
        bmpStructure.getPixelArray(), 
        bmpStructure.getHeight(), 
        bmpStructure.getWidth()
    )

    shamir = ShamirAlgorithm("AcD227", 3, 5, [[[0, 1, 4, 5], [2, 3, 6, 7]],[[8,9,12,13],[10,11,14,15]], [[0, 1, 4, 5], [2, 3, 6, 7]], [[0, 1, 4, 5], [2, 3, 6, 7]], [[0, 1, 4, 5], [2, 3, 6, 7]]])
    shamir.encode()

    pixels = Transformer.mapBlocksIntoPixelArray(
        blockArray,
        bmpStructure.getHeight(), 
        bmpStructure.getWidth()
    )

    # print(blockArray)
    # print(pixels)

    bmpStructure.writeNewImage(pixels, config.directory, 'eggs.bmp')

# Program entrypoint
if __name__ == "__main__":
   main()
