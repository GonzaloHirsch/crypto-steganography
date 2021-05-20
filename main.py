import sys
from struct import unpack

action = sys.argv[1]
filepath = sys.argv[2]
number = sys.argv[3]
directory = sys.argv[4]

#with open(filepath, 'rb') as f:
    #data = bytearray(f.read())
    #header = data[0:14]
    #image = data[54:]
    #print(image)
    # print(data)

    #with open(directory + 'eggs.bmp', 'wb') as d:
    #    d.write(data)
# https://www.programmersought.com/article/89437442663/
def getImg(bitmap):
    bitmap.seek(28)
    bit_num=unpack("<i",bitmap.read(4))[0]#Bytes
    bitmap.seek(10)
    #From the beginning to the number of bytes required for the image data
    to_img_data=unpack("<i",bitmap.read(4))[0]
    bitmap.seek(bitmap.tell()+4)
    #unpack convert to decimal
    img_width=unpack("<i",bitmap.read(4))[0]
    img_height = unpack("<i", bitmap.read(4))[0]
    bitmap.seek(to_img_data)
    print(img_width)
    print(img_height)
    x=0
    y=0
    num=0
    bits = []
    while y<img_height:
        while(x<img_width):
            if (bit_num <= 8):#Image reading less than or equal to 8 bits
                img_byte= unpack("B", bitmap.read(1))[0]
                bits.append(img_byte)
                x+=1
        x=0
        y+=1
        while (num % 4 != 0):  # The number of digits in each row must be a multiple of 4
            num += 1
            bits.append(bitmap.read(1))
        num=0
    return bits

bmp = open(filepath, 'rb')
bitArray = getImg(bmp)
# print(bitArray)