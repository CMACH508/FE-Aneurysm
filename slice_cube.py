# -*- coding:UTF-8 -*-
import numpy as np
import os
import nibabel as nib
import os, cv2
import matplotlib.pyplot as plt
from PIL import Image
from Process_all_kinds_list import process_backlist, process_downlist, process_frontlist, process_leftlist,\
    process_rightlist,process_uplist,process_up_left,process_front_up,process_front_left,\
        process_last_front_back,process_last_left_right,process_last_up_down,process_last
from compare_1_2_3d import bound, IOU_1d,IOU_2d,IOU_3d
from utils import read_list


#切割img
#并且判断是否成功检测到
img_path = "data/nii_file"
label_path = "data/gt"
save_path = "data/sliced_data"
filenames = [
    "result.txt"
]

no_detected_num = 0
no_aneurysm_num = 0
false_detected = 0

_3d_iou = 0.03
_3d_para = 0.3

#_2d_para = 0.53#变小的时候最后的框会变大，而且会使false增加，当然也会使检测到的增加
#_1d_para = 0.73#变大会使false减少当然也会使true减少
removed_slice = 3#
connected_slice = 3#


para_list = [[0.5,0.7]]




for _1d_para,_2d_para  in para_list:
    all_detect_num = 0
    all_num = 0
    all_false_positive = 0
    print(_2d_para,_1d_para)
    for filename in filenames:
            txt = open(filename)
            data = txt.readlines()
            
            false_positive = 0
            linenum = -1
            while(linenum < len(data)-1):
                detected = "no"
                last_up = []
                last_down = []
                last_front = []
                last_back = []
                last_left = []
                last_right = []
                last = []
                result = []
                linenum,im_num,gt_box,up_list,back_list,down_list,front_list,left_list,right_list = read_list(data,linenum)
                all_num = all_num + 1

            
                


                #把连续的连起来
                process_backlist(back_list,last_back)
                process_frontlist(front_list,last_front)
                process_rightlist(right_list,last_right)
                process_leftlist(left_list,last_left)
                process_downlist(down_list,last_down)
                process_uplist(up_list,last_up)


                # 去除掉只检测到两次的东西
                process_last_up_down(last_up)
                process_last_up_down(last_down)
                process_last_left_right(last_right)
                process_last_left_right(last_left)
                process_last_front_back(last_front)
                process_last_front_back(last_back)
                for list in last_back:
                    list[5] = list[4] + 1
                    list[4] = list[4] - 3
                for list in last_front:
                    list[4] = list[5] - 1
                    list[5] = list[5] + 3
                for list in last_up:
                    list[0] = list[1] - 1
                    list[1] = list[1] + 3
                for list in last_down:
                    list[1] = list[0] + 1
                    list[0] = list[0] - 3
                for list in last_left:
                    list[2] = list[3] - 1
                    list[3] = list[3] + 3
                for list in last_right:
                    list[3] = list[2] + 1
                    list[2] = list[2] - 3

                process_front_up(last_front, last_up,last)
                process_front_up(last_front, last_down,last)
                process_front_up(last_back, last_up,last)
                process_front_up(last_back, last_down,last)
                process_front_left(last_front, last_left,last)
                process_front_left(last_front, last_right,last)
                process_front_left(last_back, last_left,last)
                process_front_left(last_back, last_right,last)
                process_up_left(last_up, last_left,last)
                process_up_left(last_up, last_right,last)
                process_up_left(last_down, last_right,last)
                process_up_left(last_down, last_left,last)
                process_last(last, result)
                gt = gt_box
                
                for box in result:
                    box_up,box_down,box_left,box_right,box_front,box_back = int(box[0]),int(box[1]),int(box[2]),int(box[3]),int(box[4]),int(box[5])
                    box_up = box_up - (64 - (box_down - box_up + 1)) // 2
                    box_down = box_up + 63
                    box_front = box_front - (64 - (box_back - box_front + 1)) // 2
                    box_back = box_front + 63
                    box_left = box_left - (64 - (box_right - box_left + 1)) // 2
                    box_right = box_left + 63
                    if(os.path.exists(save_path + "/" + im_num) is not True):
                        os.makedirs(save_path + "/" + im_num)
                    img = np.array(nib.load(img_path + "/" + im_num + ".nii.gz").dataobj)
                    np.save(save_path + "/" + im_num + "/" + str(box_up) + "_"+ str(box_down) + "_"+ str(box_left) + "_"+ str(box_right) + "_"+ str(box_front) + "_"+ str(box_back)+".npy",img[box_up:box_down+1,box_front:box_back+1,box_left:box_right+1])
                    if (IOU_3d(gt, box) >= _3d_iou):
                        detected = "yes"
                        #print("yes")
                    if (IOU_3d(gt, box) < _3d_iou):
                        all_false_positive = all_false_positive + 1

                if (detected == "yes"):
                    #print("yes",im_num)
                    all_detect_num = all_detect_num + 1
                else:
                    print("no",im_num)
                    no_detected_num = no_detected_num + 1

    print(all_num)
    print(all_detect_num)
    print(all_false_positive)
    print(all_detect_num/float(all_num))
