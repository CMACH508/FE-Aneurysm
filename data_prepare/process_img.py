from PIL import Image
import numpy as np
import os
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


#此脚本将c++切割出来的图片，切割成合适的大小
#输入的图片中包含有方向和重建的信息


#os.listdir("D:/test")

in_path = "img_input"
out_path = "img_output"


filedir = os.listdir(in_path)
for file in filedir:
        img_jpg = Image.open(in_path + "/" + file)
        value = file.split('_')[1]
        img = np.array(img_jpg)
        left = img.shape[1]
        up = img.shape[0]
        right = 0
        down = 0
        for i in range(up):
            if(np.all(img[i] < [50,50,50])):
                continue
            else:
                if(i < up):
                    up = i
                if(i > down):
                    down = i
        img = img.transpose((1,0,2))
        for i in range(left):
            if(np.all(img[i] < [50,50,50])):
                continue
            else:
                if(i < left):
                    left = i
                if(i > right):
                    right = i
        file_num = file.split("_")[0]
        file_value = file.split("_")[1]
        file_dire = file.split("_")[3][0:2]
        if(file_dire == "up"):
            file_dire = "UP"
        if (file_dire == "do"):
            file_dire = "DOWN"
        if (file_dire == "le"):
            file_dire = "LEFT"
        if (file_dire == "ri"):
            file_dire = "RIGHT"
        if (file_dire == "fr"):
            file_dire = "FRONT"
        if (file_dire == "ba"):
            file_dire = "BACK"
        file_path = out_path + "/" + file_num + "/" + file_value + "/" + file_dire
        if(os.path.exists(file_path) is not True):
            print(file_path)
            os.makedirs(file_path)
        cropped = img_jpg.crop((left, up ,right + 1 ,down + 1))  # (left, upper, right, lower)
        cropped.save(out_path + "/" + file)