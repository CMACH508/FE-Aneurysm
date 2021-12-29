import os
import numpy as np
import torch
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
import random


def flip(index, img, gt):
    if(index == 1):
        img = img[:,:,::-1]
        gt = gt[:,:,::-1]
    if(index == 2):
        img = img[:,::-1,:]
        gt = gt[:,::-1,:]
    if(index == 3):
        img = img[::-1,:,:]
        gt = gt[::-1,:,:]
    return img,gt

def rotate(index, img,gt):
    if(index == 1):
        img = np.rot90(img,1,(0,1))
        gt = np.rot90(gt,1,(0,1))
    if(index == 2):
        img = np.rot90(img,2,(0,1))
        gt = np.rot90(gt,2,(0,1))
    if(index == 3):
        img = np.rot90(img,3,(0,1))
        gt = np.rot90(gt,3,(0,1))
    if(index == 4):
        img = np.rot90(img,1,(0,2))
        gt = np.rot90(gt,1,(0,2))
    if(index == 5):
        img = np.rot90(img,2,(0,2))
        gt = np.rot90(gt,2,(0,2))
    if(index == 6):
        img = np.rot90(img,3,(0,2))
        gt = np.rot90(gt,3,(0,2))
    if(index == 7):
        img = np.rot90(img,1,(1,2))
        gt = np.rot90(gt,1,(1,2))
    if(index == 8):
        img = np.rot90(img,2,(1,2))
        gt = np.rot90(gt,2,(1,2))
    if(index == 9):
        img = np.rot90(img,3,(1,2))
        gt = np.rot90(gt,3,(1,2))
    return img, gt








class BasicDataset(Dataset):
    def __init__(self, imgs_dir, gts_dir):
        self.imgs_dir = imgs_dir
        self.gts_dir = gts_dir
        self.imgs_list = os.listdir(imgs_dir)
        self.gts_list = os.listdir(gts_dir)

    def __len__(self):
        return len(self.imgs_list)

    def __getitem__(self, i):
        img = np.load(self.imgs_dir + "/" + self.imgs_list[i])
        #print(self.imgs_dir + "/" + self.imgs_list[i])
        gt = np.load(self.gts_dir + "/" + self.gts_list[i])

        # 0 1 2 3代表从不同的轴翻转
        index = int(random.random() * 4)
        img,gt = flip(index,img, gt)
        #print("index: ",index)
        #flip(index,img,gt)

        #0 1 2 3 4 5 6 7 8 9代表不同的旋转
        index = int(random.random() * 10)
        #print("index: ",index)
        img, gt = rotate(index, img, gt)


        img =img[np.newaxis,:,:,:]
        
        gt = gt[np.newaxis, :, :,:]
        #flip
        #rotate

        return img.astype(np.float32), gt.astype(np.float32)


if __name__ == "__main__":
    test_loader = DataLoader(
        BasicDataset("unet_out/img","unet_out/gt"))
    for i , data in enumerate(test_loader):
        #print("epoch",i)
        img, gt = data
        print(img.shape)
        print(gt.shape)
        print(img[0][0][9])
        #print(gt)
        #print(target.shape)
        break