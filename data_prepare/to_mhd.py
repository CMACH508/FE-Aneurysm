import os
from pathlib import Path
import pydicom
import numpy as np
import SimpleITK
import nibabel as nib

# 将nii文件转换为mhd文件
# filelist 是包含value信息的 filenum_vlaue.nii.gz
# 在faster rcnn detect的时候， 需要in_path中的这个文件，以及对应的value



#out_path和f_path 应该在运行slicing.cpp的目录下
in_path = "img_source_data"
out_path = "Files/SaveRaw"
dicom_path = "DICOM"
f_path = ""
gt_path = "gt"



files = os.listdir(in_path)



#filelist = os.listdir(in_path)
#print(filelist)
def bound(brain,index):
    c,h,w = brain.shape
    #print(brain.shape)
    up = 0
    down = c
    left = 0
    right = w
    front = 0
    back = h
    for i in range(c):
        #print(i)
        if np.all(brain[i] < index):
            continue
        else:
            up = i
            break
    for i in range(c):
        if np.all(brain[c - i - 1] < index):
            continue
        else:
            down = c - i - 1
            break
    brain_1 = brain.transpose((2,1,0))
    for i in range(w):
        if np.all(brain_1[i] < index):
            continue
        else:
            left = i
            break
    for i in range(w):
        if np.all(brain_1[w - i - 1] < index):
            continue
        else:
            right = w - i - 1
            break
    brain_2 = brain.transpose((1,0,2))
    for i in range(h):
        if np.all(brain_2[i] < index):
            continue
        else:
            front = i
            break
    for i in range(h):
        if np.all(brain_2[h - i - 1] < index):
            continue
        else:
            back = h - i - 1
            break
    return up, down, left, right, front, back


def load_scan(path):
    slices = [pydicom.read_file(path + '/' + s) for s in os.listdir(path)]
    slices.sort(key = lambda x: float(x.ImagePositionPatient[2]))
    try:
        slice_thickness = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    except:
        slice_thickness = np.abs(slices[0].SliceLocation - slices[1].SliceLocation)
 
    for s in slices:
        s.SliceThickness = slice_thickness
    return slices




def f(brain):
    brain = brain[np.newaxis,:,:]
    c,h,w = brain.shape
    ##print(brain.shape)
    up = 0
    down = c
    left = 0
    right = 512
    front = 0
    back = 512
    brain_2 = brain.transpose((1,0,2))
    for i in range(512):
        if np.all(brain_2[i] < 1180):
            continue
        else:
            front = i
            break
    for i in range(512):
        if np.all(brain_2[512 - i - 1] < 1180):
            continue
        else:
            back = 512 - i - 1
            break

    return front, back


space = [0.488281,0.488281,0.65]

#filelist = os.listdir("data/gt")

f1 = open(f_path + "/gt_bound.txt", "w")
f2 = open(f_path + "/image_bound.txt","w")
f3 = open(f_path + "/name.txt","w")




for file in files:

    print(file)
    #filenum = file.split("_")[0]
    filenum = file.split("_")[0]
    value = int(file.split("_")[1].split(".")[0])
    
    PathDicom = dicom_path + "/" + filenum

    lstFilesDCM = []
    image = np.array((nib.load(in_path + "/" + filenum + "_" + str(value) + ".nii.gz").dataobj))
    gt = np.array(nib.load(gt_path + "/" + filenum + ".nii.gz").dataobj)

    lstFilesDCM = load_scan(PathDicom)
    RefDs = lstFilesDCM[0]  # 读取第一张dicom图片
   
    ConstPixelDims = (int(image.shape[0]), int(image.shape[1]), image.shape[2])
   
    ConstPixelSpacing = (float(RefDs.PixelSpacing[0]), float(RefDs.PixelSpacing[1]), RefDs.SliceThickness)
    print(RefDs.SliceThickness)
    print(RefDs.PixelSpacing)
    Origin = RefDs.ImagePositionPatient
    print(Origin)
    ArrayDicom = np.zeros(image.shape)  # array is a numpy array
    c = image.shape[0]
    image = image.transpose((1,0,2))
    img = np.zeros((image.shape))
    for i in range(512):
         img[i] = image[511-i]
    img = img.transpose((1,0,2))
    image = img




    up_1, down_1, left_1, right_1, front_1, back_1 = bound(gt,1)#up down 是z轴 left right 是x轴 front back 是y轴
    up_2, down_2, left_2, right_2, front_2, back_2 = bound(image,value)
    print(bound(image,value))
    down_2 = down_2 + 1
    right_2 = right_2 + 1
    back_2 = back_2 + 1


    SaveRawDicom = out_path + filenum + "_" + str(value)
    #print(SaveRawDicom)
    if os.path.exists(SaveRawDicom) is not True:
        os.makedirs(SaveRawDicom)




    f1.write(str(right_1) + " " + str(left_1) + " " + str(front_1) + " " + str(back_1) + " " + str(down_1) + " " + str(up_1) + " " +"\n")
    f2.write(filenum + " " + str(value) +"  " +str(right_2) + " " + str(left_2) + " " + str(front_2) + " " + str(back_2) + " " + str(down_2) + " " + str(up_2) + " " +"\n")
    f3.write(filenum + " " + str(value) + "\n")


    image[image<value] = 0
    print(bound(image,value))



    for i in range(0,c):
         ArrayDicom[i] = image[i]
    sitk_img = SimpleITK.GetImageFromArray(ArrayDicom, isVector=False)
    sitk_img.SetSpacing(ConstPixelSpacing)
    sitk_img.SetOrigin(Origin)
    SimpleITK.WriteImage(sitk_img, os.path.join(SaveRawDicom, "sample" + ".mhd"))