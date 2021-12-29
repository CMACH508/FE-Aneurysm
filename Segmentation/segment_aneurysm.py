import torch
import os
import numpy as np
import nibabel as nib
from vnet import VNet
from miou import Miou
from miou import Precision
from miou import TPR
from miou import Dice




#将slice后的结果送去分割
slice_cube_path = "../data/sliced_data/"#在前面slice出来的
gt_path = "../data/gt/"
save_path = "../data/result_data/"
model_path = "ckpts/model_epoch_500.pt"


def f(brain):
    c,h,w = brain.shape
    #print(brain.shape)
    up = 0
    down = c
    left = 0
    right = 512
    front = 0
    back = 512
    for i in range(c):
        #print(i)
        if np.all(brain[i] == 0):
            continue
        else:
            up = i
            break
    for i in range(c):
        if np.all(brain[c - i - 1] == 0):
            continue
        else:
            down = c - i - 1
            break

    brain_1 = brain.transpose((2,1,0))
    for i in range(512):
        if np.all(brain_1[i] == 0):
            continue
        else:
            left = i
            break
    for i in range(512):
        if np.all(brain_1[512 - i - 1] == 0):
            continue
        else:
            right = 512 - i - 1
            break

    brain_2 = brain.transpose((1,0,2))
    for i in range(512):
        if np.all(brain_2[i] == 0):
            continue
        else:
            front = i
            break
    for i in range(512):
        if np.all(brain_2[512 - i - 1] == 0):
            continue
        else:
            back = 512 - i - 1
            break

    return up, down, left, right, front, back


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
max_index = 100
max_iou = 0
Filedirlist = os.listdir(slice_cube_path)
print(Filedirlist)
M = 0
T = 0
P = 0
D = 0
num = 0
for Filedir in Filedirlist:
    print(Filedir)

    model = VNet().to(device)
    model.load_state_dict(torch.load(model_path,map_location=torch.device('cpu')))
    
    files = os.listdir(slice_cube_path + "/" + Filedir)
    #print("ok")
    # gt = np.array(nib.load("../data/gt/" + filedir + ".nii.gz").dataobj)
    # print("gt.shape:",gt.shape)
    gt = np.array(nib.load(gt_path + "/" + Filedir + ".nii.gz").dataobj)
    gt = torch.from_numpy(gt)
    result = np.zeros(gt.shape)
    result = torch.from_numpy(result)

    for file in files:

        imgs = np.load(slice_cube_path + "/" + Filedir + "/" + file)
        #print("imgsshape",imgs.shape)
        c, w, h = imgs.shape
        print(imgs.shape)
        if(imgs.shape[0] != 64 or imgs.shape[1] != 64 or imgs.shape[2] != 64):
            continue

        test_img = imgs

        #test_img = to_64x64x64(imgs)

        up = file.split("_")[0]
        down = file.split("_")[1]
        left = file.split("_")[2]
        right = file.split("_")[3]
        front = file.split("_")[4]
        back = file.split("_")[5].split(".")[0]

        up = int(up)
        down = int(down)
        front = int(front)
        back = int(back)
        left = int(left)
        right = int(right)
        # imgs = np.load("source_detected_data/resample_64x64/" + filedir + "/" + file)
        test_img = test_img[np.newaxis,np.newaxis,: :, :]
        input = torch.from_numpy(test_img)
        input = input.to(dtype=torch.float32)
        input = input.to(device)
        output = model(input)
        # print(output.shape)
        output = output.argmax(dim=1).cpu()
        #out_source = to_source_from_64x64x64(output.squeeze(), c, w, h)
        # print("output.shape", output.shape)
        # c = down - up
        # w = back - front
        # h = right - left

        # print("out_source.shape",out_source.shape)
        result[up:down+1, front:back+1, left:right+1] = result[up:down+1, front:back+1,
                                                              left:right+1] + output.squeeze()#torch.from_numpy(output)
    # print("input.shape",input.shape)
    # np.save("valid_64x64_resample/out/" + file,output.cpu().numpy())

    # print("gt.shape", gt.shape)
    # miou = Miou(output.cpu(),gt.cpu())
    result[result >= 1] = 1
    result = result.numpy()
    #result = torch.numpy(result)
    result = result.astype(np.int16)
    new_result = nib.Nifti1Image(result,np.eye(4))
    print(save_path + "/" + Filedir + ".nii.gz")
    nib.save(new_result,save_path + "/" + Filedir + ".nii.gz")



    #np.save(save_path + "/" + filedir, result)
    result = torch.from_numpy(result)
    miou = Miou(result, gt)
    print(miou)
    dice = Dice(result, gt)
    tpr = TPR(result,gt)
    precision = Precision(result,gt)

    #print(miou)
    M = M + miou
    D = D + dice
    T = T + tpr
    P = P + precision
    num = num + 1
print("M")
print(M / num)
print("D")
print(D / num)
print("T")
print(T / num)
print("P")
print(P / num)

