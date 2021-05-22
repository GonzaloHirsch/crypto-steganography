from struct import unpack, pack
    

def writeNewImage(filepath, newpicture, directory, fileName):
    bitmap = open(filepath, 'rb')
    raw = bytearray(bitmap.read())
    newBytes = []
    for byte in newpicture:
        newByte = pack("B", byte)
        newBytes.append(newByte)
    bitmap.seek(28)
    bitmap.seek(10)
    #From the beginning to the number of bytes required for the image data
    to_img_data=unpack("<i",bitmap.read(4))[0]
    bitmap.seek(bitmap.tell()+4)
    with open(directory + fileName, 'wb') as d:
        d.write(raw)
        d.seek(to_img_data)
        for byte in newBytes:
            d.write(byte)
    bitmap.close()