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
    k = int(sys.argv[3])
    directory = sys.argv[4]
    # Validations
    if not os.path.isdir(directory):  
        print("[Error] El path al directorio \'{}\' no es válido".format(directory)) 
        exit(1)
    if action == ENCODE and (not os.path.isfile(secret_image) or not secret_image.endswith('.bmp')): 
        print("[Error] El path a la imagen secreta \'{}\' no es un válido".format(secret_image))
        exit(1)
    files_in_directory = len([name for name in os.listdir(directory) if os.path.isfile(directory + "/" + name) and name.endswith('.bmp')])
    if validate:
        if action != ENCODE and action != DECODE:
            print('[Error] Opción inválida \'{}\' para la acción, debe ser \'{}\' o \'{}\''.format(action, ENCODE, DECODE))
            exit(1)
        if k < 4 or k > 6:
            print('[Error] Opción inválida \'{}\' para K, debe ser 4 <= k <= 6'.format(k))
            exit(1)
        if files_in_directory < k:
            print('[Error] Opción inválida \'{}\' para directorio, deben haber al menos {} archivos .bmp'.format(directory, k))
            exit(1)
    return Config(action, secret_image, k, files_in_directory, directory)

# Extracts all images from a given directory
def get_images_from_directory(config):
    portadoras = []
    w, h = 0, 0

    for name in os.listdir(config.directory):
        filepath = os.path.join(config.directory, name)
        if os.path.isfile(filepath) and filepath.endswith('.bmp'):
            portadoraStructure = BMPStructure(filepath)
            # Store w and h, and check if all share dimensions
            if w == 0 or h == 0:
                w, h = portadoraStructure.getWidth(), portadoraStructure.getHeight()
            elif w != portadoraStructure.getWidth() or h != portadoraStructure.getHeight():
                print("[Error] Las imágenes del directorio no tienen todas el mismo tamaño")
                exit(1)
            portadoras.append(Transformer.mapPixelArrayIntoBlocks(
                portadoraStructure.getPixelArray(), 
                portadoraStructure.getHeight(), 
                portadoraStructure.getWidth()
            ))

    return portadoras, w, h

def encode(config, galoisField):
    # Parsing the BMP image
    bmpStructure = BMPStructure(config.secret_image)

    # Extracting images from directory
    portadoras, w, h = get_images_from_directory(config)

    # Checking that sizes are correct
    if w != bmpStructure.getWidth() or h != bmpStructure.getHeight():
        print("[Error] La imagen secreta no es del mismo tamaño que las portadoras. Las portadoras son de {}x{} y la imagen secreta es de {}x{}".format(w,h,bmpStructure.getWidth(),bmpStructure.getHeight()))
        exit(1)

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
    portadoras, w, h = get_images_from_directory(config)

    # Decode using the Shamir Algorithm
    shamir = ShamirAlgorithm(DECODE, galoisField, portadoras, config.k, width=w, height=h)
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
    config = parse_cli(True)

    F = ffield.FField(8, gen=355, useLUT=1)

    if config.action == 'd':
        encode(config, F)
    else:
        decode(config, F)

# Program entrypoint
if __name__ == "__main__":
   main()
