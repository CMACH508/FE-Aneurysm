from compare_1_2_3d import IOU_1d,IOU_2d,IOU_3d

_3d_iou = 0.03
_3d_para = 0.3

_2d_para = 0.5#变小的时候最后的框会变大，而且会使false增加，当然也会使检测到的增加
_1d_para = 0.7#变大会使false减少当然也会使true减少
removed_slice = 3#
connected_slice = 3#





def left_cmp(x):
                return x[2]


def right_cmp(x):
                return -x[2]


def front_cmp(x):
                return x[4]


def back_cmp(x):
                return -x[4]


def up_cmp(x):
                return x[0]


def down_cmp(x):
                return -x[0]





#把各个方向上的方框连起来
def process_backlist(List,last_back):
                # 作用是把在一起的连起来
                List = sorted(List, key=back_cmp)
                # print("back_sort")
                # print(List)
                List_refer = List.copy()
                while (len(List)):
                    x = List[0]
                    Len = len(List_refer)
                    # print(Len)
                    for i in range(Len):
                        # print("i",i)
                        # print("list_refer",List_refer)
                        # print(List_refer[i])
                        if (IOU_2d([x[0], x[2], x[1], x[3]], [List_refer[i][0], List_refer[i][2], List_refer[i][1],
                                                              List_refer[i][3]]) >= _2d_para and abs(
                            x[4] - List_refer[i][4]) <= connected_slice):
                            List.remove(List_refer[i])
                            x[0] = min(x[0], List_refer[i][0])
                            x[1] = max(x[1], List_refer[i][1])
                            x[2] = min(x[2], List_refer[i][2])
                            x[3] = max(x[3], List_refer[i][3])
                            x[4] = min(x[4], List_refer[i][4])
                            x[5] = max(x[5], List_refer[i][5])
                    last_back.append(x)
                    List_refer = List.copy()

def process_leftlist(List,last_left):
                List = sorted(List, key=left_cmp)
                # print("left_List:")
                # print(List)
                List_refer = List.copy()
                while (len(List)):
                    x = List[0]
                    Len = len(List_refer)
                    for i in range(Len):
                        if (IOU_2d([x[0], x[4], x[1], x[5]], [List_refer[i][0], List_refer[i][4], List_refer[i][1],
                                                              List_refer[i][5]]) >= _2d_para and abs(
                            x[3] - List_refer[i][3]) <= connected_slice):
                            List.remove(List_refer[i])
                            x[0] = min(x[0], List_refer[i][0])
                            x[1] = max(x[1], List_refer[i][1])
                            x[2] = min(x[2], List_refer[i][2])
                            x[3] = max(x[3], List_refer[i][3])
                            x[4] = min(x[4], List_refer[i][4])
                            x[5] = max(x[5], List_refer[i][5])
                        # else:
                        #    print(IOU_2d([x[0], x[4], x[1], x[5]],[List_refer[i][0], List_refer[i][4], List_refer[i][1], List_refer[i][5]]))
                        #    print("x :",x)
                        #    print(List_refer[i])

                    last_left.append(x)
                    # print("left_x:",x)
                    List_refer = List.copy()


def process_rightlist(List,last_right):
                List = sorted(List, key=right_cmp)
                List_refer = List.copy()
                while (len(List)):
                    x = List[0]
                    Len = len(List_refer)
                    for i in range(Len):
                        # print([x[0],x[4],x[1],x[5]])
                        # print([List_refer[i][0],List_refer[i][4],List_refer[i][1],List_refer[i][5]])
                        # print(IOU_2d([x[0],x[4],x[1],x[5]],[List_refer[i][0],List_refer[i][4],List_refer[i][1],List_refer[i][5]]))
                        if (IOU_2d([x[0], x[4], x[1], x[5]], [List_refer[i][0], List_refer[i][4], List_refer[i][1],
                                                              List_refer[i][5]]) >= _2d_para and abs(
                            x[2] - List_refer[i][2]) <= connected_slice):
                            List.remove(List_refer[i])
                            x[0] = min(x[0], List_refer[i][0])
                            x[1] = max(x[1], List_refer[i][1])
                            x[2] = min(x[2], List_refer[i][2])
                            x[3] = max(x[3], List_refer[i][3])
                            x[4] = min(x[4], List_refer[i][4])
                            x[5] = max(x[5], List_refer[i][5])
                    last_right.append(x)
                    List_refer = List.copy()




