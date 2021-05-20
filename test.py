import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
from struct import unpack
def byte_to_int(str1):
    #From a byte of type str to int
    result=0
    for i in range(len(str1)):
        y=int(str1[len(str1)-1-i])
        result+=y*2**i
    return result

def breakup_byte(num1,n):
    #byte is the input parameter of type byte, n is the number of digits required for each number
    result=[]#Returned number
    num=num1[2:]
    num_len=len(num)
    str1 = ""
    for i in range(8-num_len):
        str1+=str(0)
    num=str1+num
    for i in range(int(8/n)):
        temp=num[8-n*(i+1):8-n*i]
        result.append(byte_to_int(temp))
    result.reverse()
    return result

def breakup_16byte(str1,str2):
    #16bits are stored in little endian
    num1=str1[2:]
    num2=str2[2:]
    str1_ = ""
    str2_ = ""
    num_len1=len(num1)
    num_len2=len(num2)
    for i in range(8-num_len1):
        str1_+=str(0)
    num1=str1_+num1
    for i in range(8-num_len2):
        str2_+=str(0)
    num2=str2_+num2
    num = num2 + num1
    #16 bits use two bytes to indicate that rgb is set to 555 and the last one is 0
    result = []
    r=byte_to_int(num[1:6])
    g=byte_to_int(num[6:11])
    b=byte_to_int(num[11:16])
    result.append(r*8)
    result.append(g*8)
    result.append(b*8)
    return result

def bmp_img_read_save_hist(filename):
    xxx=1
    #List the positions of 1, 4, 8, 16, 24
    imgs=os.listdir(filename)
    #The path of the generated image is saved in imgs_path
    imgs_path=[]
    print(imgs)
    for img_name in imgs:
        img_path=filename+os.sep+img_name
        imgs_path.append(img_path)
    #carried out
    for img_path in imgs_path:
        img=open(img_path,"rb")
        #Skip the beginning of the bmp file information, read the size information of the picture directly
        img.seek(28)
        bit_num=unpack("<i",img.read(4))[0]#Bytes
        img.seek(10)
        #From the beginning to the number of bytes required for the image data
        to_img_data=unpack("<i",img.read(4))[0]
        img.seek(img.tell()+4)
        #unpack convert to decimal
        img_width=unpack("<i",img.read(4))[0]
        img_height = unpack("<i", img.read(4))[0]
        img.seek(50)
        #Color index number
        color_num = unpack("<i", img.read(4))[0]
        #1 bit is one bit per pixel, 4 bits is 0.5 byte per pixel, 8 bits is 1 pixel per pixel, 16 bits is 2 bytes per pixel (555+0), 24 bits is 3 bytes per pixel (bgr+alpha)
        #The reading pointer skips 54 bits in total to the color wheel, of which 16, 24 bit images do not need a color wheel
        img.seek(54)
        if(bit_num<=8):
            #How many bytes there are 2^n palette colors
            color_table_num=2**int(bit_num)
            color_table=np.zeros((color_table_num,3),dtype=np.int)
            for i in range(color_table_num):
                b=unpack("B",img.read(1))[0];
                g = unpack("B", img.read(1))[0];
                r = unpack("B", img.read(1))[0];
                alpha=unpack("B", img.read(1))[0];
                color_table[i][0]=b;
                color_table[i][1] = g;
                color_table[i][2] = r;
        #Store data in numpy
        img.seek(to_img_data)
        img_np=np.zeros((img_height,img_width,3),dtype=np.int)
        num=0#Calculate the total number of bytes read
        #Data arrangement from left to right, bottom to top
        x=0
        y=0
        while y<img_height:
            while(x<img_width):
                if (bit_num <= 8):#Image reading less than or equal to 8 bits
                    img_byte= unpack("B", img.read(1))[0]
                    img_byte=bin(img_byte)
                    color_index=breakup_byte(img_byte,bit_num)
                    num+=1
                    for index in color_index:
                        if(x<img_width):
                            img_np[img_height-y-1][x]=color_table[index]
                            x+=1
                elif(bit_num==24):#24-bit image reading
                    num+=3
                    g=unpack("B", img.read(1))[0]
                    b=unpack("B", img.read(1))[0]
                    r=unpack("B", img.read(1))[0]
                    img_np[img_height - y - 1][x]=[r,b,g]
                    x+=1
                elif (bit_num==16):#16-bit image reading
                    str1=bin(unpack("B", img.read(1))[0])
                    str2=bin(unpack("B", img.read(1))[0])
                    bgr_color=breakup_16byte(str1,str2)
                    img_np[img_height - y - 1][x]=[bgr_color[0],bgr_color[1],bgr_color[2]]
                    num+=2
                    x+=1
            x=0
            y+=1
            while (num % 4 != 0):  # The number of digits in each row must be a multiple of 4
                num += 1
                img.read(1)
            num=0
        plt.imshow(img_np)
        plt.show()
        img.close()
        #Save the picture in jpg format in the saved_img folder
        img_name_save="saved_img"+os.sep+"saved_"+img_path.split(os.sep)[1]
        matplotlib.image.imsave(img_name_save, img_np.astype(np.uint8))
        #Draw histogram
        if bit_num<=8:
            plt.figure("hist")
            arr = img_np.flatten()
            plt.hist(arr, bins=2**bit_num,facecolor='green', alpha=0.75)
            plt.show()
        else:
            plt.figure("hist")
            ar = np.array(img_np[:,:,0]).flatten()
            plt.hist(ar, bins=256,facecolor='r', edgecolor='r',alpha=0.5)
            ag = np.array(img_np[:,:,1]).flatten()
            plt.hist(ag, bins=256, facecolor='g', edgecolor='g',alpha=0.5)
            ab = np.array(img_np[:,:,2]).flatten()
            plt.hist(ab, bins=256, facecolor='b', edgecolor='b',alpha=0.5)
            plt.show()
        #Save the picture pixels to a txt file. Since savetxt in numpy can only save one-dimensional or two-dimensional arrays, now expand img_np
        txt_name="img_txt"+os.sep+"txt_"+(img_path.split(os.sep)[1]).split('.')[0]+'.txt'
        img_np=np.reshape(img_np,(img_height*3,img_width))
        np.savetxt(txt_name,img_np)
bmp_img_read_save_hist("./images")

