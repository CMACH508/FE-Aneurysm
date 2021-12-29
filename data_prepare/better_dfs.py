import os
#import pydicom
import numpy as np
#import SimpleITK
import nibabel as nib


in_path = "./data/brain_file"
out_path = "./data/img_source_data"

value = 150#此值可改，但一般为150


files = os.listdir(in_path)


for file in files:
        print(file)
        in_file_path = os.path.join(in_path,file)
        img = np.array((nib.load(in_file_path).dataobj),dtype=int)
        image = np.array((nib.load(in_file_path).dataobj),dtype=int)
        c = img.shape[0]
        img[img < value] = 0
        img[img >= value] = -1
        dic = {}
        stack = []
        num_list = []
        index = 1
        for i in range(c):
            for j in range(512):
                for k in range(512):
                    if (img[i][j][k] == -1):
                        #print('ok')
                        #print(i,j,k)
                        num = 0
                        stack.append([i, j, k])
                        img[i][j][k] = index
                        while (len(stack) > 0):
                            position = stack[-1]
                            del stack[-1]
                            num = num + 1
                            z, x, y = position[0], position[1], position[2]
                            if (z + 1 < c and img[z + 1][x][y] == -1):
                                stack.append([z + 1, x, y])
                                img[z + 1][x][y] = index
                            if (z - 1 >= 0 and img[z - 1][x][y] == -1):
                                stack.append([z - 1, x, y])
                                img[z - 1][x][y] = index
                            if (x + 1 < 512 and img[z][x + 1][y] == -1):
                                stack.append([z, x + 1, y])
                                img[z][x + 1][y] = index
                            if (x - 1 >= 0 and img[z][x - 1][y] == -1):
                                stack.append([z, x - 1, y])
                                img[z][x - 1][y] = index
                            if (y + 1 < 512 and img[z][x][y + 1] == -1):
                                stack.append([z, x, y + 1])
                                img[z][x][y + 1] = index
                            if (y - 1 >= 0 and img[z][x][y - 1] == -1):
                                stack.append([z, x, y - 1])
                                img[z][x][y - 1] = index
                        #num和index的关系是，numpy中为index的点有多少个
                        dic[num] = index
                        #print(num)
                        num_list.append(num)
                        index = index + 1
        num_list.sort(reverse=True)
        other_dic = sorted(dic.items())
        print(num_list[0])
        print(other_dic)
        #img[img == 0] = dic[num_list[0]]

        for i in range(30):

            img[img == dic[num_list[i]]] = dic[num_list[0]]
        image[img != dic[num_list[0]]] = 0

        new_img = nib.Nifti1Image(image, np.eye(4))
        out_file_path = out_path + "/" + file.split(".")[0] + "_" + str(value) +".nii.gz"
        nib.save(new_img, out_file_path)