# Lib imports
import sys
from transformer import Transformer
import os, os.path
from pyfinite import ffield

# Local imports
from config import Config
from bmpStructure import BMPStructure
from transformer import Transformer
from shamirAlgorithm import ShamirAlgorithm
from constants import DECODE, ENCODE

# Parses CLI options
def parse_cli(validate = False):
    # Parsing
    action = sys.argv[1]
    secret_image = sys.argv[2]
    k = sys.argv[3]
    directory = sys.argv[4]
    # Validations
    if validate:
        if action != ENCODE and action != DECODE:
            print('Opción inválida \'{}\' para la acción, debe ser \'{}\' o \'{}\''.format(action, ENCODE, DECODE))
            exit(1)
        if k < 4 or k > 6:
            print('Opción inválida \'{}\' para K, debe ser 4 <= k <= 6'.format(k))
            exit(1)
        files_in_directory = len([name for name in os.listdir(directory) if os.path.isfile(name)])
        if files_in_directory < k:
            print('Opción inválida \'{}\' para directorio, deben haber al menos {} archivos'.format(directory, k))
            exit(1)
    return Config(action, secret_image, k, directory)

def encode(config, galoisField):
    # Parsing the BMP image
    bmpStructure = BMPStructure(config.secret_image)
    print(bmpStructure)

    blockArray = Transformer.mapPixelArrayIntoBlocks(
        bmpStructure.getPixelArray(), 
        bmpStructure.getHeight(), 
        bmpStructure.getWidth()
    )
    # TODO
    randomShadows = [[[0, 1, 4, 5], [2, 3, 6, 7]],[[8,9,12,13],[10,11,14,15]], [[0, 1, 4, 5], [2, 3, 6, 7]], [[0, 1, 4, 5], [2, 3, 6, 7]], [[0, 1, 4, 5], [2, 3, 6, 7]]]

    shamir = ShamirAlgorithm(ENCODE, galoisField, randomShadows, config.k, len(randomShadows), bmpStructure.getPixelArray())
    shamir.encode()

    pixels = Transformer.mapBlocksIntoPixelArray(
        blockArray,
        bmpStructure.getHeight(), 
        bmpStructure.getWidth()
    )

    # print(blockArray)
    # print(pixels)

    bmpStructure.writeNewImage(pixels, config.directory, 'eggs.bmp')

def decode(config, galoisField):
    return

def main():
    # Parse program arguments and get config object
    config = parse_cli()

    F = ffield.FField(8, gen=355, useLUT=0)

    if config.action == 'd':
        encode(config, F)
    else:
        decode(config, F)

# Program entrypoint
if __name__ == "__main__":
   main()
