import sys
from PIL import Image

action = sys.argv[1]
filepath = sys.argv[2]
number = sys.argv[3]
directory = sys.argv[4]

img = Image.open(filepath) 

imageSizeW, imageSizeH = img.size

nonWhitePixels = []

for i in range(1, imageSizeW):
    for j in range(1, imageSizeH):
        pixVal = img.getpixel((i, j))
        if pixVal != (255, 255, 255):
            nonWhitePixels.append([i, j])

print(nonWhitePixels)

#with open(filepath, 'rb') as f:
    #data = bytearray(f.read())
    #header = data[0:14]
    #image = data[54:]
    #print(image)
    # print(data)

    #with open(directory + 'eggs.bmp', 'wb') as d:
    #    d.write(data)

