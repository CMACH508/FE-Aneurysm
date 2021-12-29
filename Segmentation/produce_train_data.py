import nibabel as nib
import numpy as np
import os



def f(brain):
    c,h,w = brain.shape
    #print(brain.shape)
    up = 0
    down = c
    left = 0
    right = h
    front = 0
    back = w
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
    for i in range(h):
        if np.all(brain_1[i] == 0):
            continue
        else:
            left = i
            break
    for i in range(h):
        if np.all(brain_1[h - i - 1] == 0):
            continue
        else:
            right = h - i - 1
            break

    brain_2 = brain.transpose((1,0,2))
    for i in range(h):
        if np.all(brain_2[i] == 0):
            continue
        else:
            front = i
            break
    for i in range(h):
        if np.all(brain_2[h - i - 1] == 0):
            continue
        else:
            back = h - i - 1
            break

    return up, down, left, right, front, back


def to_64x64(img):
    w,h = img.shape
    result = np.zeros((64,64))
    for i in range(64):
        for j in range(64):
            result[i][j] = img[int(i * (w-1) / float(64) + 0.5)][int(j * (h - 1) / float(64) + 0.5)]
    return result





in_path = ""
gt_in_path = ""
out_path = ""
gt_out_path = ""

filelist = os.listdir(in_path)


for file in filelist:
    img = np.array(nib.load(in_path + "/" + file).dataobj)
    gt = np.array(nib.load(gt_in_path +  "/" + file).dataobj)
    up, down, left, right, front, back = f(gt)
    up = up - (64 - (down - up + 1)) // 2
    down = up + 64
    front = front - (64 - (back - front + 1)) // 2
    back = front + 64
    left = left - (64 - (right - left + 1)) // 2
    right = left + 64

    result_1 = img[up:down,front:back,left:right]
    result_1[result_1 > 900] = 900
    result_1[result_1 < 0] = 0
    result_1 = result_1 / float(900)
    result_1 = result_1 * 2 - 1
    print(result_1.max(),result_1.min())
    result_2 = gt[up:down,front:back,left:right]
    #print(result_2)
    if(os.path.exists(out_path + "/img") is not True):
        os.makedirs(out_path + "/img")
        os.makedirs(gt_out_path + "/gt")
    np.save(out_path + "/img/" + file.split(".")[0], result_1)
    np.save(out_path + "/gt/" + file.split(".")[0], result_2)