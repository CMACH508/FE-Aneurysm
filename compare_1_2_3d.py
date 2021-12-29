import numpy as np


#brain是一个三维矩阵，找出各个维度上，第一个和最后一个大于等于index的位置
def bound(brain,index):
    c,h,w = brain.shape
    #print(brain.shape)
    up = 0
    down = c
    left = 0
    right = h
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
    for i in range(h):
        if np.all(brain_1[i] < index):
            continue
        else:
            left = i
            break
    for i in range(h):
        if np.all(brain_1[h - i - 1] < index):
            continue
        else:
            right = h - i - 1
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


def IOU_2d(gt, pre):
                # gt xmin ymin xmax ymax
                gt_x_min = gt[0]
                gt_x_max = gt[2]
                pre_x_min = pre[0]
                pre_x_max = pre[2]
                gt_y_min = gt[1]
                gt_y_max = gt[3]
                pre_y_min = pre[1]
                pre_y_max = pre[3]
                IOU_W = min(gt_x_min, pre_x_min) + gt_x_max - gt_x_min + pre_x_max - pre_x_min - max(gt_x_max,
                                                                                                     pre_x_max)
                # print(min(gt_x_min,pre_x_min),gt_x_max - gt_x_min,pre_x_max - pre_x_min,max(gt_x_max,pre_x_max))
                # print("IOU_W:   ",IOU_W)
                IOU_H = min(gt_y_min, pre_y_min) + gt_y_max - gt_y_min + pre_y_max - pre_y_min - max(gt_y_max,
                                                                                                     pre_y_max)
                # print("IOU_H:   ",IOU_H)

                if (IOU_W <= 0 or IOU_H <= 0):
                    return 0
                areas = IOU_H * IOU_W
                gt_areas = (gt_x_max - gt_x_min) * (gt_y_max - gt_y_min)
                pre_areas = (pre_x_max - pre_x_min) * (pre_y_max - pre_y_min)
                return areas / (gt_areas + pre_areas - areas)

def IOU_1d(first, second):
                first_min = first[0]
                first_max = first[1]
                second_min = second[0]
                second_max = second[1]
                Max = max(second_max, first_max)
                Min = min(first_min, second_min)
                return (first_max - first_min + second_max - second_min - (Max - Min)) / (Max - Min)

def IOU_3d(Reframe, GTframe):
                """
                自定义函数，计算两矩形 IOU，传入为 up down left right front back
                """
                # print("Reframe:",Reframe)
                up1 = Reframe[0]
                left1 = Reframe[2]
                front1 = Reframe[4]

                height1 = Reframe[1] - Reframe[0]
                width1 = Reframe[3] - Reframe[2]
                thickness1 = Reframe[5] - Reframe[4]

                up2 = GTframe[0]
                left2 = GTframe[2]
                front2 = GTframe[4]

                height2 = GTframe[1] - GTframe[0]
                width2 = GTframe[3] - GTframe[2]
                thickness2 = GTframe[5] - GTframe[4]

                end_up = max(up1 + height1, up2 + height2)
                start_up = min(up1, up2)
                height = height1 + height2 - (end_up - start_up)

                end_left = max(left1 + width1, left2 + width2)
                start_left = min(left1, left2)
                width = width1 + width2 - (end_left - start_left)

                end_front = max(front1 + thickness1, front2 + thickness2)
                start_front = min(front1, front2)
                thickness = thickness1 + thickness2 - (end_front - start_front)

                if width <= 0 or height <= 0 or thickness <= 0:
                    ratio = 0  # 重叠率为 0
                else:
                    Area = width * height * thickness;  # 两立方体相交体积
                    Area1 = width1 * height1 * thickness1;
                    Area2 = width2 * height2 * thickness2;
                    ratio = Area * 1. / (Area1 + Area2 - Area)
                # return IOU
                # print(ratio)
                return ratio