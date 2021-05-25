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
    files_in_directory = len([name for name in os.listdir(directory) if os.path.isfile(directory + "/" + name)])
    if validate:
        if action != ENCODE and action != DECODE:
            print('Opción inválida \'{}\' para la acción, debe ser \'{}\' o \'{}\''.format(action, ENCODE, DECODE))
            exit(1)
        if k < 4 or k > 6:
            print('Opción inválida \'{}\' para K, debe ser 4 <= k <= 6'.format(k))
            exit(1)
        if files_in_directory < k:
            print('Opción inválida \'{}\' para directorio, deben haber al menos {} archivos'.format(directory, k))
            exit(1)
    return Config(action, secret_image, k, files_in_directory, directory)

# Extracts all images from a given directory
def get_images_from_directory(config):
    portadoras = []

    for name in os.listdir(config.directory):
        filepath = os.path.join(config.directory, name)
        if os.path.isfile(filepath):
            portadoraStructure = BMPStructure(filepath)
            portadoras.append(Transformer.mapPixelArrayIntoBlocks(
                portadoraStructure.getPixelArray(), 
                portadoraStructure.getHeight(), 
                portadoraStructure.getWidth()
            ))

    return portadoras

def encode(config, galoisField):
    # Parsing the BMP image
    bmpStructure = BMPStructure(config.secret_image)

    portadoras = get_images_from_directory(config)

    shamir = ShamirAlgorithm(ENCODE, galoisField, portadoras, config.k, config.n, bmpStructure.getPixelArray())
    shamir.encode()

    for idx, name in enumerate(os.listdir(config.directory)):
        filepath = os.path.join(config.directory, name)
        if os.path.isfile(filepath) :
            shadows = shamir.shadows
            shadow = Transformer.mapBlocksIntoPixelArray(
                shadows[idx],
                bmpStructure.getHeight(), 
                bmpStructure.getWidth()
            )
            bmpStructure.writeNewImage(shadow, os.path.join(config.directory, name))

def decode(config, galoisField):
    # Extract shadowed images
    portadoras = get_images_from_directory(config)

    # Decode using the Shamir Algorithm
    shamir = ShamirAlgorithm(DECODE, galoisField, portadoras, config.k)
    shamir.decode()

    # Find an image to use
    resultStructure = None
    for name in os.listdir(config.directory):
        filepath = os.path.join(config.directory, name)
        if os.path.isfile(filepath):
            resultStructure = BMPStructure(filepath)
            break
    if resultStructure == None:
        print("No hay imagenes para reusar encabezados en el directorio \'{}\'".format(config.directory))
        exit(1)
    
    # Write result into the secret image
    resultStructure.writeNewImage(shamir.secret, config.secret_image)


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
