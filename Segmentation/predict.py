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
#slice_cube_path 是带有参数的  "../txt_test/my_all_output/"0.730.82
slice_cube_path = ""
gt_path = ""
save_path = "./data/result_data/"
model_path = "ckpts/model_epoch_500.pt"


device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
max_index = 100
max_iou = 0
model = VNet().to(device)
model.load_state_dict(torch.load(model_path,map_location=torch.device('cpu')))
Filedirlist = os.listdir(slice_cube_path)
M = 0
T = 0
P = 0
D = 0
num = 0
for filedir in Filedirlist:
    print(filedir)
    files = os.listdir(slice_cube_path  +"/" + filedir)
    gt = np.array(nib.load(gt_path + "/" + filedir + ".nii.gz").dataobj)
    gt = torch.from_numpy(gt)
    result = np.zeros(gt.shape)
    result = torch.from_numpy(result)

    for file in files:
        imgs = np.load(slice_cube_path  +"/" + filedir + "/" + file)
        c, w, h = imgs.shape
        print(imgs.shape)
        test_img = imgs
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
        test_img = test_img[np.newaxis,np.newaxis,: :, :]
        input = torch.from_numpy(test_img)
        input = input.to(dtype=torch.float32)
        input = input.to(device)
        output = model(input)
        output = output.argmax(dim=1).cpu()
        result[up:down, front:back, left:right] = result[up:down, front:back,
                                                              left:right] + output.squeeze()#torch.from_numpy(output)
    result[result >= 1] = 1
    result = result.numpy()
    #result = torch.numpy(result)
    result = result.astype(np.int16)
    new_result = nib.Nifti1Image(result,np.eye(4))
    print(save_path + "/" + filedir + ".nii.gz")
    nib.save(new_result,save_path + "/" + filedir + ".nii.gz")



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