def process_uplist(List,last_up):
                List = sorted(List, key=up_cmp)
                List_refer = List.copy()
                
                
                while (len(List)):
                    x = List[0]
                    Len = len(List_refer)
                    # print("Len:",Len)
                    for i in range(Len):
                        # print(i)
                        # if(i == 0):
                        # print(x)
                        # print(List_refer[i])
                        # print(x[2],x[4],x[3],x[5])
                        # print(List_refer[i][2],List_refer[i][4],List_refer[i][3],List_refer[i][5])
                        # print("iou:",IOU_2d([x[2],x[4],x[3],x[5]],[List_refer[i][2],List_refer[i][4],List_refer[i][3],List_refer[i][5]]))
                        # print("abs:",abs(x[0] - List_refer[i][0]))
                        if (IOU_2d([x[2], x[4], x[3], x[5]], [List_refer[i][2], List_refer[i][4], List_refer[i][3],
                                                              List_refer[i][5]]) >= _2d_para and abs(
                            x[1] - List_refer[i][1]) <= connected_slice):  # 这个地方不能这么算，
                            List.remove(List_refer[i])
                            x[0] = min(x[0], List_refer[i][0])
                            x[1] = max(x[1], List_refer[i][1])
                            x[2] = min(x[2], List_refer[i][2])
                            x[3] = max(x[3], List_refer[i][3])
                            x[4] = min(x[4], List_refer[i][4])
                            x[5] = max(x[5], List_refer[i][5])
                    last_up.append(x)
                    List_refer = List.copy()


def process_downlist(List,last_down):
                #print("down")
                List = sorted(List, key=down_cmp)
                List_refer = List.copy()
                #for this_list in List:
                #    print(this_list)
                while (len(List)):
                    x = List[0]
                    Len = len(List_refer)
                    #print("x  ",x)
                    for i in range(Len):
                        if (IOU_2d([x[2], x[4], x[3], x[5]], [List_refer[i][2], List_refer[i][4], List_refer[i][3],
                                                              List_refer[i][5]]) >= _2d_para and abs(
                            x[0] - List_refer[i][0]) <= connected_slice):  # 这个地方不能这么算，
                            List.remove(List_refer[i])
                            x[0] = min(x[0], List_refer[i][0])
                            x[1] = max(x[1], List_refer[i][1])
                            x[2] = min(x[2], List_refer[i][2])
                            x[3] = max(x[3], List_refer[i][3])
                            x[4] = min(x[4], List_refer[i][4])
                            x[5] = max(x[5], List_refer[i][5])
                        #else:
                        #    print(IOU_2d([x[2], x[4], x[3], x[5]], [List_refer[i][2], List_refer[i][4], List_refer[i][3],
                        #                                      List_refer[i][5]]))
                    #print("XX  ",x)
                    last_down.append(x)
                    List_refer = List.copy()


def process_frontlist(List,last_front):
                List = sorted(List, key=front_cmp)
                List_refer = List.copy()
                while (len(List)):
                    x = List[0]
                    Len = len(List_refer)
                    # print(Len)
                    for i in range(Len):
                        if (IOU_2d([x[0], x[2], x[1], x[3]], [List_refer[i][0], List_refer[i][2], List_refer[i][1],
                                                              List_refer[i][3]]) >= _2d_para and abs(
                            x[5] - List_refer[i][5]) <= connected_slice):
                            List.remove(List_refer[i])
                            x[0] = min(x[0], List_refer[i][0])
                            x[1] = max(x[1], List_refer[i][1])
                            x[2] = min(x[2], List_refer[i][2])
                            x[3] = max(x[3], List_refer[i][3])
                            x[4] = min(x[4], List_refer[i][4])
                            x[5] = max(x[5], List_refer[i][5])
                    last_front.append(x)
                    List_refer = List.copy()



#去除掉一个方向上的cube只检测到两次的情况
def process_last_up_down(List):
                # print("last_up_down")
                # 作用是除去只检测到两次以下的地方
                Len = len(List)
                refer = List.copy()
                for i in range(Len):
                    x = refer[i]
                    if (x[1] - x[0] <= removed_slice):
                        List.remove(x)


def process_last_left_right(List):
                # print("last_left_right")
                Len = len(List)
                refer = List.copy()
                for i in range(Len):
                    x = refer[i]
                    if (x[3] - x[2] <= removed_slice):
                        List.remove(x)


def process_last_front_back(List):
                # print("last_front_back")
                Len = len(List)
                refer = List.copy()
                for i in range(Len):
                    x = refer[i]
                    if (x[5] - x[4] <= removed_slice):
                        List.remove(x)





#################两个cube取交集
def process_front_up(List_1, List_2,last):
                # print("front_up")

                for i in range(len(List_1)):
                    for j in range(len(List_2)):
                        if (IOU_3d(List_1[i], List_2[j]) > 0 and IOU_1d([List_1[i][2], List_1[i][3]],
                                                                        [List_2[j][2], List_2[j][3]]) > _1d_para):
                            x = [0, 0, 0, 0, 0, 0]
                            x[0] = List_1[i][0]
                            x[1] = List_1[i][1]
                            x[2] = min(List_1[i][2], List_2[j][2])
                            x[3] = max(List_1[i][3], List_2[j][3])
                            x[4] = List_2[j][4]
                            x[5] = List_2[j][5]
                            last.append(x)
                            # print("front_up_last",last)
def process_front_left(List_1, List_2,last):
                # print("front_left")

                # print("list2",List_2)
                for i in range(len(List_1)):
                    for j in range(len(List_2)):
                        # print("j:",j,"       ",last)
                        # print(List_2[j])
                        if (IOU_3d(List_1[i], List_2[j]) > 0 and IOU_1d([List_1[i][0], List_1[i][1]],
                                                                        [List_2[j][0], List_2[j][1]]) > _1d_para):
                            x = [0, 0, 0, 0, 0, 0]
                            x[0] = min(List_1[i][0], List_2[j][0])
                            x[1] = max(List_1[i][1], List_2[j][1])
                            # print(List_1[i][1],List_2[j][1])
                            # print("x[1]",x[1])
                            x[2] = List_1[i][2]
                            x[3] = List_1[i][3]
                            # print("2", last)
                            x[4] = List_2[j][4]
                            x[5] = List_2[j][5]
                            # print("befor",last)
                            # print("x",x)
                            last.append(x)
                            # print("after",last)
                            # print("last",last)


def process_up_left(List_1, List_2,last):
                # print("up_left")

                for i in range(len(List_1)):
                    for j in range(len(List_2)):
                        if (IOU_3d(List_1[i], List_2[j]) > 0 and IOU_1d([List_1[i][4], List_1[i][5]],
                                                                        [List_2[j][4], List_2[j][5]]) > _1d_para):
                            x = [0, 0, 0, 0, 0, 0]
                            x[0] = List_2[j][0]
                            x[1] = List_2[j][1]
                            x[2] = List_1[i][2]
                            x[3] = List_1[i][3]
                            x[4] = min(List_1[i][4], List_2[j][4])
                            x[5] = max(List_1[i][5], List_2[j][5])
                            last.append(x)
                            # print("up_left_last", last)

#最后的cube中去除掉重叠的cube
def process_last(last,result):
                # print("last")
                last_refer = last.copy()
                while (len(last)):
                    x = last[0]
                    Len = len(last_refer)
                    for i in range(Len):
                        if (IOU_3d(x, last_refer[i]) > _3d_para):
                            last.remove(last_refer[i])
                            x[0] = max(x[0], last_refer[i][0])
                            x[1] = min(x[1], last_refer[i][1])
                            x[2] = max(x[2], last_refer[i][2])
                            x[3] = min(x[3], last_refer[i][3])
                            x[4] = max(x[4], last_refer[i][4])
                            x[5] = min(x[5], last_refer[i][5])
                    result.append(x)
                    last_refer = last.copy()